# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "hoot/centos7-minimal"
  config.vm.hostname = "hoot-centos"
  config.vm.synced_folder ".", "/home/vagrant/hootenanny-rpms", type: "rsync"

  # Provider-specific configuration so you can fine-tune various
  config.vm.provider "virtualbox" do |vb|
      # Customize the amount of memory on the VM:
      vb.memory = 8192
      vb.cpus = 4
  end

  config.vm.provision "setup", type: "shell", :privileged => false, :path => "VagrantProvision.sh"
end

# Allow local overrides of vagrant settings
if File.exists?('VagrantfileLocal')
  load 'VagrantfileLocal'
else
  if File.exists?('VagrantfileLocal.vbox')
    load 'VagrantfileLocal.vbox'
  end
end
