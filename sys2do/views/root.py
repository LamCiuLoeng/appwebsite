# -*- coding: utf-8 -*-
import traceback
from datetime import datetime as dt
from flask import current_app as app
from flask import g, render_template, flash, session, redirect, url_for, request
from flask.blueprints import Blueprint
from sqlalchemy.sql.expression import and_


from sys2do.views import BasicView
from sys2do.util.decorator import templated
from sys2do.model import User, DBSession
from sys2do.util.common import _g, _error
from sys2do.util.constant import MESSAGE_ERROR, MSG_USER_NOT_EXIST, \
    MSG_WRONG_PASSWORD

__all__ = ['bpRoot']

bpRoot = Blueprint('bpRoot', __name__)

class RootView(BasicView):

    @templated()
    def index(self):
        return {}

    @templated()
    def about(self):
        pass


    @templated()
    def contact(self):
        pass

    @templated()
    def register(self):
        pass

    def save_register(self):
        pass

    @templated()
    def login(self):
        pass


    def check(self):
        try:
            u = DBSession.query(User).filter(and_(User.active == 0, User.name == _g('name'))).one()
        except:
            _error(traceback.print_exc())
            flash(MSG_USER_NOT_EXIST, MESSAGE_ERROR)
            return redirect(url_for('bpRoot.view', action = 'login', next = _g('next')))
        else:
            if not _g('password'):
                flash(MSG_WRONG_PASSWORD, MESSAGE_ERROR)
                return redirect(url_for('bpRoot.view', action = 'login', next = _g('next')))

            if not u.validate_password(_g('password')):
                flash(MSG_WRONG_PASSWORD, MESSAGE_ERROR)
                return redirect(url_for('bpRoot.view', action = 'login', next = _g('next')))
            else:
                # fill the info into the session
                session['login'] = True
                session['user_profile'] = u.populate()
                permissions = set()
                for g in u.groups:
                    for p in g.permissions:
                        permissions.add(p.name)
                session['user_profile']['groups'] = [g.name for g in u.groups]
                session['user_profile']['permissions'] = list(permissions)
                u.last_login = dt.now()
                session.permanent = True
                DBSession.commit()
                if _g('next') : return redirect(_g('next'))
                return redirect(url_for('.view', action = 'index'))


    def logout(self):
        session.pop('login', None)
        session.pop('user_profile', None)
        return redirect(url_for('bpRoot.view'))

bpRoot.add_url_rule('/', view_func = RootView.as_view('view'), defaults = {'action':'index'})
bpRoot.add_url_rule('/<action>', view_func = RootView.as_view('view'))
