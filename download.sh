#wget -o /dev/null -O - https://raw.githubusercontent.com/raspcat/raspcatclient/master/download.sh | bash
cd ~
wget -O r.zip https://github.com/raspcat/raspcatclient/archive/master.zip
if [[ $? -eq 0 ]]; then
        echo "Descarregat. Instal·lant ..."
else
        echo "No es pot baixar en aquest moment, comprova connexió"
        exit 1
fi
if [[ -d raspcatclient ]]; then
        mv raspcatclient raspcatclient-master
fi
unzip -o -x r.zip 
mv raspcatclient-master raspcatclient
chmod 755 raspcatclient/raspcatclient.py 
rm r.zip
wget -o /dev/null -O raspcatclient/rasp_black_80.png http://rasp.cat/site-css/pictures/rasp_black_80.png
yes | sudo apt-get update
yes | sudo apt-get install chromium x11-xserver-utils ttf-mscorefonts-installer
#nohup raspcatclient/raspcatclient.py
