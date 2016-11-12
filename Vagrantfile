$script = <<SCRIPT

## To run the stages you will also want to put your user account in the dialup group

## Additional libraries for muse sdk
## http://www.atlantsembedded.com/b/getting-muse-sdk-work-linux
## ftp://sccn.ucsd.edu/pub/software/LSL/SDK/liblsl-C-C++-1.11.zip
# libbluetooth3-dev:i386 libstdc++6:i386 liblo7:i386

## gevent problems ---
# may need to
# easy_install -U gevent==1.1b4


## Sys Pre-Reqs
sudo apt-get install -y python python-pip python-dev git liblo-dev python-numpy python-scipy python-pygame python-qt4 python-qt4-dev cython lib32ncurses5
sudo pip install pyliblo gevent-socketio pyserial gipc

## MDM
sudo rm -rf meditation-deathmatch
git clone https://github.com/bishopZ/meditation-deathmatch
touch pull-done

SCRIPT


Vagrant.configure("2") do |config|

  config.vm.define :ubuntu do |ubuntu|
    ubuntu.vm.box      = 'ubuntu-1604'
    ubuntu.vm.box_url  = 'https://cloud-images.ubuntu.com/vagrant/xenial/current/xenial-server-cloudimg-amd64-vagrant-disk1.box'
  end

  config.vm.network :private_network, ip: '10.200.0.2'
  config.vm.network "forwarded_port", guest: 3101, host: 3101

  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--memory", 1024]
    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end

  config.vm.provision "shell", inline: $script
  
end
