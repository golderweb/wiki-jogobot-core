#!/usr/bin/env python3
# -*- coding: utf-8  -*-
#
#  config.py
#
#  Copyright 2016 GOLDERWEB – Jonathan Golder <jonathan@golderweb.de>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
"""
This module will read config for jogobot from config file (ini-style) using
python standard library module configparser
"""

import configparser
import ast

import pywikibot

__config = configparser.ConfigParser(interpolation=None)
__config.read(pywikibot.config.get_base_dir() + "/jogobot.conf")

# Convert to dict as configparser could contain only strings
config = dict( __config )

# Parse all sections
for section in __config.sections():
    # Convert to dict as configparser could contain only strings
    config[section] = dict( __config[section] )

    # Parse config with ast.literal_eval to get python datatypes
    for key, value in config[section].items():
        config[section][key] = ast.literal_eval( value )

# Make jogobot entrys available in root level (without sections)
for key, value in config["jogobot"].items():
    config[key] = value
