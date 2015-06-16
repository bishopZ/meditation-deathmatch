$script = <<SCRIPT

## Sys Pre-Reqs
sudo apt-get install -y node npm python python-pip python-dev git liblo-dev python-numpy python-scipy python-pygame python-qt4 python-qt4-dev
sudo npm install express
sudo npm install socket.io@1
sudo npm install node-thinkgear
sudo pip install pyliblo gevent-socketio pyserial

## Python MindWave
sudo rm -rf python-mindwave
git clone https://github.com/akloster/python-mindwave
cd python-mindwave
git checkout -b old-python-mindwave ca054167ae
sudo python setup.py install

## MDM
sudo rm -rf meditation-deathmatch
git clone https://github.com/bishopZ/meditation-deathmatch.git

SCRIPT

Vagrant.configure("2") do |config|

  config.vm.define :ubuntu do |ubuntu|
    ubuntu.vm.box      = 'ubuntu-1410'
    ubuntu.vm.box_url  = 'https://cloud-images.ubuntu.com/vagrant/vivid/current/vivid-server-cloudimg-i386-vagrant-disk1.box'
  end

  config.ssh.forward_x11 = true

  config.vm.network :private_network, ip: '10.200.0.2'
  config.vm.network "forwarded_port", guest: 3101, host: 3101

  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--memory", 1024]
    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end

  config.vm.synced_folder "./", "/opt/mdm"

  config.vm.provision "shell", inline: $script
  
end
