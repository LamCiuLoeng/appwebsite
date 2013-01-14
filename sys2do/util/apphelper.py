# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2013-1-8
#  @author: CL.Lam
#  Description:
###########################################
'''
import os
import traceback
from subprocess import Popen, PIPE
import shutil
from sys2do.setting import UPLOAD_FOLDER, UPLOAD_FOLDER_PREFIX, \
    UPLOAD_FOLDER_URL

from sys2do.model import DBSession, UploadFile


def createApp(user_id, appdir, package, activity, appname):
    try:
        if not os.path.exists(appdir) : os.makedirs(appdir)
        # create source code framework
        folder = os.path.join(appdir, activity)
        command1 = 'C:/phonegap/lib/android/bin/create %s %s %s' % (folder, package, activity)
        print "*" * 20
        print command1
        print "_" * 20
        p1 = Popen(command1, shell = True)
        p1.wait()

        string_xml = os.path.join(folder, 'res/values/strings.xml')
        print "*" * 20
        print string_xml
        print "_" * 20
        f = open(string_xml, 'r')
        c = f.readlines()
        f.close()
        f = open(string_xml, 'w')
        c[2] = '<string name="app_name">%s</string>\n' % appname
        f.writelines(c)
        f.close()


        # signed the .apk
        ant_properties = os.path.join(folder, 'ant.properties')
        print "*" * 20
        print ant_properties
        print "_" * 20
        f = open(ant_properties, 'a+')
        f.write('key.store=D:/eclipse_workspace_partime/appwebsite/sys2do/sys2do.keystore\n')
        f.write('key.alias=sys2do\n')
        f.write('key.store.password=ciuloeng\n')
        f.write('key.alias.password=ciuloeng')
        f.close()

        # complie and get the .apk
        command2 = 'ant release -f %s' % os.path.join(folder, 'build.xml')
        p2 = Popen(command2, shell = True)
        p2.wait()

        app_path = os.path.join(folder, 'bin', '%s-release.apk' % activity)
        filename = os.path.basename(app_path)
        shutil.copy(app_path, os.path.join(UPLOAD_FOLDER_PREFIX, UPLOAD_FOLDER, filename))

#        appFile = UploadFile(create_by_id = user_id,
#                                        name = filename, path = os.path.join(UPLOAD_FOLDER, filename),
#                                        url = "/".join([UPLOAD_FOLDER_URL, filename]))
#
#        DBSession.add(appFile)

        # clean the target foler
        command3 = 'ant clean -f %s' % os.path.join(folder, 'build.xml')
        p3 = Popen(command3, shell = True)
        p3.wait()
        return "/".join([UPLOAD_FOLDER_URL, filename])
    except:
        traceback.print_exc()
        return None

