# Script to update and setup raspberry
# pi environment for server deployment

# Setting up nginx, it starts automatically
sudo apt-get update
sudo apt-get install nginx --fix-missing
sudo apt-get install nginx

# Setting up virtualenv
sudo apt-get install python3-pip
pip3 install virtualenv

# Adding virtualenv to PATH
echo export PATH='$PATH':'"/home/pi/.local/bin"' >> ~/.bashrc
source ~/.bashrc


