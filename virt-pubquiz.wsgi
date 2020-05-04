#!/usr/bin/python

import sys
import os

sys.path.append(os.path.split(__file__)[0])

from virt_pubquiz import create_app

application = create_app()
