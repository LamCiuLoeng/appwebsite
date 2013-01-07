# -*- coding: utf-8 -*-
import traceback
from datetime import datetime as dt
from flask import current_app as app
from flask import g, render_template, flash, session, redirect, url_for, request
from flask.blueprints import Blueprint
from flask.helpers import jsonify
from sqlalchemy.sql.expression import and_


from sys2do.views import BasicView
from sys2do.util.decorator import templated
from sys2do.constant import MESSAGE_ERROR, MSG_USER_NOT_EXIST, \
    MSG_WRONG_PASSWORD, MSG_NO_ENOUGH_PARAMS, MESSAGE_WARNING

from sys2do.model import User, DBSession, AppObject
from sys2do.util.common import _g, _error, _gs, upload


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
        email, password = _gs('email', 'password')
        if not email or not password :
            flash(MSG_NO_ENOUGH_PARAMS, MESSAGE_WARNING)
            return redirect(url_for('bpRoot.view', action = 'login', next = _g('next')))

        try:
#            u = DBSession.query(User).filter(and_(User.active == 0, User.email.op('ilike')(_g('email')))).one()
            u = DBSession.query(User).filter(and_(User.active == 0, User.email == email)).one()
        except:
            _error(traceback.print_exc())
            flash(MSG_USER_NOT_EXIST, MESSAGE_WARNING)
            return redirect(url_for('bpRoot.view', action = 'login', next = _g('next')))
        else:
            if not u.validate_password(_g('password')):
                flash(MSG_WRONG_PASSWORD, MESSAGE_WARNING)
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

                apps = DBSession.query(AppObject).filter(and_(AppObject.active == 0,
                        AppObject.create_by_id == u.id)).order_by(AppObject.create_time)

                session['apps'] = [(app.id, unicode(app)) for app in apps]
                u.last_login = dt.now()
                session.permanent = True
                DBSession.commit()
                if _g('next') : return redirect(_g('next'))
                return redirect(url_for('bpConsoles.view', action = 'index'))


    def logout(self):
        session.pop('login', None)
        session.pop('user_profile', None)
        return redirect(url_for('bpRoot.view'))


    def upload(self):
        f = upload('upfile')
        if not f : return jsonify({
                                   'url' : '', 'title' : '', 'state' : 'ERROR',
                                   })

        return jsonify({
                        'url' : f.url ,
                        'title' : f.name,
                        'state' : 'SUCCESS',
                        })

bpRoot.add_url_rule('/', view_func = RootView.as_view('view'), defaults = {'action':'index'})
bpRoot.add_url_rule('/<action>', view_func = RootView.as_view('view'))
