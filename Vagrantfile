# -*- mode: ruby -*-
# vi: set ft=ruby :

$provisionSh = <<-SHELL
    ln -s hootenanny-rpms/src/ rpmbuild

    if ! yum list installed | grep --quiet epel-release.noarch ; then
        echo "### Installing epel repo"
        sudo yum -y install epel-release
    fi

    # Try the update a few times. Sometimes the epel repo gives an error.
    sudo yum -y -q update || true
    sudo yum -y -q update || true
    sudo yum -y -q upgrade

    # Enable NTP to synchronize clock
    echo "### Setup NTP..."
    sudo yum -q -y install ntp
    sudo chkconfig ntpd on
    #TODO: Better way to do this?
    sudo systemctl stop ntpd
    sudo ntpd -gq
    sudo systemctl start ntpd

SHELL

Vagrant.configure(2) do |config|
  config.vm.provision "shell", inline: $provisionSh
end

# Allow local overrides of vagrant settings
if File.exists?('VagrantfileLocal')
  load 'VagrantfileLocal'
else
  load 'VagrantfileLocal.vbox'
end
