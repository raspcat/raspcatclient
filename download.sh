#wget -o /dev/null -O - https://raw.githubusercontent.com/raspcat/raspcatclient/master/download.sh | bash
yes | sudo apt-get update
yes | sudo apt-get install chromium x11-xserver-utils ttf-mscorefonts-installer
cd ~
wget -O r.zip https://github.com/raspcat/raspcatclient/archive/master.zip
unzip -o -x r.zip 
mv raspcatclient-master raspcatclient
chmod 755 raspcatclient/raspcatclient.py 
nohup raspcatclient/raspcatclient.py
rm r.zip
wget -o /dev/null -O raspcatclient/rasp_black_80.png http://rasp.cat/site-css/pictures/rasp_black_80.png
