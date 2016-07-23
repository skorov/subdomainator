#!/usr/bin/python
# Module to get subdomains from Virus Total
# Give a domain name argument the first time to suppress notifications
#
# Author: skorov

import os
import json
import urllib
import re
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import config
import dbconnector as db
import pushbullet as p
import sdmodulebase

# Global constants
APIKEY = config.VIRUSTOTAL_APIKEY


class VirusTotal(sdmodulebase.ModuleBase):
    def getSubdomains(self, domain):
        """Must return a list of subdomains only. Eg: 'www' and not 'www.example.com'"""
        try:
            url = 'https://www.virustotal.com/vtapi/v2/domain/report'
            params = {'domain': domain, 'apikey': APIKEY}
            response = urllib.urlopen('%s?%s' % (url, urllib.urlencode(params))).read()
            response_dict = json.loads(response)
            subdomain_list = response_dict['subdomains']
            subslist = []
            for s in subdomain_list:
                subslist.append(re.search('(.+)?.%s' % domain, s).group(1))
            return subslist
        except Exception as e:
            print(str(e))
            return []

    def run(self):
        print("Looking for new subdomains in VirusTotal...")
        super(VirusTotal, self).run()

if __name__ == "__main__":
    VirusTotal().run()
