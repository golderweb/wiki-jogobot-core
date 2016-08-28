#!/usr/bin/env python3
# -*- coding: utf-8  -*-
#
#  bot.py
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
Wrapper functions to invoke bot tasks
"""

import sys

from pywikibot import pagegenerators

import jogobot


def active(task_slug):
    """
    Checks up if bot with given task_slug is active via jogobot.framework

    @param  task_slug  Task slug to check
    @type task_slug  str

    @return  True if active, otherwise False
    @rtype  bool
    """

    try:
        # Will throw Exception if disabled/blocked
        jogobot.is_active( task_slug )

    except jogobot.jogobot.Blocked:
        (type, value, traceback) = sys.exc_info()
        jogobot.output( "\03{lightpurple} %s (%s)" % (value, type ),
                        "CRITICAL" )
        return False

    except jogobot.jogobot.Disabled:
        (type, value, traceback) = sys.exc_info()
        jogobot.output( "\03{red} %s (%s)" % (value, type ),
                        "ERROR" )
        return False

    # Bot/Task is active
    else:
        return True


def parse_local_args( local_args, callback=None ):
    """
    Parses local cmd args which are not parsed by pywikibot

    @param  local_args  Local args returned by pywikibot.handle_args(args)
    @type  iterable
    @param  callback  A callback method could be provided. It will get a single
                      arg and the related value as params:
                            callback( arg, value )
                      The method should return a tuple of key, value which can
                      be directly appended to the kwargs dict.
                      Or if arg is not relevant, return None or False. Then the
                      arg will be passed to genFactory.handleArg()
    @type  callable

    @returns  The following tuple
        @return 1  Slug of given subtask (Arg "-task")
        @rtype  str
        @return 2  GenFactory with parsed pagegenerator args
        @rtype  pagegenerators.GeneratorFactory
        @return 3  Additional args for subtasks
        @rtype  dict
    @rtype  tuple
    """

    # This factory is responsible for processing command line arguments
    # that are also used by other scripts and that determine on which pages
    # to work on.
    genFactory = pagegenerators.GeneratorFactory()

    # If always is True, bot won't ask for confirmation of edit (automode)
    # always = False

    # If force_reload is True, bot will always parse Countrylist regardless
    # if parsing is needed or not
    # force_reload = False

    # Subtask selects the specific bot to run
    # Default is reddiscparser
    subtask = None

    # kwargs are passed to selected bot as **kwargs
    kwargs = dict()

    # Parse command line arguments
    for arg in local_args:

        # Split args
        argkey, sep, value = arg.partition(':')

        if argkey.startswith("-always"):
            kwargs['always'] = True
        elif argkey.startswith("-task"):
            subtask = value

        # Must be the last but one entry
        elif callable(callback):
            ret_val = callback( argkey, value )

            # Was relevant for callback
            if ret_val:
                kwargs[ret_val[0]] = ret_val[1]
            # Otherwise pass to genFactory.handleArg(arg)
            else:
                genFactory.handleArg(arg)
        else:
            genFactory.handleArg(arg)

    # Return Tuple
    return ( subtask, genFactory, kwargs )


# In current version it does not realy make sense to use this method,
# as it just proxies the callback
def prepare_bot( task_slug, subtask, genFactory, subtask_args, callback ):
    """
    Handles importing subtask Bot class and prepares specific args

    Throws exception if bot not exists

    @param  task_slug  Task slug, needed for logging
    @type task_slug  str
    @param  subtask  Slug of given subtask
    @type  subtask  str
    @param  genFactory  GenFactory with parsed pagegenerator args
    @type  genFactory  pagegenerators.GeneratorFactory
    @param  subtask_args  Additional args for subtasks
    @type  subtask_args  dict
    @param  callback  A reference to a callback method which gets the arg
                      of this method (except the callback) and should
                      return the same as this function


    @returns  The following tuple
        @return 1  Subtask slug (replaced None for default)
        @rtype  str
        @return 2  Botclass of given subtask (Arg "-task")
        @rtype  Class
        @return 3  GenFactory with parsed pagegenerator args
        @rtype  pagegenerators.GeneratorFactory
        @return 4  Additional args for subtasks
        @rtype  dict
    @rtype  tuple
    """
    # kwargs are passed to selected bot as **kwargs
    kwargs = dict()

    if callable( callback ):
        ( subtask, Bot, genFactory, subtask_args ) = callback(
            task_slug, subtask, genFactory, subtask_args )
    # Subtask error
    else:
        jogobot.output( (
            "\03{{red}} Given prepare_bot_callback from \"{task_slug}\" " +
            "is not callable!" ).format(task_slug=task_slug), "ERROR" )
        raise Exception

    return ( subtask, Bot, genFactory, kwargs )


def init_bot( task_slug, subtask, Bot, genFactory, **kwargs ):
    """
    Initiates Bot-Object with Class given in Bot and passes params genFactory
    and kwargs to it

    Passes through exception generated by Bot.__init__() after logging.

    @param  task_slug  Task slug, needed for logging
    @type task_slug  str
    @param  subtask  Slug of given subtask
    @type  subtask  str
    @param  Bot  Bot class to build bot-object from
    @type  Class
    @param  genFactory  GenFactory with parsed pagegenerator args
    @type  genFactory  pagegenerators.GeneratorFactory
    @param  **kwargs  Additional args for Bot()
    @type  **kwargs  dict

    @returns bot-object
    @type  type(Bot())
    """
    # Bot gets prepared genFactory as first param and possible kwargs dict
    # It has to threw an exception if something does not work properly
    try:
        # Init bot with genFactory and **kwargs
        bot = Bot( genFactory, **kwargs )

    except:
        # Catch Errors while initiation
        jogobot.output( (
            "\03{{red}} Error while trying to init " +
            "subtask \"{task_slug}-{subtask}\"!" ).
            format( task_slug=task_slug, subtask=subtask ), "ERROR" )
        raise
    else:
        # Init successfull
        jogobot.output( (
            "Subtask \"{task_slug}-{subtask}\" was " +
            "initiated successfully" ).
            format(task_slug=task_slug, subtask=subtask) )
        return bot


def run_bot( task_slug, subtask, bot ):
    """
    Calls the run()-method of bot-object

    Passes through exceptions generated by Bot.__init__() after logging.
    Catches Errors caused by missing run(0-method.

    @param  task_slug  Task slug, needed for logging
    @type task_slug  str
    @param  subtask  Slug of given subtask
    @type  subtask  str
    @param  bot  Bot object to call run()-method on
    @type  object with method run
    """

    # Fire up Bot
    # Bot must have implemented a run()-method
    # It has to threw an exception if something does not work properly
    try:
        # Call run method on Bot
        bot.run()

    # Special event on AttributeError to catch missing run()-method
    except AttributeError:
        (type, value, traceback) = sys.exc_info()

        # Catch missing run()-method
        if "has no attribute 'run'" in value:
            jogobot.output( (
                "\03{{red}} Error while trying to run " +
                "subtask \"{task_slug}-{subtask} \": +"
                "Run-method is missing! ").
                format( task_slug=task_slug, subtask=subtask ), "ERROR" )

        # Pass through other AttributeError
        else:
            raise

    except:
        jogobot.output( (
            "\03{{red}} Error while trying to run " +
            "subtask \"{task_slug}-{subtask} \"!" ).
            format( task_slug=task_slug, subtask=subtask ), "ERROR" )
        raise

    else:
        # Run successfull
        jogobot.output( (
            "Subtask \"{task_slug}-{subtask}\" was finished successfully").
            format(task_slug=task_slug, subtask=subtask) )
