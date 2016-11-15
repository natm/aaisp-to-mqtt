#!/usr/bin/env python

import os
import sys
import logging
import json
import urllib
import configparser

LOG = logging.getLogger(__name__)
VERSION = 0.1

def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)8s [%(asctime)s] %(message)s')

    if len(sys.argv) != 2:
        LOG.fatal("Config file not supplied")

    cfgfile = sys.argv[1]

    config = configparser.ConfigParser()
    config.read(cfgfile)

    for section in ["aaisp", "mqtt"]:
        if section not in config.sections():
            LOG.fatal("%s section not found in config file %s", section, cfgfile)



    sys.exit(0)

if __name__ == "__main__":
    main()
