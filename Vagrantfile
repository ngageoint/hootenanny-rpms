require 'yaml'

# Setting up globals from YAML configuration file.
settings = YAML::load_file('config.yml')
$images = settings.fetch('images', {})
$rpms = settings.fetch('rpms', {})
$pg_version = settings.fetch('pg_version')
$pg_dotless = $pg_version.gsub('.', '')

## Functions used by Vagrant containers.

def build_container(config, name, options)
  config.vm.define name do |container|
    container.vm.synced_folder '.', '/vagrant', disabled: true
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

        spec_file = options.fetch(
          'spec_file', "SPECS/#{name.gsub('rpmbuild-', '')}.spec"
        )

        File.open(spec_file, 'r') { |fh|
          fh.each do |line|
            if line.start_with?('BuildRequires:')
              requirement = line.gsub('BuildRequires:', '').strip.split()[0]
              # XXX: Have to replace macro requirements :(
              requirement.gsub('%{pg_dotless}', $pg_dotless)
              build_packages << requirement
            end
          end
        }

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

      build_args << '--tag'
      build_args << image_name

      options.fetch('tags', []).each do |tag|
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


# Configure container for being used to run rpmbuild.
def rpmbuild(config, name, options)
  arch = options.fetch('arch', 'x86_64')
  dist = options.fetch('dist', '.el7')
  rpm_file = "RPMS/#{arch}/#{name}-#{options['version']}#{dist}.#{arch}.rpm"
  autostart = options.fetch('autostart', ! File.exists?(rpm_file))

  config.vm.define name, autostart: autostart do |container|
    container.vm.synced_folder '.', '/vagrant', disabled: true
    container.vm.synced_folder 'RPMS', '/rpmbuild/RPMS'
    container.vm.synced_folder 'SPECS', '/rpmbuild/SPECS'
    container.vm.synced_folder 'SOURCES', '/rpmbuild/SOURCES'

    container.vm.provider :docker do |d|
      d.image = "hootenanny/#{options['image']}"
      d.create_args = options.fetch('create_args', ['-it', '--rm'])
      d.remains_running = options.fetch('remains_running', true)

      build_cmd = ['rpmbuild']

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
        build_cmd << '--define'
        build_cmd << "#{macro} #{expr}"
      end

      # Pass through any variables we want to undefine.
      options.fetch('undefines', []).each do |macro|
        build_cmd << '--undefine'
        build_cmd << macro
      end

      build_cmd << '-bb'
      build_cmd << "SPECS/#{name}.spec"
      d.cmd = build_cmd
    end
  end
end


def collect_rpms(images)
  collected = {}
  images.each do |image|
    $rpms.each do |name, options|
      if options.fetch('image', nil) == image
        collected[name] = options
      end
    end
  end
  return collected
end

## Vagrant configuration

Vagrant.configure(2) do |config|
  # Build base images and those needed for GDAL and NodeJS.
  $images['base'].each do |name, options|
    build_container(config, name, options)
  end

  # GDAL dependency RPMS need to be built first
  collect_rpms(
    ['rpmbuild-geos', 'rpmbuild-libgeotiff', 'rpmbuild-libkml']
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

  # Finally, finish with PostGIS, NodeJS and all of the other RPMs.
  collect_rpms(
    ['rpmbuild-generic', 'rpmbuild-nodejs', 'rpmbuild-postgis']
  ).each do |name, options|
    rpmbuild(config, name, options)
  end
end
