#!/usr/bin/env python3
# -*- coding: utf-8  -*-
#
#  jogobot.py
#
#  Copyright 2015 GOLDERWEB – Jonathan Golder <jonathan@golderweb.de>
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

import os

import pywikibot


class JogoBot:
    """
    Basic bot framework
    """

    def __init__( self ):
        """
        Initialise our class
        """

        # We need a pywikibot site object
        self.site = pywikibot.Site()

        # We need the shell working directory
        self.cwd = os.getcwd()

    def is_active( self ):
        """
        Checks if whole bot or task specified by task_slug is:
        * not blocked
        * not disabled by file
        * not disabled on wiki
        """
        pass

    def is_active_on_wiki( self, task_slug=None ):
        """
        Checks if whole bot or task specified by task_slug is disabled
        on wiki

        @param task_slug    Slug of task to check, None for whole Bot
        @type str
        """

        # Define page for look up
        if task_slug:
            page_title = "Benutzer:JogoBot/" + task_slug + "/active.js"
        else:
            page_title = "Benutzer:JogoBot/active"

        # Get pywikibot page object
        page = pywikibot.Page( self.site, page_title )

        # Get page text
        page_text = page.get()

        if "true" not in page_text.lower():
            pass
            # Disabled

            # Return False
            # Send E-Mail
            # Create disable-file

    def is_blocked_on_wiki( self ):
        """
        Checks if bot user is blocked on wiki
        """
        if self.site.is_blocked():
            pass
            # Blocked

            # Return False
            # Send E-Mail
            # Create disable-file

    def is_active_by_file(self, task_slug=None):
        """
        Checks if whole bot or task specified by task_slug is disabled
        by file

        @param task_slug    Slug of task to check, None for whole Bot
        @type str
        """

        # Define filepath
        if task_slug:
            disable_file = self.cwd + "/" + task_slug + "/disabled"
        else:
            disable_file = self.cwd + "/disabled"

        if os.path.isfile( disable_file ):
            pass
            # Disabled

            # Return False
            # Send E-Mail

    def create_disable_file( self, task_slug=None ):
        """
        Creates disable file for whole bot or task specified by task_slug

        @param task_slug    Slug of task to check, None for whole Bot
        @type str
        """

        # Define filepath
        if task_slug:
            disable_file = self.cwd + "/" + task_slug + "/disabled"
        else:
            disable_file = self.cwd + "/disabled"

        # Try to create file
        with open(disable_file, 'a'):
            pass
