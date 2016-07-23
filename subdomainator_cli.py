#!/usr/bin/python
# CLI for commands within Subdomainator
#
# Author: skorov (Adapted from Empire. Thanks Harmj0y!)

import sys
import os
from cmd import Cmd
from tldextract import extract
import dbconnector as db
import config
import crontab
import subprocess


BASEDIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(BASEDIR, config.DATABASE)
db.connect(DATABASE)

try:
    input = raw_input
except NameError:
    pass


def title():
    os.system("clear")
    print("""
                 _     _               _         _
     _______ _ _| |_ _| |___ _____ ___|_|___ ___| |_ ___ ___
    |       | | | . | . | . |     | .'| |   | .'|  _| . |  _|
    |    ___|___|___|___|___|_|_|_|__,|_|_|_|__,|_| |___|_|
    |        \   ============================================
    |_____    \      I will find you and I will hack you
    |          \ ============================================
    |__________/     [Twitter]: @skorov8 | [Version]: 1.0

    """)


def stats():
    domain_count = len(db.getDomains())
    pushkey_count = len(db.getPushkeys())
    modules = getModulesWithStatus()
    modules_total_count = len(modules)
    modules_enabled_count = len([x for x in modules if x[1] != "off"])
    pushkey_warning = "! You may want to fix this !" if pushkey_count < 1 else ""
    modules_warning = "! You may want to fix this !" if modules_enabled_count < 1 else ""
    print("    [*] %d domains tracked" % domain_count)
    print("    [*] %d Pushbullet keys registered %s" % (pushkey_count, pushkey_warning))
    print("    [*] %d/%d modules enabled %s" % (modules_enabled_count, modules_total_count, modules_warning))
    print("")


def setup():
    title()
    print("Looks like this is your first time running Subdomainator. Let's\n"
          "get things setup.\n"
          "Creating database...")
    db.createdb()
    print("All done. Don't forget to enable the modules!\n")
    input("Hit enter to continue... ")


def printList(title, items):
    """Prints a pretty table of values"""

    # Don't print anything if nothing to print
    if len(items) < 1:
        print("\n[>] Nothing to list\n")
        return

    # Get longest length
    l = len(title)
    for i in items:
        if len(i) > l:
            l = len(i)

    print("\n+-" + '-' * l + "-+")
    print("| " + title.ljust(l) + " |")
    print("+-" + '-' * l + "-+")
    for i in items:
        print("| " + i.ljust(l) + " |")

    print("+-" + '-' * l + "-+\n")


def printModules(items):
    """Print the status of modules"""

    if (len(items) < 1):
        return

    l = 6
    for i in items:
        if len(i[0]) > l:
            l = len(i[0])

    print("\n+-" + '-' * l + "-+-" + '-' * 9 + "-+")
    print("| " + "Module".ljust(l) + " | Frequency |")
    print("+-" + '-' * l + "-+-" + '-' * 9 + "-+")
    for i in items:
        line = "| " + i[0].ljust(l) + " | " + i[1].ljust(9) + " |"
        print(line)

    print("+-" + '-' * l + "-+-" + '-' * 9 + "-+\n")


def getModulesWithStatus():
    """Retrieves a list of all items in the modules folder"""
    ignore_modules = ["sdmodulebase.py", "example.py"]
    modules = []
    for file in os.listdir(os.path.join(BASEDIR, "modules")):
        if file.endswith(".py") and file not in ignore_modules:
            # Get status | True = on, False = off
            name = os.path.splitext(file)[0]
            freq = "off"
            try:
                job = [x for x in crontab.CronTab(user=True) if x.comment == name][0]
                if job.frequency() == 8784:
                    freq = "hourly"
                elif job.frequency() == 366:
                    freq = "daily"
                elif job.frequency() == 52:
                    freq = "weekly"
                elif job.frequency() == 12:
                    freq = "monthly"
            except:
                pass

            modules.append([name, freq])

    return modules


def doFirstRun(domain):
    """Runs all modules to compile the initial entries for a domain"""
    modules = getModulesWithStatus()

    try:
        FNULL = open(os.devnull, 'w')
        for mod in modules:
            script = os.path.join(BASEDIR, "modules", mod[0] + ".py")
            subprocess.Popen(["python", script, domain], stdout=FNULL, stderr=FNULL)

        FNULL.close()
    except Exception as e:
        print(str(e))


class NavMain(Exception):
    pass


class NavDomains(Exception):
    pass


class NavPushkeys(Exception):
    pass


class NavSubdomains(Exception):
    pass


class NavModules(Exception):
    pass


class MainMenu(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = '(Subdomainator) > '
        self.do_help.__func__.__doc__ = '''Displays the help menu.'''
        self.doc_header = 'Commands'

        self.menu_state = "main"

    def cmdloop(self):
        while True:
            try:
                if self.menu_state == "domains":
                    self.do_domains("")
                elif self.menu_state == "pushkeys":
                    self.do_pushkeys("")
                elif self.menu_state == "modules":
                    self.do_modules("")
                else:  # main
                    title()
                    stats()
                    Cmd.cmdloop(self)

            # handle those pesky ctrl+c's
            except KeyboardInterrupt as e:
                self.menu_state = "main"
                try:
                    choice = input("\n[>] Exit? [y/N] ")
                    if choice.lower() != "" and choice.lower()[0] == "y":
                        sys.exit()
                        return True
                    else:
                        continue
                except KeyboardInterrupt as e:
                    continue

            # exception used to signal jumping to "Main" menu
            except NavMain as e:
                self.menu_state = "main"

            # exception used to signal jumping to "Agents" menu
            except NavPushkeys as e:
                self.menu_state = "pushkeys"

            # exception used to signal jumping to "Listeners" menu
            except NavModules as e:
                self.menu_state = "modules"

            except Exception as e:
                print("Exception: %s" % e)

    # stolen/adapted from empire who stole it form recon-ng
    def print_topics(self, header, cmds, cmdlen, maxcol):
        if cmds:
            self.stdout.write("%s\n" % str(header))
            if self.ruler:
                self.stdout.write("%s\n" % str(self.ruler * len(header)))
            for cmd in cmds:
                self.stdout.write("%s %s\n" % (cmd.ljust(17), getattr(self, 'do_' + cmd).__doc__))
            self.stdout.write("\n")

    def emptyline(self):
        pass

    # Commandline Commands
    # ====================
    def default(self, line):
        pass

    def do_exit(self, line):
        """Exit Subdomainator"""
        raise KeyboardInterrupt

    def do_domains(self, line):
        """Mess with domains"""
        try:
            DomainsMenu().cmdloop()
        except Exception as e:
            raise e

    def do_pushkeys(self, line):
        """Mess with Pushbullet keys"""
        try:
            PushkeysMenu().cmdloop()
        except Exception as e:
            raise e

    def do_modules(self, line):
        """Manage modules"""
        try:
            ModulesMenu().cmdloop()
        except Exception as e:
            raise e


class DomainsMenu(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = '(Subdomainator: domains) > '
        self.do_help.__func__.__doc__ = '''Displays the help menu.'''
        self.doc_header = 'Commands'

        self.domains = db.getDomains()
        printList("Domains", self.domains)

    # stolen/adapted from empire who stole it form recon-ng
    def print_topics(self, header, cmds, cmdlen, maxcol):
        if cmds:
            self.stdout.write("%s\n" % str(header))
            if self.ruler:
                self.stdout.write("%s\n" % str(self.ruler * len(header)))
            for cmd in cmds:
                self.stdout.write("%s %s\n" % (cmd.ljust(17), getattr(self, 'do_' + cmd).__doc__))
            self.stdout.write("\n")

    def emptyline(self):
        pass

    # Commandline Commands
    # ====================
    def default(self, line):
        pass

    def do_exit(self, line):
        """Exit Subdomainator"""
        raise KeyboardInterrupt

    def do_back(self, line):
        """Go back to the main menu."""
        raise NavMain()

    def do_adddomain(self, line):
        """Add domain to watch list"""
        newdomain = line.strip()
        if (extract(newdomain).subdomain == ''):
            if (newdomain not in self.domains):
                db.addDomain(newdomain)
                self.domains.append(newdomain)
                doFirstRun(newdomain)

            print("\n[>] Added new domain\n")
        else:
            print("\n[>] Domain not valid. Do not include subdomains. (E.g. example.com)\n")

    def do_removedomain(self, line):
        """Remove domain from list"""
        domain = line.strip()
        if (domain in self.domains):
            db.deleteDomain(domain)
            self.domains.remove(domain)
            print("\n[>] Domain removed.\n")
        else:
            print("\n[>] Domain not in list.\n")

    def do_list(self, line):
        """List domains or subdomains"""
        parts = line.strip().split(' ')

        if parts[0] != '':
            if parts[0] in self.domains:
                subdomains = db.getSubdomains(parts[0])
                for i in range(0, len(subdomains)):
                    subdomains[i] = "%s.%s" % (subdomains[i], parts[0])
                printList("Subdomains", subdomains)

        else:
            printList("Domains", self.domains)

    def complete_removedomain(self, text, line, begidx, endidx):
        """Tab-complete removedomain command"""

        names = self.domains
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        return [s[offs:] for s in names if s.startswith(mline)]

    def complete_list(self, text, line, begidx, endidx):
        """Tab-complete list command"""
        names = self.domains
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        return [s[offs:] for s in names if s.startswith(mline)]


class PushkeysMenu(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = '(Subdomainator: pushkeys) > '
        self.do_help.__func__.__doc__ = '''Displays the help menu.'''
        self.doc_header = 'Commands'

        self.pushkeys = db.getPushkeys()
        printList("Pushbullet Keys", self.pushkeys)

    # stolen/adapted from empire who stole it form recon-ng
    def print_topics(self, header, cmds, cmdlen, maxcol):
        if cmds:
            self.stdout.write("%s\n" % str(header))
            if self.ruler:
                self.stdout.write("%s\n" % str(self.ruler * len(header)))
            for cmd in cmds:
                self.stdout.write("%s %s\n" % (cmd.ljust(17), getattr(self, 'do_' + cmd).__doc__))
            self.stdout.write("\n")

    def emptyline(self):
        pass

    # Commandline Commands
    # ====================
    def default(self, line):
        pass

    def do_exit(self, line):
        """Exit Subdomainator"""
        raise KeyboardInterrupt

    def do_back(self, line):
        """Go back to the main menu."""
        raise NavMain()

    def do_addkey(self, line):
        """Add Pushbullet key to notify list"""
        newkey = line.strip()
        if (newkey[:2] == "o."):
            if (newkey not in self.pushkeys):
                db.addPushkey(newkey)
                self.pushkeys.append(newkey)
                self.do_list(line)

            print("\n[>] Added new key\n")
        else:
            print("\n[>] Invalid key\n")

    def do_removekey(self, line):
        """Remove Pushbullet key from list"""
        key = line.strip()
        if (key in self.pushkeys):
            db.deletePushkey(key)
            self.pushkeys.remove(key)
            print("\n[>] Key removed.\n")
        else:
            print("\n[>] Key not in list.\n")

    def do_list(self, line):
        """List Pushbullet keys"""
        printList("Pushbullet Keys", self.pushkeys)

    def complete_removekey(self, text, line, begidx, endidx):
        """Tab-complete removekey command"""

        names = self.pushkeys
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        return [s[offs:] for s in names if s.startswith(mline)]


class ModulesMenu(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = '(Subdomainator: modules) > '
        self.do_help.__func__.__doc__ = '''Displays the help menu.'''
        self.doc_header = 'Commands'

        self.modules = getModulesWithStatus()
        printModules(self.modules)

    # stolen/adapted from empire who stole it form recon-ng
    def print_topics(self, header, cmds, cmdlen, maxcol):
        if cmds:
            self.stdout.write("%s\n" % str(header))
            if self.ruler:
                self.stdout.write("%s\n" % str(self.ruler * len(header)))
            for cmd in cmds:
                self.stdout.write("%s %s\n" % (cmd.ljust(17), getattr(self, 'do_' + cmd).__doc__))
            self.stdout.write("\n")

    def emptyline(self):
        pass

    # Commandline Commands
    # ====================
    def default(self, line):
        pass

    def do_exit(self, line):
        """Exit Subdomainator"""
        raise KeyboardInterrupt

    def do_back(self, line):
        """Go back to the main menu"""
        raise NavMain()

    def do_enablemodule(self, line):
        """Enable module so that it run periodically"""
        mod = line.strip().split(' ')
        if len(mod) != 2:
            print("\n[>] Syntax: enablemodule [name] (hourly|daily|weekly|monthly)\n")
            return

        if mod[0] not in [x[0] for x in self.modules]:
            print("\n[>] No such module")
            return

        module = [x for x in self.modules if x[0] == mod[0]][0]

        if module[1] != "off":
            print("\n[>] Module already enabled\n")
            return

        if mod[1].lower() not in ['hourly', 'daily', 'weekly', 'monthly']:
            print("\n[>] Timing must be one of: hourly, daily, weekly, monthly\n")
            return

        # Enable module and add to crontab
        command = "python " + os.path.join(BASEDIR, "modules", mod[0] + ".py")
        comment = mod[0]
        cron = crontab.CronTab(user=True)
        job = cron.new(command=command, comment=comment)
        if mod[1].lower() == 'hourly':
            job.every(1).hours()
        elif mod[1].lower() == 'daily':
            job.every(1).days()
        elif mod[1].lower() == 'weekly':
            job.setall("@weekly")
        elif mod[1].lower() == 'monthly':
            job.every(1).month()
        else:
            print("\n[>] How did you even get here??\n")
            return
        cron.write(user=True)
        module[1] = mod[1].lower()
        print("\n[>] Module enabled\n")

    def do_disablemodule(self, line):
        """Disable module from ever running"""
        mod = line.strip().split(' ')
        if mod[0] not in [x[0] for x in self.modules]:
            print("\n[>] No such module")
            return

        module = [x for x in self.modules if x[0] == mod[0]][0]

        if module[1] == "off":
            print("\n[>] Module already disabled\n")
            return

        cron = crontab.CronTab(user=True)
        cron.remove_all(comment=module[0])
        cron.write()
        module[1] = "off"
        print("\n[>] Module disabled\n")

    def do_list(self, line):
        """List available modules"""
        printModules(self.modules)

    def complete_enablemodule(self, text, line, begidx, endidx):
        """Tab-complete disablemodule command"""

        if len(line.split(" ")) > 2:
            intervalTypes = ['hourly', 'daily', 'weekly', 'monthly']
            endLine = " ".join(line.split(" ")[1:])
            mline = endLine.partition(' ')[2]
            offs = len(mline) - len(text)
            return [s[offs:] for s in intervalTypes if s.startswith(mline)]

        names = [x[0] for x in self.modules]
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        return [s[offs:] for s in names if s.startswith(mline)]

    def complete_disablemodule(self, text, line, begidx, endidx):
        """Tab-complete enablemodule command"""

        names = [x[0] for x in self.modules]
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        return [s[offs:] for s in names if s.startswith(mline)]


if not db.dbexists():
    setup()

MainMenu().cmdloop()
