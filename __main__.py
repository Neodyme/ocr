#!/usr/bin/env python3.2
#-*- encoding: utf-8 -*-

# __main__.py
# 
# Started on  Thu Oct 30 13:52:13 2014 Prost P.
## Last update Thu Oct 30 14:32:20 2014 Prost P.
#
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

if __name__=="__main__":
    optlist, args = getopt.getopt(sys.argv[1:], "h", ["help",])
    for o, a in optlist:
        if o in ("-h", "--help"):
            print('''Usage: {0}: [OPTION] scan|learn file [file...]\
                   \nvalid argument may be:\
                   \n\t-h, --help: print this help message\
                   \n\tscan: scan for valid text in file'''.format(sys.argv[0]))
            sys.exit(0)

        elif o in "scan":
            for filename in optlist[1:]:
                do_scan(filename)
    sys.exit(0)
