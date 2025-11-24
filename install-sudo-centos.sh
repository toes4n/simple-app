#!/bin/bash

# Switch to root user (only relevant if running script interactively)
# Uncomment if you want the script to stop and open an interactive root shell
# sudo -i

# Update all packages
sudo yum update -y

# Install Development Tools group and required packages
sudo yum groupinstall "Development Tools" -y
sudo yum install gcc gcc-c++ make pam-devel openssl-devel -y

# Go to /tmp directory
cd /tmp || exit 1

# Download sudo 1.9.17p2 source tarball
wget https://www.sudo.ws/dist/sudo-1.9.17p2.tar.gz

# Extract the tarball
tar -xzvf sudo-1.9.17p2.tar.gz

cd sudo-1.9.17p2 || exit 1

# Configure, build, and install sudo from source
./configure
make
sudo make install

# Backup old sudo binary and replace it with the new one
sudo mv /usr/bin/sudo /usr/bin/sudo.old
sudo ln -sf /usr/local/bin/sudo /usr/bin/sudo

# Verify sudo version
sudo -V
