#!/usr/bin/python
# Module to get subdomains from Virus Total
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

BASEDIR = os.path.join(os.path.dirname(__file__), '..')
DATABASE = os.path.join(BASEDIR, config.DATABASE)
db.connect(DATABASE)
SUBLIST3R_PATH = '/opt/sublist3r-git/sublist3r.py'
TMP_PATH = '/tmp'


def getSubdomains(domain):
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

print("Running Sublist3r...")
domains = getDomainsFromDB()
pushkeys = getPushkeysFromDB()

if newdomain:
    domains = [newdomain]

for domain in domains:
    subs = getSubdomains(domain)
    dbsubs = getSubsFromDB(domain)
    for sub in subs:
        if sub not in dbsubs:
            fqdn = sub + '.' + domain
            if not newdomain:
                sendNotification(fqdn, pushkeys)
            addSubToDB(sub, domain)
            print("New domain found: %s" % fqdn)
