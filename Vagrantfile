require 'yaml'
require 'vagrant/errors'
require 'vagrant/ui'
require 'vagrant/util/downloader'
require 'vagrant/util/subprocess'

# Require Vagrant 2.0+.
Vagrant.require_version '>= 2.0.0'

# Setting up globals from YAML configuration file.
settings = YAML::load_file('config.yml')
$images = settings.fetch('images', {})
$maven = settings.fetch('maven', {})
$rpms = settings.fetch('rpms', {})
$pg_version = settings.fetch('versions')['postgresql']
$pg_dotless = $pg_version.gsub('.', '')

# Special workaround if we want the `rpmbuild` UID and GID to match that of
# the user invoking Vagrant, which simplifies file permissions for host
# volume mounts.
if ENV.key?('RPMBUILD_UID_MATCH')
  $images['base']['rpmbuild']['args']['rpmbuild_uid'] = Process.uid
  $images['base']['rpmbuild']['args']['rpmbuild_gid'] = Process.gid
end

## Functions used by Vagrant containers.

def collect_rpms(filters)
  collected = {}
  filters.each do |filter|
    $rpms.each do |name, options|
      if (name == filter or
          options.fetch('image', nil) == filter)
        collected[name] = options
      end
    end
  end
  return collected
end


def make_hoot_dirs
  ['hootenanny', 'RPMS', 'cache', 'cache/m2', 'cache/npm'].each do |directory|
    if ! File.directory?(directory)
      Dir.mkdir(directory, 0755)
    end
  end
end


# Use Vagrant utilities to download and extract the Maven cache.
def maven_cache
  if ! File.directory?('cache/m2/repository')
    ui = Vagrant::UI::Basic.new()
    ui.say('info', 'Downloading Maven cache')
    tmp_file = '/var/tmp/m2-cache.tar.gz'

    d = Vagrant::Util::Downloader.new(
       $maven['cache_url'],
       tmp_file,
       {
         :sha1 => $maven['cache_sha1'],
         :ui => ui,
       }
    )

    begin
      d.download!
    rescue Vagrant::Errors::VagrantError
      raise Vagrant::Errors::VagrantError, output: 'Could not download maven cache!'
    end

    ui.say('info', 'Extracting Maven cache')
    result = Vagrant::Util::Subprocess.execute(
      'tar', '-C', 'cache/m2', '-xzf', tmp_file
    )
    if result.exit_code != 0
      raise Vagrant::Errors::VagrantError, output: 'Could not extract Maven cache.'
    end
  end
end


def rpm_file(name, options)
  arch = options.fetch('arch', 'x86_64')
  dist = options.fetch('dist', '.el7')
  return "RPMS/#{arch}/#{name}-#{options['version']}#{dist}.#{arch}.rpm"
end


def shared_folders(container, name, options, rpmbuild: false)
  container.vm.synced_folder '.', '/vagrant', disabled: true

  if options.fetch('rpmbuild', rpmbuild)
    make_hoot_dirs()

    # Container needs to be able to write RPMs via bind mounts.
    container.vm.synced_folder 'RPMS', '/rpmbuild/RPMS'
    container.vm.synced_folder 'SPECS', '/rpmbuild/SPECS'
    container.vm.synced_folder 'SOURCES', '/rpmbuild/SOURCES'

    # Additional directories need to be shared for Hootenanny builds.
    if options.fetch('spec_file', '') == 'SPECS/hootenanny.spec'
      if ENV.fetch('MAVEN_CACHE', '1') == '1'
        maven_cache()
      end

      container.vm.synced_folder 'cache/m2', '/rpmbuild/.m2'
      container.vm.synced_folder 'cache/npm', '/rpmbuild/.npm'
      container.vm.synced_folder 'hootenanny', '/rpmbuild/hootenanny'
      container.vm.synced_folder 'scripts', '/rpmbuild/scripts'
    end
  end
end


def build_container(config, name, options)
  config.vm.define name do |container|
    shared_folders(container, name, options)

    container.vm.provider :docker do |d|
      # On the containers we're building don't actually run anything.
      d.build_dir = options.fetch('build_dir', '.')
      d.cmd = options.fetch('cmd', [])

      # Start build arguments.
      build_args = []
      args = options.fetch('args', {})

      # Pull out `BuildRequires:` packages and add them to a `packages`
      # build argument for the container.
      if options.fetch('buildrequires', false)
        build_packages = []

        # Fill out dummy macros so `rpmspec` won't choke.
        rpmspec_cmd = ['rpmspec', '-q', '--buildrequires']
        {
          '_topdir' => File.realpath(File.dirname(__FILE__)),
          'hoot_version_gen' => '0.0.0',
          'pg_dotless' => $pg_dotless,
          'rpmbuild_version' => '0.0.0',
          'rpmbuild_release' => '1',
          'tomcat_version' => '0.0.0',
        }.each do |macro, expr|
          rpmspec_cmd << '--define'
          # Have to put in single quotes surrounding macro since this is a
          # raw command.
          rpmspec_cmd << "#{macro} #{expr}"
        end
        rpmspec_cmd << options.fetch(
          'spec_file', "SPECS/#{name.gsub('rpmbuild-', '')}.spec"
        )

        result = Vagrant::Util::Subprocess.execute(*rpmspec_cmd)
        if result.exit_code != 0
          raise Vagrant::Errors::VagrantError, output: "Couldn't execute rpmspec for #{name}"
        end

        build_packages = result.stdout.split("\n")
        if build_packages
          build_args << '--build-arg'
          build_args << "packages=#{build_packages.join(' ')}"
        end
      end

      args.each do |arg, value|
        build_args << '--build-arg'
        build_args << "#{arg}=#{value}"
      end

      # Add any tags to the build arguments.
      image_name = "hootenanny/#{name}"

      options.fetch('tags', ['latest']).each do |tag|
        build_args << '--tag'
        build_args << "#{image_name}:#{tag}"
      end

      # Setting provisioner parameters.
      d.build_args = build_args

      # Set up basic container settings.
      d.dockerfile = options.fetch('dockerfile', "docker/Dockerfile.#{name}")
      d.remains_running = options.fetch('remains_running', false)
    end
  end
end


# Configure a container to be run from another image to execute `rpmbuild`.
def rpmbuild(config, name, options)
  autostart = options.fetch('autostart', false)
  config.vm.define name, autostart: autostart do |container|
    shared_folders(container, name, options, rpmbuild: true)

    image_name = "hootenanny/#{options['image']}"

    container.vm.provider :docker do |d|
      d.image = image_name

      # Add `--rm` to the creation args so we don't need to keep the container
      # (it's image is just ran to compile the RPM).
      d.create_args = options.fetch(
        'create_args', ['--rm']
      )
      d.remains_running = options.fetch(
        'remains_running', true
      )

      # Start constructing the `rpmbuild` command.
      rpmbuild_cmd = ['rpmbuild']

      # Pass in the RPM version/release information via CLI define statements.
      version, release = options['version'].split('-')
      defines = options.fetch('defines', {})
      defines.update(
        {
          'rpmbuild_version' => version,
          'rpmbuild_release' => release,
        }
      )
      defines.each do |macro, expr|
        rpmbuild_cmd << '--define'
        rpmbuild_cmd << "#{macro} #{expr}"
      end

      # Pass through any variables we want to undefine.
      options.fetch('undefines', []).each do |macro|
        rpmbuild_cmd << '--undefine'
        rpmbuild_cmd << macro
      end

      # Default to using `rpmbuild -bb`.
      rpmbuild_cmd << options.fetch('build_type', '-bb')
      rpmbuild_cmd << options.fetch('spec_file', "SPECS/#{name}.spec")

      d.cmd = rpmbuild_cmd
    end
  end
end

## Vagrant configuration

Vagrant.configure(2) do |config|
  # Base images, including one for building Hootenanny, based on
  # stable released dependencies, as well as those needed for
  # GDAL (FileGDBAPI, libgeotiff, libkml) and NodeJS.
  $images['base'].each do |name, options|
    build_container(config, name, options)
  end

  # Generic, NodeJS, and GDAL dependency RPMS are built first.
  collect_rpms(
    ['rpmbuild-generic',
     'rpmbuild-geos',
     'rpmbuild-glpk',
     'rpmbuild-libgeotiff',
     'rpmbuild-libkml',
     'rpmbuild-nodejs']
  ).each do |name, options|
    rpmbuild(config, name, options)
  end

  # GDAL can be built when dependency RPMs are present.
  $images['gdal'].each do |name, options|
    build_container(config, name, options)
  end

  collect_rpms(['rpmbuild-gdal']).each do |name, options|
    rpmbuild(config, name, options)
  end

  # PostGIS can be built when GDAL RPMs are present.
  $images['postgis'].each do |name, options|
    build_container(config, name, options)
  end

  collect_rpms(['rpmbuild-postgis']).each do |name, options|
    rpmbuild(config, name, options)
  end

  # The development containers are last because they all depend
  # on RPMS built previously.
  $images['hoot'].each do |name, options|
    build_container(config, name, options)
  end
end
