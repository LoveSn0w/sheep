#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from lib.consoles.baseCmd import baseCmd
from lib.consoles.useScriptCmd import useScriptCmd
from lib.consoles.runPocsCmd import runPocsCmd
from lib.core.settings import IS_WIN
from thirdparty.colorama.initialise import init as colorInit
from lib.core.data import scr, logger, paths
from lib.core.common import systemQuit, importModule
from lib.core.enums import EXIT_STATUS



class scriptCmd(baseCmd):
    """"""
    def __init__(self):
        if IS_WIN:
            colorInit()
        baseCmd.__init__(self)
        self.shellPrompt = "\033[01;35msheep>script>\033[0m"
        self.current_scrid = 1
        self.scr = scr
        self.scr.pocs = {}
        self.scr.exploits = {}
        self.import_script_dir(paths.SCRIPT_POC_PATH, self.scr.pocs)
        self.pocSum = self.current_scrid - 1
        self.import_script_dir(paths.SCRIPT_EXPLOIT_PATH, self.scr.exploits)
        self.exploitSum = self.current_scrid - self.pocSum - 1


    def fuzzyFinder(self, input):
        """Fuzzy find"""
        results = {}
        input = str(input) if not isinstance(input, str) else input
#        pattern = '.*?'.join(map(re.escape, input))
        regex = re.compile(input, re.I)
        for k, v in self.scr.pocs.items():
            r = regex.search(v)
            if r:
                results.update({k:v})
        for k, v in self.scr.exploits.items():
            r = regex.search(v)
            if r:
                results.update({k: v})
        return results


    def do_search(self, line):
        """Search script by name"""
        res = self.fuzzyFinder(line)
        if res == {}:
            logger.warning('No find!')
            return
        logger.info("Search result:")
        msg_format = "   {:>13}  {:<33}  "
        msgTop_format = "   {:>25}  {:<60}  "
        print
        print(msgTop_format.format('\033[01;32mSCR-ID\033[0m', '\033[01;32mSCR_NAME\033[0m'))
        print(msgTop_format.format('\033[01;33m======\033[0m', '\033[01;33m========\033[0m'))
        for i in res.items():
            print(msg_format.format(*i))


    def do_pocs(self, line):
        """Run multiple scripts """
        poc = runPocsCmd(self.scr.pocs)
        poc.cmdloop()


    def import_script(self, scriptFile, store):
        """Import a scipt from a directory"""
        try:
            if scriptFile and os.path.isfile(scriptFile):
                _ = os.path.split(scriptFile)[1].split('.')
                scriptName = _[0]
                if scriptName.startswith('__init__') or _[1] == 'pyc':
                    return
                store.update({self.current_scrid: scriptName})
                self.current_scrid += 1
        except Exception:
            logger.warning("Import script file error!")


    def import_script_dir(self, scriptDir, store):
        """Import  scripts from a directory"""
        try:
            if scriptDir and os.path.isdir(scriptDir):
                for sname in os.listdir(scriptDir):
                    sname = os.path.join(scriptDir, sname)
                    self.import_script(sname, store)
            else:
                logger.error("script's directory error")
                systemQuit(EXIT_STATUS.ERROR_EXIT)
        except Exception:
            logger.warning("Import script dir error!")


    def checkModule(self, module):
        """Detection  module is correct"""
        ok = 1
        if not hasattr(module, 'readme'):
            logger.warning("Module is the lack of readme dict.")
            ok = 0
        if not hasattr(module, 'run'):
            logger.warning("Module is the lack of run function.")
            ok = 0
        return ok


    def do_use(self, line):
        """Select a script to use"""
        moduleName = modulepath = ''
        if line == "":
            logger.warning("Please select a script's ID.")
            return
        try:
            id = int(line)
            if id < 1 or id >= self.current_scrid:
                logger.warning("Invalid ID!")
                return
            if self.scr.exploits.has_key(id):
                moduleName = self.scr.exploits.get(id)
                modulepath = 'script.exploits.' + moduleName
            else:
                moduleName = self.scr.pocs.get(id)
                modulepath = 'script.pocs.' + moduleName
            module = importModule(modulepath)
            if self.checkModule(module):
                Use = useScriptCmd(module, moduleName)
                Use.cmdloop()
        except TypeError:
            logger.warning("Please select a script's ID.")
        except ValueError:
            logger.warning("Please select a script's ID.")
        except Exception as e:
            logger.error("Use error! %s" % e)


    def do_list(self, line):
        """Show all available scripts"""
        msg_format = "   {:>13}  {:<33}  "
        msgTop_format = "   {:>25}  {:<60}  "
        print
        print(msgTop_format.format('\033[01;32mPOC-ID\033[0m', '\033[01;32mSCR_NAME\033[0m'))
        print(msgTop_format.format('\033[01;33m======\033[0m', '\033[01;33m========\033[0m'))
        for i in scr.pocs.items():
            print(msg_format.format(*i))
        print
        print(msgTop_format.format('\033[01;32mEXPLOIT-ID\033[0m', '\033[01;32mSCR_NAME\033[0m'))
        print(msgTop_format.format('\033[01;33m==========\033[0m', '\033[01;33m========\033[0m'))
        for i in self.scr.exploits.items():
            print(msg_format.format(*i))
        print



