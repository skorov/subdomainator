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

APIKEY = config.VIRUSTOTAL_API
BASEDIR = os.path.join(os.path.dirname(__file__), '..')
DATABASE = os.path.join(BASEDIR, config.DATABASE)
db.connect(DATABASE)


def getSubdomains(domain, apikey):
    """Must return a list of subdomains only. Eg: 'www' and not 'www.example.com'"""
    try:
        url = 'https://www.virustotal.com/vtapi/v2/domain/report'
        params = {'domain': domain, 'apikey': apikey}
        response = urllib.urlopen('%s?%s' % (url, urllib.urlencode(params))).read()
        response_dict = json.loads(response)
        subdomain_list = response_dict['subdomains']
        subslist = []
        for s in subdomain_list:
            subslist.append(re.search('(.+)?.%s' % domain, s).group(1))
        return subslist
    except Exception as e:
        print(str(e))


def getSubsFromDB(domain):
    return db.getSubdomains(domain)


def getDomainsFromDB():
    return db.getDomains()


def addSubToDB(subdomain, domain):
    db.addSubdomain(subdomain, domain)


def getPushkeysFromDB():
    return db.getPushkeys()


def sendNotification(subdomain, pushkeys):
    for k in pushkeys:
        p.push('Found %s' % subdomain, k)


if (not db.dbexists()):
    print("Database is not initialised. You should make it.")
    sys.exit()

newdomain = ""
try:
    newdomain = sys.argv[1]
except:
    pass

print("Looking for new subdomains in VirusTotal...")
domains = getDomainsFromDB()
pushkeys = getPushkeysFromDB()

if newdomain:
    domains = [newdomain]

for domain in domains:
    subs = getSubdomains(domain, APIKEY)
    dbsubs = getSubsFromDB(domain)
    for sub in subs:
        if sub not in dbsubs:
            fqdn = sub + '.' + domain
            if not newdomain:
                sendNotification(fqdn, pushkeys)
            addSubToDB(sub, domain)
            print("New domain found: %s" % fqdn)
