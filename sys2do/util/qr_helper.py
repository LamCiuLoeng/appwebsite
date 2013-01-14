# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2012-6-1
#  @author: CL.Lam
#  Description:
###########################################
'''
from datetime import datetime as dt
import random, os
import traceback
from elaphe import                                                                                                                                      qrcode


from sys2do.setting import UPLOAD_FOLDER, UPLOAD_FOLDER_PREFIX, UPLOAD_FOLDER_URL
from sys2do.model import UploadFile
from sys2do.util.common import _error, _info


def createQR(content, scale = 4, ext = '.png'):
    try:
        filename = "%s%.4d%s" % (dt.now().strftime("%Y%m%d%H%M%S"), random.randint(1, 1000), ext)
        filedir = os.path.join(UPLOAD_FOLDER_PREFIX, UPLOAD_FOLDER)
        if not os.path.exists(filedir): os.makedirs(filedir)
        savepath = os.path.join(filedir, filename)

        c = qrcode.QrCode()
        f = c.render(content, options = dict(version = 4, eclevel = 'L'), scale = scale, margin = 10, data_mode = '8bits')
        f.save(savepath)
        imgFile = UploadFile(name = filename, path = os.path.join(filedir, filename),
                                        url = "/".join([UPLOAD_FOLDER_URL, filename]),
                                        size = os.path.getsize(savepath),
                                        type = ext[1:],)

        return imgFile
    except:
        traceback.print_exc()
        return None
