#!/bin/bash
yum \-y install python3
sudo su \- tcl \-c "pip3 install --user telethon"
sudo su \- tcl \-c "pip3 install --user peewee"
sudo su \- tcl \-c "pip3 install --user PyJWT"
sudo su \- tcl \-c "pip3 install --user flask"
sudo su \- tcl \-c "pip3 install --user psycopg2-binary"
sudo su \- tcl \-c "pip3 install --user -U flask-cors"
yum \-y install git
cd /opt
git clone https://github.com/gerladeno/telega.git
mv telega tcl
yum \-y install vim
echo "[Unit]
Description=Telegram Chat Listener
After=syslog.target network.target
 
[Service]
Environment=LOCATION=/opt/tcl/
User=tcl
LimitNOFILE=102642
OOMScoreAdjust=-1000
PIDFile=/var/run/tcl/tcl.pid
ExecStart=/opt/tcl/start.sh \$LOCATION
#StandardOutput=null
 
[Install]
WantedBy=multi-user.target" > /etc/systemd/system/tcl.service
chmod \+x /opt/tcl/start.sh
systemctl enable tcl.service
echo "[Unit]
Description=Telegram Chat Listener Front
After=syslog.target network.target

[Service]
Environment=LOCATION=/opt/tcl/
User=tcl
LimitNOFILE=102642
OOMScoreAdjust=-1000
PIDFile=/var/run/tcl/tclweb.pid
ExecStart=/opt/tcl/front.sh \$LOCATION
#StandardOutput=null

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/tclweb.service
chmod \+x /opt/tcl/front.sh
systemctl enable tclweb.service
useradd tcl
passwd \-l tcl
chown \-R tcl:tcl /opt/tcl
echo "Don't forget config.ini and phone/code activation"
