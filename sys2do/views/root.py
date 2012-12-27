# -*- coding: utf-8 -*-
from flask import current_app as app
from flask import g, render_template, flash, session, redirect, url_for, request
from flask.blueprints import Blueprint

from sys2do.views import BasicView
from sys2do.util.decorator import templated

__all__ = ['bpRoot']

bpRoot = Blueprint('bpRoot', __name__)

class RootView(BasicView):

    @templated("index.html")
    def index(self):
        return {}


bpRoot.add_url_rule('/', view_func = RootView.as_view('view'), defaults = {'action':'index'})
bpRoot.add_url_rule('/<action>', view_func = RootView.as_view('view'))
