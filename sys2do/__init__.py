# -*- coding: utf-8 -*-

from flask import Flask, Module
from flask_beaker import BeakerSession
from flaskext.babel import Babel

__all__ = ["app"]

app = Flask(__name__, static_url_path = '/static')
app.config.from_object("sys2do.setting")
beaker = BeakerSession(app)  # set the beader session plugin
babel = Babel(app)  # set the babel i18n plugin

app.debug = True


#===============================================================================
# sys.py
#===============================================================================
import views.sys as s
for error_code in [403, 404] : app.error_handler_spec[None][error_code] = s.error_page(error_code)


#===============================================================================
# root.py
#===============================================================================
import views.root
app.register_blueprint(views.root.bpRoot)

#===============================================================================
# consoles.py
#===============================================================================
import views.consoles
app.register_blueprint(views.consoles.bpConsoles, url_prefix = '/c')


#===============================================================================
# import the customize filter and testing
#===============================================================================
import util.filters as filters
for f in filters.__all__ : app.jinja_env.filters[f] = getattr(filters, f)

import util.tests as tests
for t in tests.__all__ : app.jinja_env.tests[t] = getattr(tests, t)
