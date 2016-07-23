#!/usr/bin/python
# Base class for module functionality
# Give a domain name argument the first time to suppress notifications
#
# Author: skorov

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import config
import dbconnector as db
import pushbullet as p

# Global constance
BASEDIR = os.path.join(os.path.dirname(__file__), '..')
DATABASE = os.path.join(BASEDIR, config.DATABASE)


class ModuleBase(object):

    def __init__(self):
        db.connect(DATABASE)

    def getSubdomains(self, domain):
        """Must return a list of subdomains only. Eg: 'www' and not 'www.example.com'"""
        return []

    def getSubsFromDB(self, domain):
        return db.getSubdomains(domain)

    def getDomainsFromDB(self):
        return db.getDomains()

    def addSubToDB(self, subdomain, domain):
        db.addSubdomain(subdomain, domain)

    def getPushkeysFromDB(self):
        return db.getPushkeys()

    def sendNotification(self, subdomain, pushkeys):
        for k in pushkeys:
            p.push('Found %s' % subdomain, k)

    def run(self):
        if (not db.dbexists()):
            print("Database is not initialised. You should make it.")
            sys.exit()

        newdomain = ""
        try:
            newdomain = sys.argv[1]
        except:
            pass

        domains = self.getDomainsFromDB()
        pushkeys = self.getPushkeysFromDB()

        if newdomain:
            domains = [newdomain]

        for domain in domains:
            subs = self.getSubdomains(domain)
            dbsubs = self.getSubsFromDB(domain)
            for sub in subs:
                if sub not in dbsubs:
                    fqdn = sub + '.' + domain
                    if not newdomain:
                        self.sendNotification(fqdn, pushkeys)
                    self.addSubToDB(sub, domain)
                    print("New domain found: %s" % fqdn)
