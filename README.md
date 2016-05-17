App client per a rasp.cat
=========================

Client python pel servei [rasp.cat](http://www.rasp.cat)

### Passes:

* Instal·lar sistema operatiu ( ex: Raspbian )
* Instal·lar requeriments: sudo apt-get install xwit chromium x11-xserver-utils ttf-mscorefonts-installer
* Descarregar script i configurar-lo per tal que s'executin a l'inici.

Necessites ajuda? info@rasp.cat

```bash
 wget -qO - http://bintray.com/user/downloadSubjectPublicKey?username=bintray | sudo apt-key add -
 echo "deb http://dl.bintray.com/kusti8/chromium-rpi jessie main" | sudo tee -a /etc/apt/sources.list
 wget -qO- https://raw.githubusercontent.com/raspcat/raspcatclient/master/download.sh | bash

```


