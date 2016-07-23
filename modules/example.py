#!/usr/bin/python
# This is an example module file. It does nothing other that give you an idea
# of how to create your own custom modules.
# Give a domain name argument the first time to suppress notifications
#
# Author: skorov

import os
import sys
# More python libs go here

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

# Subdomainator helpers
import config
import dbconnector as db
import pushbullet as p
import sdmodulebase

# Global constants
APIKEY = config.EXAMPLE_APIKEY  # Add to config file if needed. These are this module's settings.


# This module's class. It inerits the ModuleBase
class Example(sdmodulebase.ModuleBase):

    # Override me
    def getSubdomains(self, domain):
        """Must return a list of subdomains only. Eg: 'www' and not 'www.example.com'"""

        # domain variable is provided
        # Do whatever you need to do to get a list of subdomains.

    def run(self):

        # Do some work here before calling running the module

        super(Example, self).run()

if __name__ == "__main__":
    Example().run()
