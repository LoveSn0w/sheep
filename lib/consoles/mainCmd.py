#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
from lib.consoles.baseCmd import baseCmd
from lib.consoles.scriptCmd import scriptCmd
from lib.core.settings import IS_WIN
from thirdparty.colorama.initialise import init as colorInit
from lib.core.common import banner

class mainCmd(baseCmd):
    def __init__(self):
        if IS_WIN:
            colorInit()
        baseCmd.__init__(self)
        self.shellPrompt = "sheep>"
        banner()

    def do_script(self, line):
        scrCmd = scriptCmd()
        scrCmd.cmdloop()

if __name__ == "__main__":
    test = mainCmd()
    test.cmdloop()

