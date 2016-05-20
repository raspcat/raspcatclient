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
        browser_command = """
            /usr/bin/chromium-browser 
                 --disable-threaded-gpu-rasterization --disable-quic --disable-gpu --disable-display-list-2d-canvas --disable-new-avatar-menu --disable-3d-apis --disable-about-in-settings --disable-accelerated-2d-canvas --disable-accelerated-jpeg-decoding --disable-accelerated-video-decode --disable-account-consistency --disable-affiliation-based-matching --disable-answers-in-suggest --disable-app-list-dismiss-on-blur --disable-async-dns --disable-background-networking --disable-backing-store-limit --disable-blink-features --disable-blink-scheduler --disable-boot-animation --disable-breakpad --disable-bundled-ppapi-flash --disable-canvas-aa --disable-cast --disable-cast-streaming-hw-encoding --disable-click-delay --disable-client-side-phishing-detection --disable-cloud-import --disable-component-cloud-policy --disable-component-extensions-with-background-pages --disable-component-update --disable-composited-antialiasing --disable-confirmation --disable-contextual-search --disable-core-animation-plugins --disable-credit-card-scan --disable-d3d11 --disable-databases --disable-default-apps --disable-delegated-renderer --disable-demo-mode --disable-device-disabling --disable-device-discovery-notifications --disable-direct-npapi-requests --disable-direct-write --disable-directwrite-for-ui --disable-display-color-calibration --disable-display-list-2d-canvas --disable-distance-field-text --disable-domain-reliability --disable-drive-apps-in-app-list --disable-drop-sync-credential --disable-dwm-composition --disable-easy-unlock --disable-encrypted-media --disable-experimental-app-list --disable-experimental-hotwording --disable-extensions --disable-extensions-file-access-check --disable-extensions-http-throttling --disable-file-system --disable-fill-on-account-select --disable-flash-3d --disable-flash-stage3d --disable-gaia-services --disable-gesture-requirement-for-media-playback --disable-gl-drawing-for-tests --disable-gl-error-limit --disable-glsl-translator --disable-gpu --disable-gpu-compositing --disable-gpu-driver-bug-workarounds --disable-gpu-program-cache --disable-gpu-rasterization --disable-gpu-sandbox --disable-gpu-shader-disk-cache --disable-gpu-vsync --disable-gpu-watchdog --disable-hang-monitor --disable-hid-detection-on-oobe --disable-histogram-customizer --disable-hosted-app-shim-creation --disable-impl-side-painting --disable-infobar-for-protected-media-identifier --disable-infobars --disable-input-view --disable-ipv4 --disable-ipv6 --disable-java --disable-javascript-harmony-shipping --disable-kill-after-bad-ipc --disable-lcd-text --disable-legacy-window --disable-local-storage --disable-logging --disable-login-animations --disable-login-scroll-into-view --disable-low-end-device-mode --disable-low-res-tiling --disable-main-frame-before-activation --disable-manager-for-sync-signin --disable-media-source --disable-memory-pressure-chromeos --disable-method-check --disable-minimize-on-second-launcher-item-click --disable-mojo-channel --disable-namespace-sandbox --disable-network-portal-notification --disable-new-avatar-menu --disable-new-bookmark-apps --disable-new-channel-switcher-ui --disable-new-kiosk-ui --disable-new-offline-error-page --disable-new-profile-management --disable-new-zip-unpacker --disable-notifications --disable-ntp-other-sessions-menu --disable-office-editing-component-extension --disable-offline-auto-reload --disable-offline-auto-reload-visible-only --disable-offline-load-stale-cache --disable-one-copy --disable-out-of-process-pdf --disable-overlay-scrollbar --disable-overscroll-edge-effect --disable-panel-fitting --disable-password-generation --disable-password-link --disable-password-manager-reauthentication --disable-pdf-material-ui --disable-pepper-3d --disable-permissions-bubbles --disable-physical-keyboard-autocorrect --disable-pinch --disable-pinch-virtual-viewport --disable-plugins-discovery --disable-pnacl-crash-throttling --disable-policy-key-verification --disable-popup-blocking --disable-preconnect --disable-prefer-compositing-to-lcd-text --disable-prefixed-encrypted-media --disable-prerender-local-predictor --disable-print-preview --disable-prompt-on-repost --disable-pull-to-refresh-effect --disable-quic --disable-quic-pacing --disable-quic-port-selection --disable-reading-from-canvas --disable-remote-core-animation --disable-remote-fonts --disable-renderer-accessibility --disable-roboto-font-ui --disable-rollback-option --disable-save-password-bubble --disable-seccomp-filter-sandbox --disable-session-crashed-bubble --disable-settings-window --disable-setuid-sandbox --disable-shader-name-hashing --disable-shared-workers --disable-signin-scoped-device-id --disable-single-click-autofill --disable-single-thread-proxy-scheduler --disable-smart-virtual-keyboard --disable-smooth-scrolling --disable-software-rasterizer --disable-spdy-proxy-dev-auth-origin --disable-suggestions-service --disable-supervised-user-blacklist --disable-supervised-user-safesites --disable-surfaces --disable-svg1dom --disable-sync --disable-sync-app-list --disable-sync-backup --disable-sync-rollback --disable-sync-types --disable-synctypes --disable-system-fullscreen-for-testing --disable-text-blobs --disable-text-input-focus-manager --disable-threaded-animation --disable-threaded-compositing --disable-threaded-gpu-rasterization --disable-threaded-scrolling --disable-timezone-tracking-option --disable-touch-adjustment --disable-touch-drag-drop --disable-touch-editing --disable-touch-feedback --disable-translate --disable-v8-idle-tasks --disable-vaapi-accelerated-video-encode --disable-views-rect-based-targeting --disable-virtual-keyboard-overscroll --disable-voice-input --disable-volume-adjust-sound --disable-wake-on-wifi --disable-web-resources --disable-web-security --disable-webaudio --disable-webgl --disable-webrtc --disable-webrtc-encryption --disable-webrtc-hw-decoding --disable-webrtc-hw-encoding --disable-win32k-renderer-lockdown --disable-x-token --disable-zero-browsers-open-for-tests --disable-zero-suggest --disable-impl-side-painting            
                 --user-data-dir={profile_dir} --kiosk  %s 
            """.format(  profile_dir = PROFILE_DIR ).replace( '\n', '' )
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
        #response = urllib2.urlopen(self.source)
        #url_new = response.read()        
        url_new = ""
        url_old = ""
        i = 100
        while True:            
            if self.finalitzar:
                return            
            if i >= 20:  
                hi_ha_error = False
                try:
                    response = urllib2.urlopen(self.source)
                    self.entryXarxaVarOK.configure(bg = 'green')
                    url_new = response.read()
                except urllib2.HTTPError:
                    hi_ha_error = True
                except urllib2.URLError:
                    hi_ha_error = True
                except urllib2.HTTPException:
                    hi_ha_error = True
                except Exception:
                    hi_ha_error = True
                if hi_ha_error:
                    self.entryXarxaVarOK.configure(bg = 'yellow')
                i=0
            if url_old != url_new or self.force_restart_browse:         
                self.force_restart_browse = False
                self.stop_browsers( ) 
                self.start_browser( url_new )  
                url_old = url_new
            i+=1  
            time.sleep(1)
            
    def start_browser(self, url ):
        exited_cleanly = """
            if [ -f {profile_dir}/Default/Preferences ]; then
               sed -i 's/exited_cleanly\":\ false/exited_cleanly\":\ true/g' {profile_dir}/Default/Preferences;
            fi;
            """.format(  profile_dir = PROFILE_DIR )
        os.system( exited_cleanly )
        t = threading.Thread(target=self.wb.open, args=( url, ))
        t.daemon = True
        t.start()                    

    def stop_browsers(self):
        os.system("killall chromium-browser")
        time.sleep(1)
        os.system("killall -9 chromium-browser")
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
    
    
    
    
