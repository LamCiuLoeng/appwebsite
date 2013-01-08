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


def createApp(folder, package, activity, appname):
    try:
        # create source code framework
        command = 'C:/phonegap/lib/android/bin/create %s %s %s'
        os.popen(command % (folder, package, activity))

        string_xml = os.path.join(folder, 'res/values/strings.xml')
        f = open(string_xml, 'r')
        c = f.readlines()
        f.close()
        f = open(string_xml, 'w')
        c[2] = '<string name="app_name">%s</string>\n' % appname
        f.writelines(c)
        f.close()


        # signed the .apk
        ant_properties = os.path.join(folder, 'ant.properties')
        f = open(ant_properties, 'a+')
        f.write('key.store=D:/eclipse_workspace_partime/appwebsite/sys2do/sys2do.keystore\n')
        f.write('key.alias=sys2do')
        f.close()

        # complie and get the .apk
        cmd = 'ant release -f %s' % os.path.join(folder, 'build.xml')
        os.popen(cmd)
        return True
    except:
        traceback.print_exc()
        return False

