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
from sys2do.model.logic import AppObject

__all__ = ['bpConsoles']

bpConsoles = Blueprint('bpConsoles', __name__)

class ConsolesView(BasicView):

    @templated("consoles/index.html")
    def index(self):
        apps = DBSession.query(AppObject)\
            .filter(and_(AppObject.active == 0,
                    AppObject.create_by_id == session['user_profile']['id'])) \
            .order_by(AppObject.create_time)

        return {
                'apps' : apps,
                }



bpConsoles.add_url_rule('/', view_func = ConsolesView.as_view('view'), defaults = {'action':'index'})
bpConsoles.add_url_rule('/<action>', view_func = ConsolesView.as_view('view'))
