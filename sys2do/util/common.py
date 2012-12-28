# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2012-12-28
#  @author: CL.Lam
#  Description:
###########################################
'''
from flask import request
from flask import current_app as app


__all__ = ['_g', '_gl', '_gp', '_debug', '_info', '_error' ]

def _g(name, default = None):
    return request.values.get(name, default) or None

def _gl(name):
    return request.form.getlist(name)

def _gp(prefix):
    return sorted([(k, v or None) for k, v in request.values.items() if k.startswith(prefix)], cmp = lambda x, y: cmp(x[0], y[0]))


_debug = lambda msg : app.logger.debug(msg)

_info = lambda msg : app.logger.info(msg)

_error = lambda msg : app.logger.error(msg)
