# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2012-12-28
#  @author: CL.Lam
#  Description:
###########################################
'''
import os
from datetime import datetime as dt
from flask import request, session
from flask import current_app as app

from sys2do.setting import UPLOAD_FOLDER, UPLOAD_FOLDER_PREFIX, \
    UPLOAD_FOLDER_URL
from sys2do.model import DBSession, UploadFile



__all__ = ['_g', '_gs', '_gl', '_gp', '_debug', '_info', '_error', 'upload' ]

def _g(name, default = None):
    return request.values.get(name, default) or None


def _gs(*name_list):
    return [_g(name) for name in name_list]


def _gl(name):
    return request.form.getlist(name)

def _gp(prefix):
    return sorted([(k, v or None) for k, v in request.values.items() if k.startswith(prefix)], cmp = lambda x, y: cmp(x[0], y[0]))


_debug = lambda msg : app.logger.debug(msg)

_info = lambda msg : app.logger.info(msg)

_error = lambda msg : app.logger.error(msg)



def upload(name):
    f = request.files.get(name, None)
#    if not f : raise makeException(MSG_NO_FILE_UPLOADED)
    if not f : return None

    dir_path = os.path.join(UPLOAD_FOLDER_PREFIX, UPLOAD_FOLDER)

    if not os.path.exists(dir_path) : os.makedirs(dir_path)

    (pre, ext) = os.path.splitext(f.filename)

    converted_name = "%s%s" % (dt.now().strftime("%Y%m%d%H%M%S"), ext)
    path = os.path.join(dir_path, converted_name)
    f.save(path)

    db_file_name = os.path.basename(f.filename)
    db_file_path = os.path.join(UPLOAD_FOLDER, converted_name)
    u = UploadFile(create_by_id = session['user_profile']['id'], name = db_file_name, path = db_file_path, url = "/".join([UPLOAD_FOLDER_URL, converted_name]))
    DBSession.add(u)
    DBSession.flush()
    return u
