#!/usr/bin/python2.7
# coding: utf-8

import threading
import webbrowser
import Tkinter as TK
import os
import urllib2
import time
#from uuid import getnode as get_mac
from uuid import uuid4

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join( BASE_DIR, 'myconfig.txt')
PROFILE_DIR = os.path.join( BASE_DIR, 'profile_dir')


#http://sebsauvage.net/python/gui/

class grabboot(TK.Tk):
    
    def __init__(self,parent):
        TK.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

        #controla si cal finalitzar els threads oberts
        self.finalitzar = False
        
        #browser
        browser_command = '/usr/bin/chromium --user-data-dir={profile_dir} --kiosk  %s '.format(  profile_dir = PROFILE_DIR )
        self.wb = webbrowser.get(browser_command)
        
        #diccionari de settings
        self.settings = {}
        
        #la meva mac
        #self.mac = ':'.join(("%012X" % get_mac() )[i:i+2]  for i in range(0, 12, 2))
        
        #defaultMasterKey
        self.defaultMasterKey = "00000000000000000000"
        
        #carregar el fitxer de configuració
        self.read_config_file()
        
        #indica si cal re-engegar els navegadors
        self.force_restart_browse = True
        
        #thread que gestiona els navegadors:
        self.monitorthread = None
        
        #TODO: Prevenir blank screen
        #http://raspberrypi.stackexchange.com/questions/752/how-do-i-prevent-the-screen-from-going-blank
        #ó: /etc/kbd/config
        #BLANK_TIME=0
        #BLANK_DPMS=off
        #POWERDOWN_TIME=0
                
        #si tenim masterkey comencem
        if self.masterkey != self.defaultMasterKey:
            self.run_button(3)

    def initialize(self):
        self.grid()

        #------------- Fitxer de Configuració -----------------
        row = 0
        self.labelConfig = TK.StringVar(value=u"Configuració del dispositiu")
        l = TK.Label(self,textvariable=self.labelConfig,anchor="w",relief=TK.FLAT,)
        l.grid(column=0,row=row,sticky='EW' ,pady=(10,10) ,padx=(10,10))

        #--
        button = TK.Button(self,text=u"Obra fitxer de configuració del dispositiu", height=1,
                                command=self.open_config_file )
        button.grid(column=1,row=row, sticky='EW', padx=(10,10))

        #--
        self.entryConfigVarOK = TK.Label(bg='green', relief=TK.SUNKEN,width=5)
        self.entryConfigVarOK.grid(row=row,column=3,pady=(10,10) ,padx=(10,10))
        
        #-------------- Configuració de Xarxa -------------
        
        row += 1
        self.labelXarxa = TK.StringVar(value=u"Configuració Wifi")
        l = TK.Label(self,textvariable=self.labelXarxa,anchor="w",relief=TK.FLAT,)
        l.grid(column=0,row=row,sticky='EW' ,pady=(10,10) ,padx=(10,10))

        #--
        button = TK.Button(self,text=u"Configuració Wifi", height=1,
                                command=self.open_wifi_config )
        button.grid(column=1,row=row, sticky='EW', padx=(10,10))

        #--
        self.entryXarxaVarOK = TK.Label(bg='green', relief=TK.SUNKEN,width=5)
        self.entryXarxaVarOK.grid(row=row,column=3,pady=(10,10) ,padx=(10,10))

        #-------------- Modes del monitor -------------
        row += 1
        self.labelMonitor = TK.StringVar(value=u"Configuració Monitor")
        l = TK.Label(self,textvariable=self.labelMonitor,anchor="w",relief=TK.FLAT,)
        l.grid(column=0,row=row,sticky='EW' ,pady=(10,10) ,padx=(10,10))

        #--
        button = TK.Button(self,text=u"Modes Monitor", height=1,
                                command=self.open_show_monitor )
        button.grid(column=1,row=row, sticky='EW', padx=(10,10))

        #--
        self.entryMonitorVarOK = TK.Label(bg='green', relief=TK.SUNKEN,width=5)
        self.entryMonitorVarOK.grid(row=row,column=3,pady=(10,10) ,padx=(10,10))


        #-------------- Els meu config -------------
        row += 1
        self.labelMyConfig = TK.StringVar(value=u"Configuració programa")
        l = TK.Label(self,textvariable=self.labelMyConfig,anchor="w",relief=TK.FLAT,)
        l.grid(column=0,row=row,sticky='EW' ,pady=(10,10) ,padx=(10,10))

        #--
        button = TK.Button(self,text=u"Configuració del programa", height=1,
                                command=self.open_myconfig_file )
        button.grid(column=1,row=row, sticky='EW', padx=(10,10))

        #--
        self.entryMyConfigVarOK = TK.Label(bg='green', relief=TK.SUNKEN,width=5)
        self.entryMyConfigVarOK.grid(row=row,column=3,pady=(10,10) ,padx=(10,10))

        #-------------- Run -------------
        row += 1
        self.labelGo = TK.StringVar(value=u"Run!")
        l = TK.Label(self,textvariable=self.labelGo,anchor="w",relief=TK.FLAT,)
        l.grid(column=0,row=row,sticky='EW' ,pady=(10,10) ,padx=(10,10))

        #--
        button = TK.Button(self,text=u"Run!", height=1,
                                command=self.run_button )
        button.grid(column=1,row=row, sticky='EW', padx=(10,10))

        #--
        self.entryGoOK = TK.Label(bg='green', relief=TK.SUNKEN,width=5)
        self.entryGoOK.grid(row=row,column=3,pady=(10,10) ,padx=(10,10))

        #----------------------------------------------
        #self.grid_columnconfigure(0,weight=1)
        self.resizable( True,False)
        self.update()
        self.geometry(self.geometry())       
        #self.entryRootUser.focus_set()
        #self.entryRootUser.selection_range(0, TK.END)

    #--------------------------------------------------------------------------------------------------

    def run_button(self, espera=0):
        self.force_restart_browse = True
        if self.monitorthread is None:         
            self.monitorthread = threading.Thread(target=self.monitoreja, args=( espera, ) )
            self.monitorthread.start()
    
    def monitoreja(self, espera):
        no_apaguis_pantalla = """
            xset s off   
            xset -dpms   
            xset s noblank 
            xwit -root -warp 4000 4000
            """
        os.system( no_apaguis_pantalla )
        time.sleep(espera)
        self.read_config_file()
        response = urllib2.urlopen(self.source)
        url_new = response.read()        
        url_old = ""
        i = 0
        while True:            
            if self.finalitzar:
                return            
            if url_old != url_new or self.force_restart_browse:         
                self.stop_browsers( ) 
                self.start_browser( url_new )  
                url_old = url_new
                self.force_restart_browse = False
            if i >= 20:  
                response = urllib2.urlopen(self.source)
                url_new = response.read()
                i=0
            i+=1  
            time.sleep(1)
            
    def start_browser(self, url ):
        t = threading.Thread(target=self.wb.open, args=( url, ))
        t.daemon = True
        t.start()                    

    def stop_browsers(self):
        os.system("killall chromium")
        time.sleep(1)
        os.system("killall -9 chromium")
        time.sleep(1)
        
    #------------------------------------------------------------------------------

    def os_thread(self, txtcommand):
        t = threading.Thread(target=os.system, args=( txtcommand, ))
        t.daemon = True
        t.start()   
        
    def open_config_file(self):
        self.os_thread( "gksu leafpad /boot/config.txt" )
        
    def open_wifi_config(self):
        self.os_thread("wpa_gui")

    def open_show_monitor(self):
        comandes = """
        tvservice -s > /tmp/monitor.txt ;
        tvservice -m CEA  >> /tmp/monitor.txt;
        tvservice -m DMT >> /tmp/monitor.txt;
        """
        os.system(comandes)
        self.os_thread("leafpad /tmp/monitor.txt")

    def open_myconfig_file(self):        
        self.os_thread('leafpad "{config_file}"'.format(config_file=CONFIG_FILE))
        
    #------------------------------------------------------------------------------

    def read_config_file(self):
        
        desa_settings = False
        f = open (CONFIG_FILE, "a+")
        f.seek(0)
        data=f.read().split('\n')
        f.close()
        validlines = [ l.replace(u" ","") for l in data if l and not l.startswith("#") and not l.startswith(" ") and "=" in l ]
        for l in validlines:
            parell = l.split("=")
            self.settings[parell[0]]=parell[1]
            
        if 'masterkey' not in self.settings:
            desa_settings = True
            self.settings['masterkey']=self.defaultMasterKey
            
        if 'deviceid' not in self.settings:
            desa_settings = True
            self.settings['deviceid']=str( uuid4() ).split("-")[-1]   #12 caracters
            
        self.masterkey = self.settings.get("masterkey","00000000000000000000")
        self.deviceid = self.settings['deviceid']
        self.source = "https://rasp.cat/giveme/{version}/{deviceid}/{masterkey}".format(version = 1, deviceid= self.deviceid, masterkey = self.masterkey)
        
        #deso el fitxer:
        if desa_settings:
            contingut_txt = u"\n".join( [ u"{0}={1}".format( s, self.settings[s]  ) for s in self.settings  ]  )
            f = open (CONFIG_FILE, "w")
            f.write( contingut_txt )
            f.close()        
        

    #------------------------------------------------------------------------------
    
    def on_delete(self):
        print "sortint ..."
        self.stop_browsers()
        self.finalitzar = True
        self.destroy()
        
if __name__ == "__main__":
    app = grabboot(None)
    app.title('raspCat engine')
    app.wm_protocol ("WM_DELETE_WINDOW", app.on_delete)
    app.mainloop()
    
    
    
    
