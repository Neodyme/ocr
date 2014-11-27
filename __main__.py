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
# from gui import gui

def print_help():
    print('''Usage: {0}: [OPTION] scan|text|learn file [file...]\
          \nExtract string from image file
          \nvalid argument may be:\
          \n    -h, --help: print this help message\
          \n    -d, --dir: dataset directory\
          \n    scan: scan for valid text in file'''.format(sys.argv[0]))
    sys.exit(0)

if __name__=="__main__":
    optlist, args = getopt.getopt(sys.argv[1:], "hd:k:", ["help", "dir", "knn"])
    direc = "dataset"
    knn = None
    for o, a in optlist:
        if o in ("-h", "--help"):
            print_help()
        if o in ("-d", "--dir"):
            direc = a
        if o in ("-k", "--knn"):
            knn = a
    if len(args) >= 2 and args[0] in ("s", "scan"):
        if not knn:
            knn = learnLetter()
        else:
            knn = read_pickled_knn(knn)
        for filename in args[1:]:
            scan(knn, filename)
    elif len(args) >= 2 and args[0] in ("t", "text"):
        print(direc)
        if not knn:
            knn = learnLetter(directory=direc)
        else:
            knn = read_pickled_knn(knn)
        for filename in args[1:]:
            scantext(knn, filename)
    elif len(args) >= 1 and args[0] in ("l", "learn"):
        knn = learnLetter(pickle_knn=True, directory=direc)
    elif len(args) >= 1 and args[0] in ("f", "format"):
        if len(args) >= 2:
            for filename in args[1:]:
                splitDataset(filename)
#    else:
#       gui(args)
    sys.exit(0)
