# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from sys2do import app

if __name__ == '__main__':
    app.run(host = 'localhost', port = 5000)
