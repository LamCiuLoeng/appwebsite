# -*- coding: utf-8 -*-

import datetime
from jinja2.filters import do_default
from sys2do.constant import SYSTEM_DATE_FORMAT, SYSTEM_DATETIME_FORMAT

__all__ = ['ft', 'fd', 'f', ]


def ft(t, f = SYSTEM_DATETIME_FORMAT):
    try:
        return t.strftime(f)
    except:
        return '' if not t else str(t)


def fd(d, f = SYSTEM_DATE_FORMAT):
    try:
        return d.strftime(f)
    except:
        return '' if not d else str(d)


f = lambda v, default = u'' : do_default(v, default) or default
