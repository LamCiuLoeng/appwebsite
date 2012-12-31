# -*- coding: utf-8 -*-

import traceback
import sys

reload(sys)
sys.setdefaultencoding('utf8')


from sys2do.model import metadata, engine, DBSession, User


def init():
    try:
        print "create tables"
        metadata.drop_all(engine, checkfirst = True)
        metadata.create_all(engine)

        DBSession.add(User(email = 'test@sys2do.com', password = 'test'))
        DBSession.add(User(email = 'admin@sys2do.com', password = 'admin'))
        DBSession.commit()

        print "finish init!"
    except:
        traceback.print_exc()
        DBSession.rollback()




if __name__ == '__main__':
    init()
