#! /usr/bin/env python
import os

os.chdir("/home/bjorn/WikidPad")

import WikidPadStarter

if __name__ == "__main__":
    WikidPadStarter.main()



'''
Linux:

this file can be put in the wikidpad intallation directory (above user_extensions)

The a launcher can be set to invoke with this command:

python -O /home/bjorn/WikidPad/WikidPad.py

where /home/bjorn/WikidPad is the wp dir
'''