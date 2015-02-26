```
Install GCC:
[root@newinstance ~]# yum groupinstall "Development Tools"
[root@newinstance ~]# yum install kernel-devel kernel-headers

[root@newinstance installables]# ll
total 98804
-rw-r--r-- 1 222 500  5439122 Feb 25 17:00 apache-maven-3.1.0-bin.tar.gz
-rw-r--r-- 1 222 500    78316 Feb 25 17:00 htop-0.9-1.el6.rf.x86_64.rpm
-rw-r--r-- 1 222 500 85414670 Feb 25 17:00 jdk-7u25-linux-x64.rpm
-rw-r--r-- 1 222 500  9021839 Feb 25 17:00 jetty-distribution-9.0.4.v20130625.tar.gz
-rw-r--r-- 1 222 500   850772 Feb 25 17:00 libevent-2.0.21-stable.tar.gz

Install JVM
[root@newinstance installables]# rpm -ivh jdk-7u25-linux-x64.rpm

Verify JVM version:
[root@newinstance installables]# java -version
java version "1.7.0_25"
Java(TM) SE Runtime Environment (build 1.7.0_25-b15)
Java HotSpot(TM) 64-Bit Server VM (build 23.25-b01, mixed mode)

Set JAVA_HOME and add to PATH in ~/.bashrc:
export JAVA_HOME=/usr/java/latest
export PATH=$PATH:$JAVA_HOME/bin

Install Maven:
[root@newinstance installables]# tar -zxvf apache-maven-3.1.0-bin.tar.gz
[root@newinstance installables]# mv apache-maven-3.1.0 /opt/.
[root@newinstance installables]# cd /opt/
[root@newinstance opt]# ln -s apache-maven-3.1.0 maven

Set M2_HOME and PATH in ~/.bashrc:
export M2_HOME=/opt/maven
export PATH=$PATH:$JAVA_HOME/bin:$M2_HOME/bin

Install JETTY:
[root@newinstance installables]# tar -zxvf jetty-distribution-9.0.4.v20130625.tar.gz
[root@newinstance installables]# mv jetty-distribution-9.0.4.v20130625 /opt/.
[root@newinstance installables]# cd /opt/
[root@newinstance opt]# cp -r jetty-distribution-9.0.4.v20130625/ jetty1
[root@newinstance opt]# cp -r jetty-distribution-9.0.4.v20130625/ jetty2

Install Libevent:
[root@newinstance installables]# tar -zxvf libevent-2.0.21-stable.tar.gz
[root@newinstance installables]# cd libevent-2.0.21-stable
[root@newinstance libevent-2.0.21-stable]# ./configure
[root@newinstance libevent-2.0.21-stable]# make && make install

Install Memcached:
[root@newinstance installables]# yum install memcached

Install HTOP:
[root@newinstance installables]# rpm -ivh htop-0.9-1.el6.rf.x86_64.rpm


Optimize the instance:
Increase TCP Buffer size:
sysctl -w net.core.rmem_max=16777216
sysctl -w net.core.wmem_max=16777216
sysctl -w net.ipv4.tcp_rmem="4096 87380 16777216"
sysctl -w net.ipv4.tcp_wmem="4096 16384 16777216"

Queue size:
sysctl -w net.core.somaxconn=4096
sysctl -w net.core.netdev_max_backlog=16384
sysctl -w net.ipv4.tcp_max_syn_backlog=8192
sysctl -w net.ipv4.tcp_syncookies=1

Ports:
sysctl -w net.ipv4.ip_local_port_range="1024 65535"
sysctl -w net.ipv4.tcp_tw_recycle=1

Max-files:
sysctl -w fs.file-max=300000

File Descriptors:
Add the below in /etc/security/limits.conf
root		soft nofile	128000
root		hard nofile	128000
nobody		soft nofile	128000
nobody		hard nofile	128000
root		soft nproc	128000
root		hard nproc	128000
nobody		soft nproc	128000
nobody		hard nproc	128000


Start the services:
Start Memcached:
memcached -d -p 11211 -u nobody -m 1024 -c 262144 -P /var/run/memcached/memcached1.pid -l localhost
memcached -d -p 11212 -u nobody -m 1024 -c 262144 -P /var/run/memcached/memcached2.pid -l localhost


Start JETTY:
/usr/java/latest/bin/java -Djetty.state=/opt/Jetty1/Jetty1.state -server -Xms4096m -Xmx4096m -XX:+DisableExplicitGC -Djetty.logs=/opt/Jetty1/logs -Djetty.home=/opt/Jetty1 -Djava.io.tmpdir=/tmp -jar /opt/Jetty1/start.jar jetty.port=8080 jetty.https.port=8443 etc/jetty-logging.xml etc/jetty-started.xml --daemon &

/usr/java/latest/bin/java -Djetty.state=/opt/Jetty2/Jetty2.state -server -Xms4096m -Xmx4096m -XX:+DisableExplicitGC -Djetty.logs=/opt/Jetty2/logs -Djetty.home=/opt/Jetty2 -Djava.io.tmpdir=/tmp -jar /opt/Jetty2/start.jar jetty.port=8090 jetty.https.port=8543 etc/jetty-logging.xml etc/jetty-started.xml --daemon &
```
