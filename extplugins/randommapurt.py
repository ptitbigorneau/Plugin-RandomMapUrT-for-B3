# RandomMapUrT Plugin

__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '1.2'

import b3
import b3.plugin
import b3.events
import random
import time, threading, thread

def fexist(fichier):
    
    try:
    
        file(fichier)
     
        return True
   
    except:
  
        return False 

class RandommapurtPlugin(b3.plugin.Plugin):
    
    _adminPlugin = None
    _adminlevel = 100
    _shufflemaplevel = 60
    _shufflemapcycle = "off"
    _rmonoff = "on"
    _test = None
    _listmap = []
    _listmapsplayed = []
    _comptemaps = 1

    def onStartup(self):

        self._adminPlugin = self.console.getPlugin('admin')
        
        if not self._adminPlugin:

            self.error('Could not find admin plugin')
            return False
        
        self.registerEvent(b3.events.EVT_GAME_MAP_CHANGE)

        self._adminPlugin.registerCommand(self, 'randommap',self._adminlevel, self.cmd_randommap)
        self._adminPlugin.registerCommand(self, 'shufflemapcycle',self._adminlevel, self.cmd_shufflemapcycle)
        self._adminPlugin.registerCommand(self, 'shufflemaps',self._shufflemaplevel, self.cmd_shufflemaps)
        
        self._listmapsplayed.append(self.console.game.mapName)

        self.listemaps()

        if self._shufflemapcycle == "off":

            if self.nmap <= 5:

                self._shufflemapcycle = "on"
                self.debug('maps < 6 shufflemapcycle : %s' % self._shufflemapcycle)

        if self._shufflemapcycle == "on":

            random.shuffle(self._listmap)

            if self.console.game.mapName == self._listmap[0]:

                self.console.write("g_nextmap %s"%self._listmap[1])

            else:

                self.console.write("g_nextmap %s"%self._listmap[0])

    def onLoadConfig(self):

        try:
            self._adminlevel = self.config.getint('settings', 'adminlevel')
        
        except Exception, err:
            self.warning("Using default value %s for adminlevel. %s" % (self._adminlevel, err))
        self.debug('min level for cmds : %s' % self._adminlevel)

        try:
            self._shufflemaplevel = self.config.getint('settings', 'shufflemaplevel')
        
        except Exception, err:
            self.warning("Using default value %s for shufflemaplevel. %s" % (self._shufflemaplevel, err))
        self.debug('min level for shufflemapcycle : %s' % self._shufflemaplevel)

        try:
            self._shufflemapcycle = self.config.get('settings', 'shufflemapcycle')
            
            if self._shufflemapcycle != "on" and self._shufflemapcycle !="off":
                self._shufflemapcycle = "off"
        
        except Exception, err:
            self.warning("Using default value %s for shufflemapcycle. %s" % (self._shufflemapcycle, err))
        self.debug('shufflemapcycle : %s' % self._shufflemapcycle)

    def onEvent(self, event):
        
        if event.type == b3.events.EVT_GAME_MAP_CHANGE:

            self._listmapsplayed.append(self.console.game.mapName)

            if self._rmonoff == "on":

                self._comptemaps += 1

                if self._shufflemapcycle == "on":

                    if self._comptemaps == self.nmap and self.nmap > 1:

                        self._comptemaps = 1

                        random.shuffle(self._listmap)

                    x = self._comptemaps - 1

                    if self.console.game.mapName == self._listmap[x] and self.nmap > 1:

                        x += 1

                    self.nextmap = self._listmap[x]

                    thread.start_new_thread(self.wait, (50,))

                    self.console.write("g_nextmap %s"%self.nextmap)

                if self._shufflemapcycle == "off":

                    if self.nmap >= 8:

                        z = 5

                    if self.nmap < 8:

                        z = self.nmap / 2

                    if self._comptemaps == z:

                        self._comptemaps = z -1 
                        self._listmapsplayed.remove(self._listmapsplayed[0])

                    self.randommap()

            self.debug("shufflemapcycle %s"%self._listmap)
            self.debug("listmapsplayed %s"%self._listmapsplayed)
            self.debug("mapsplayed %s / %s"%(self._comptemaps, self.nmap))
    
    def randommap(self):

        self.random()

        while self.nextmap in  self._listmapsplayed:

            self.random()

        thread.start_new_thread(self.wait, (50,))

        self.console.write("g_nextmap %s"%self.nextmap)

    def listemaps(self):

        self._listemap = []

        mapcycletxt = self.console.getCvar('g_mapcycle').getString()
        homepath = self.console.getCvar('fs_homepath').getString()
        basepath = self.console.getCvar('fs_basepath').getString()
        gamepath = self.console.getCvar('fs_game').getString()

        mapcyclefile = basepath + "/" + gamepath + "/" + mapcycletxt

        if fexist(mapcyclefile) == False:
                
            mapcyclefile = homepath + "/" + gamepath + "/" + mapcycletxt

        self.debug('Mapcycle : %s' % mapcyclefile)

        fichier = open(mapcyclefile, "r")

        contenu = fichier.readlines()
        fichier.close()

        for ligne in contenu:
            
            ligne = ligne.replace("\n", "")
            ligne = ligne.replace("\r", "")
            ligne = ligne.replace(" ", "")
            
            if ligne != "":
                
                if self._test == None:
                    
                    if "{" in ligne:

                        self._test = "test"
                        continue
            
                    else:

                        self._listmap.append(ligne)
                        
                    if self._test != None:
            
                        if "}" in ligne:

                            self._test = None

        self.nmap = 0

        for map in self._listmap:
            self.nmap += 1

    def random(self):

        namap = random.randint(0, self.nmap-1)

        x = namap
        self.nextmap = self._listmap[x]

        return

    def ut4mapname(self, map):

        if map[:4] == 'ut4_': map = map[4:]
        
        elif map[:3] == 'ut_': map = map[3:]

        return map

    def wait(self, temps):

        time.sleep(temps)
          
        map = self.nextmap

        map = self.ut4mapname(map)

        if self._shufflemapcycle == "off":

            self.console.write('bigtext "^2Random Nextmap: ^4%s^7"'%map)

        else:

            self.console.write('bigtext "^3ShuffleMapcycle Nextmap: ^4%s^7"'%map)

    def cmd_randommap(self, data, client, cmd=None):
        
        """\
        activate / deactivate RandomMapUrT
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
        
            if self._rmonoff == 'on':

                client.message('RandomMapUrT ^2activated')

            if self._rmonoff == 'off':

                client.message('RandomMapUrT ^1deactivated')

            client.message('!randommap <on / off>')
            return

        if input[0] == 'on':

            if self._rmonoff != 'on':

                self._rmonoff = 'on'
                message = '^2activated'

            else:

                client.message('RandomMapUrT is already ^2activated') 

                return False

        if input[0] == 'off':

            if self._rmonoff != 'off':

                self._rmonoff = 'off'
                message = '^1deactivated'

            else:
                
                client.message('RandomMapUrT is already ^1disabled')                

                return False

        client.message('RandomMapUrT %s'%(message))

    def cmd_shufflemapcycle(self, data, client, cmd=None):
        
        """\
        activate / deactivate ShuffleMapcycle
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
        
            if self._shufflemapcycle == 'on':

                client.message('ShuffleMapcycle ^2activated')

            if self._shufflemapcycle == 'off':

                client.message('ShuffleMapcycle ^1deactivated')

            client.message('!shufflemapcycle <on / off>')
            return

        if input[0] == 'on':

            if self._shufflemapcycle != 'on':

                self._shufflemapcycle = 'on'
                message = '^2activated'

            else:

                client.message('ShuffleMapcycle is already ^2activated') 

                return False

        if input[0] == 'off':

            if self._shufflemapcycle != 'off':

                self._shufflemapcycle = 'off'
                message = '^1deactivated'

            else:
                
                client.message('ShuffleMapcycle is already ^1disabled')                

                return False

        client.message('ShuffleMapcycle %s'%(message))

    def cmd_shufflemaps(self, data, client, cmd=None):
        
        """\
        Shuffle mapcycle
        """

        random.shuffle(self._listmap)

        if self.console.game.mapName == self._listmap[0] and self.nmap > 1:

            map = self._listmap[1]

        else:

            map = self._listmap[0]

        self.console.write("g_nextmap %s"%map)

        map = self.ut4mapname(map)

        client.message('ShuffleMapcycle Nextmap : %s'%map)

        self.console.write('bigtext "^3ShuffleMapcycle Nextmap: ^4%s^7"'%map)

        self.debug("shufflemapcycle %s"%self._listmap)

