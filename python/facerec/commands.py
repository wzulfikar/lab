#!/usr/bin/env python

import sys

import lib.command_runner as command_runner

# commands from facerec module
import modules.facerec.commands.faceadd as faceadd
import modules.facerec.commands.facefind as facefind
import modules.facerec.commands.facedb as facedb
import modules.facerec.commands.setup_db as setup_db

# register your commands here
commands = {
    'faceadd': faceadd,
    'facedb': facedb,
    'facefind': facefind,
    'setupdb': setup_db,
}

if len(sys.argv) == 1:
    command_runner.list_commands(commands)
else:
    _, command, *args = sys.argv
    command_runner.run(commands, command, args)