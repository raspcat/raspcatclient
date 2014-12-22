cd ~
wget -O r.zip https://github.com/raspcat/raspcatclient/archive/master.zip
unzip -x r.zip 
mv raspcatclient-master raspcatclient
chmod 755 raspcatclient/raspcatclient.py 
rm r.zip
