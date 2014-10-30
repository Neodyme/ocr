#!/usr/bin/env python2.7
#-*- encoding: utf-8 -*-

# Started on  Thu Oct 30 13:52:13 2014 Prost P.
## Last update Thu Oct 30 15:36:05 2014 Prost P.
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

from scan import scan

if __name__=="__main__":
    optlist, args = getopt.getopt(sys.argv[1:], "h", ["help",])
    for o, a in optlist:
        if o in ("-h", "--help"):
            print('''Usage: {0}: [OPTION] scan|learn file [file...]\
                   \nvalid argument may be:\
                   \n\t-h, --help: print this help message\
                   \n\tscan: scan for valid text in file'''.format(sys.argv[0]))
            sys.exit(0)

    if args[0] in ("s", "scan") and len(args) >= 2:
        for filename in args[1:]:
            scan(filename)
    sys.exit(0)
