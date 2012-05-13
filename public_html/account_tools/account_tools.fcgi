#!/usr/bin/env python
import sys, os
import account_tools

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")

