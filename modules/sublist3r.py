#!/usr/bin/python
# Module to run sublist3r and it's functionality
# Give a domain name argument the first time to suppress notifications
#
# Author: skorov

import os
import re
import sys
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import config
import dbconnector as db
import pushbullet as p
import sdmodulebase

# Global Constants #
SUBLIST3R_PATH = config.SUBLIST3R_PATH
TMP_PATH = '/tmp'


class Sublist3r(sdmodulebase.ModuleBase):

    # Override
    def getSubdomains(self, domain):
        """Must return a list of subdomains only. Eg: 'www' and not 'www.example.com'"""
        try:
            tmp_filename = os.path.join(TMP_PATH, 'subdomaintor.tmp')
            if os.path.isfile(tmp_filename):
                os.remove(tmp_filename)

            subprocess.call([SUBLIST3R_PATH, '-d', domain, '-o', tmp_filename],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            f = open(tmp_filename, 'ro')
            subslist = []
            for line in f:
                subslist.append(re.search('(.+)?.%s' % domain, line).group(1))

            f.close()
            os.remove(tmp_filename)
            return subslist
        except Exception as e:
            print(str(e))
            return []

    def run(self):
        print("Running Sublist3r...")
        super(Sublist3r, self).run()

if __name__ == "__main__":
    Sublist3r().run()
