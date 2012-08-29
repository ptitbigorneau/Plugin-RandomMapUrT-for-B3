# RandomMapUrT Plugin

__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '1.0'

import b3
import b3.plugin
import b3.events
import random
import b3, time, threading, thread

class RandommapurtPlugin(b3.plugin.Plugin):
    
    _adminPlugin = None
    _adminlevel = 100
    _rmonoff = "on"
    _test = None
    _listmap = []

    def onStartup(self):

        self._adminPlugin = self.console.getPlugin('admin')
        
        if not self._adminPlugin:

            self.error('Could not find admin plugin')
            return False
        
        self.registerEvent(b3.events.EVT_GAME_ROUND_START)

        self._adminPlugin.registerCommand(self, 'randommap',self._adminlevel, self.cmd_randommap)
        
    def onLoadConfig(self):

        try:
            self._adminlevel = self.config.getint('settings', 'adminlevel')
        except Exception, err:
            self.warning("Using default value %s for adminlevel. %s" % (self._adminlevel, err))
        self.debug('min level for cmds : %s' % self._adminlevel)

    def onEvent(self, event):
        
        if event.type == b3.events.EVT_GAME_ROUND_START:

            if self._rmonoff == "on":

                self.randommap()
    
    def cmd_randommap(self, data, client, cmd=None):
        
        """\
        activate / deactivate randommapurt
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

    def randommap(self):

        nmap = 0

        mapcycletxt = self.console.getCvar('g_mapcycle').getString()
        homepath = self.console.getCvar('fs_homepath').getString()
        gamepath = self.console.getCvar('fs_game').getString()
        mapcyclefile = homepath + "/" + gamepath + "/" + mapcycletxt

        fichier = open(mapcyclefile, "r")

        contenu = contenu = fichier.readlines()
        fichier.close()

        for ligne in contenu:
            
            ligne = ligne.replace("\n", "")
            ligne = ligne.replace("\r\n", "")
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

        for map in self._listmap:
            nmap += 1

        namap = random.randint(0, nmap-1)

        x = namap
        self.nextmap = self._listmap[x]

        cmap = self.console.game.mapName

        if cmap == self.nextmap:

            x += 1
            self.nextmap = self_listmap[x]
                
        thread.start_new_thread(self.wait, (60,))

        self.console.write("g_nextmap %s"%self.nextmap)

    def wait(self, temps):

        time.sleep(temps)
          
        map = self.nextmap

        if map[:4] == 'ut4_': map = map[4:]
        
        elif map[:3] == 'ut_': map = map[3:]

        self.console.write('bigtext "^2Random Nextmap: ^4%s^7"'%map)
