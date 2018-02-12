require 'yaml'

settings = YAML::load_file('config.yml')

base_images = settings.fetch('base_images', {})
rpms = settings.fetch('rpms', {})

packaging_home = File.realpath(File.dirname(__FILE__))

Vagrant.configure(2) do |config|
  base_images.each do |name, options|
    config.vm.define name do |container|
      container.vm.synced_folder '.', '/vagrant', disabled: true
      container.vm.provider :docker do |d|
        # On the containers we're building don't actually run anything.
        d.build_dir = options.fetch('build_dir', '.')
        d.cmd = options.fetch('cmd', [])

        # Start build arguments.
        build_args = []
        options.fetch('args', {}).each do |arg, value|
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

  generic_rpms = {}
  rpms.each do |name, options|
    if options.fetch('image', '') == 'rpmbuild-generic'
      generic_rpms[name] = options
    end
  end

  generic_rpms.each do |name, options|
    config.vm.define name, autostart: false do |container|
      container.vm.synced_folder '.', '/vagrant', disabled: true
      container.vm.synced_folder 'RPMS', '/rpmbuild/RPMS'
      container.vm.synced_folder 'SPECS', '/rpmbuild/SPECS'
      container.vm.synced_folder 'SOURCES', '/rpmbuild/SOURCES'

      container.vm.provider :docker do |d|
        d.image = "hootenanny/#{options['image']}"
        d.create_args = options.fetch('create_args', ['-it', '--rm'])
        d.remains_running = options.fetch('remains_running', true)

        build_cmd = ['rpmbuild']

        version, release = options['version'].split('-')
        d.env = options.fetch(
          'env', {
            'RPMBUILD_VERSION' => version,
            'RPMBUILD_RELEASE' => release,
          }
        )

        # Very difficult to pass in defines on CLI.
        #defines = options.fetch('defines', {})
        #defines.each do |macro, expr|
        #  build_cmd << "--define='#{macro} #{expr}'"
        #end

        options.fetch('undefines', []).each do |macro|
          build_cmd << '--undefine'
          build_cmd << macro
        end

        build_cmd << '-bb'
        build_cmd << "SPECS/#{name}.spec"
#        puts build_cmd
        d.cmd = build_cmd
      end
    end
  end
end
