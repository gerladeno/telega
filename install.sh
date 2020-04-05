#!/bin/bash
yum \-y install python3
pip3 install --user telethon
pip3 install --user peewee
pip3 install --user PyJWT
pip3 install --user flask
pip3 install --user psycopg2-binary
pip3 install --user -U flask-cors
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
useradd tcl
passwd \-l tcl
chown \-R tcl:tcl /opt/tcl
firewall-cmd \--zone=public \--permanent \--add-port=5000/tcp
firewall-cmd \--permanent \--zone=public \--add-service=http
firewall-cmd \--reload
echo "Don't forget config.ini and phone/code activation"
