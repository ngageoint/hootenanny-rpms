# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = 'hoot/centos7-minimal'
  config.vm.hostname = 'hoot-rpms'
  config.vm.synced_folder '.', '/home/vagrant/hootenanny-rpms'

  # Default to 8GB and 4CPUs to run Hootenanny.
  config.vm.provider :virtualbox do |vb|
    vb.memory = 8192
    vb.cpus = 4
  end
end
