#!/usr/bin/env python2.7
#-*- encoding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#        
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import sys
import getopt

from scan import *
from gui import gui

def print_help():
    print('''Usage: {0}: [OPTION] scan|text|learn file [file...]\
          \nExtract string from image file 
          \nvalid argument may be:\
          \n    -h, --help: print this help message\
          \n    scan: scan for valid text in file'''.format(sys.argv[0]))
    sys.exit(0)

if __name__=="__main__":
    optlist, args = getopt.getopt(sys.argv[1:], "h", ["help",])
    for o, a in optlist:
        if o in ("-h", "--help") :
            print_help()
    if len(args) >= 2 and args[0] in ("s", "scan"):
        for filename in args[1:]:
            scan(filename)
    elif len(args) >= 2 and args[0] in ("t", "text"):
        for filename in args[1:]:
            scantext(filename)
    elif len(args) >= 1 and args[0] in ("l", "learn"):
        if len(args) >= 2:
            learnLetter(filename)
        else:
            learnLetter()
    else:
       gui(args)
    sys.exit(0)
