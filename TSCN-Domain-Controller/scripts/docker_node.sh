#!/bin/bash

# Date : 13/7/16 PM4:44
# Author: 'liming'
# Email: liminghilton@gmail.com
# Copyright: TradeShift.com

# docker registry server
reg_addr=172.16.30.80:5000

# swarm-manager server
swarm_addr=172.16.30.80:19999

# consul-server
consul_addr=172.16.30.80:8500

# private interface
priv_if=eth0

priv_ip=`ifconfig eth0|grep 'inet addr'|sed -e 's/^.*inet addr://;s/  Bcast.*$//'`

if [ x"$priv_ip" == "x" ]
	then
	echo "Private ip is not found !!!!!!!!!!!!!!"
	exit 9
fi

# locale
cat > /var/lib/locales/supported.d/local << EOF
zh_CN GB2312
en_US.UTF-8 UTF-8
zh_CN.GBK GBK
zh_CN.UTF-8 UTF-8
EOF

locale-gen

# cat > /etc/default/locale <<EOF
# LANG=en_US.utf8
# LANGUAGE=en_US.utf8
# LC_TIME=en_US.utf8
# LC_CTYPE=en_US.utf8
# LC_ALL=zh_CN.utf8
# EOF

# echo "export LC_ALL=zh_CN.utf8" >> /etc/profile
# export LC_ALL=zh_CN.utf8

cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

echo "10000 61000" > /proc/sys/net/ipv4/ip_local_port_range
cat >> /etc/sysctl.conf << EOF
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_timestamps = 1
net.ipv4.tcp_fin_timeout = 10
#net.ipv4.tcp_max_tw_buckets = 16384
# for redis
#vm.overcommit_memory = 1
vm.swappiness = 10
net.ipv4.ip_forward = 1
EOF

sysctl -p /etc/sysctl.conf


# limit config
echo "* - nofile 655350" >> /etc/security/limits.conf
echo "session required pam_limits.so" >> /etc/pam.d/common-session
echo "ulimit -SHn 655350" >> /etc/profile

# ssh
mkdir /root/.ssh
cat > /root/.ssh/authorized_keys << EOF
# liming
ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAvNFKgo9vmcy9AfdfLA8I/kRglcQPfcgC/hTapxoq2Y+/u9b0b/L2TBQkdWvTljBLkD/g213PuU1UdfrM26Kv22LByM3r1GhBujpjyynJT6hTh4UAU8tVBrB3LQXPGAWdKJLTWxIBnLv3bfXIQtJ76DXU3ThCSm+AoCvgPRoc/TUoxqtM/LjB+f4RuKeIcf2cW0/L6ZVjdPzY1hQP6XkZvS/UuTUkPOOuKZk7x1fp+iK4eXqkKvmE9VvBOTUOOB4AOvIRbvQ1g5wgrg0tgi/iYp/XPzjvJdnNL0KQfMDqj0cu2EcIhMcz0Cj9L4TgspxTxTXn6dxaaD/pIt2ynW7uuw== liming
# surry
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDM5jnETFXw7h7SUfKHqwNF++PWcuqNgj1s3W4NFh9kQm/H8ckFzDG17VTQW/Ha3ye1Go5yL88mLW5rx2YQsuEHTjp8pXHe2fKzMyeFbYmNpErVUkMKpQJA5NjzYpAwmRfUK1LJepAP2WhacmamUL7J8uWMcBaNRTp10D/MoAoBgC26poudisSBV7k0j6YQb40zn048kH51y7oK3NJcU0nRb/UXJ2HNqYI29iV0UBCbQWXxDRTaFZ1TOyl10u8UtbFg9O3aO2HyMF5FGBOZEzSeWRdj8MTTQiy5pVz5G0ky55H7mlZW8lIr+OC/5Hf8QEjryhccDu24WnoAKd7iUx3/ SunrryCao@caoyuans-MacBook-Pro.local
# dhy

EOF

cat > /etc/ssh/sshd_config << EOF
Port 22
Protocol 2
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_dsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key
UsePrivilegeSeparation yes
KeyRegenerationInterval 3600
ServerKeyBits 1024
SyslogFacility AUTH
LogLevel INFO
LoginGraceTime 120
PermitRootLogin without-password
StrictModes yes
RSAAuthentication yes
PubkeyAuthentication yes
PasswordAuthentication no
IgnoreRhosts yes
RhostsRSAAuthentication no
HostbasedAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no
X11Forwarding yes
X11DisplayOffset 10
PrintMotd no
PrintLastLog yes
TCPKeepAlive yes
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server
UsePAM yes
UseDNS no
EOF

service ssh restart

# apt source
cat > /etc/apt/sources.list << EOF
deb http://mirrors.aliyun.com/ubuntu/ trusty main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-backports main restricted universe multiverse
EOF

apt-get update


# fw
ufw disable
iptables -F
iptables -t nat -F
iptables -t mangle -F

# disable auto upgrade
# /usr/bin/python3 /usr/lib/ubuntu-release-upgrader/check-new-release -q

# install docker engine
curl https://get.docker.com/ | /bin/bash

# customize docker engine
mkdir -p /opt/docker

cat > /etc/default/docker << EOF
DOCKER_OPTS="-H unix:///var/run/docker.sock -H tcp://0.0.0.0:2375 --insecure-registry $reg_addr --graph=/opt/docker"
EOF

service docker restart


# start node app
docker run --restart=always -d --name swarm-agent $reg_addr/swarm join --addr=$priv_ip:2375 consul://$consul_addr
docker run --restart=always -d \
-v /var/run/docker.sock:/tmp/docker.sock \
--name bwts-registrator -h bwts-registrator \
$reg_addr/registrator:latest -ip="$priv_ip" consul://$consul_addr


