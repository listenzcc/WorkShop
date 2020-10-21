# File: __init__.py
# Aim: Package init
# coding: utf-8

import os
import logging
import logging.config

# -----------------------------------------------
# Settings
_logging_mode = 'release'
_logging_filename = 'logfile.log'
_logging_configname = os.path.join(__file__,
                                   '..',
                                   'logging.cfg')

# -----------------------------------------------
# Setup logger
logging.config.fileConfig(_logging_configname,
                          defaults=dict(filename=_logging_filename))

logger = logging.getLogger(_logging_mode)
logger.info('Logging started at "{}" mode.'.format(_logging_mode))
