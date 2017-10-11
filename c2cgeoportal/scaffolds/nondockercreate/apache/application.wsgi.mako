import site
import sys
import re
import os
from logging.config import fileConfig

site.addsitedir("${python_path}")
root = "${project_directory}"


from pyramid.paster import get_app

configfile = os.path.join(root, "${'development' if development == 'TRUE' else 'production'}.ini")

# Load the logging config without using pyramid to be able to use environment variables in there.
vars = dict(__file__=configfile, here=os.path.dirname(configfile))
vars.update(os.environ)
fileConfig(configfile, defaults=vars)

application = get_app(configfile, 'main')
