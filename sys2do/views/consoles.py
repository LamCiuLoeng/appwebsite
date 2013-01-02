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
from sys2do.util.common import _g, _error, _gs
from sys2do.constant import MESSAGE_ERROR, MSG_USER_NOT_EXIST, \
    MSG_WRONG_PASSWORD, MSG_NO_APP_NAME, MSG_APP_NAME_DUPLICATED, \
    MSG_SERVER_ERROR, MSG_SAVE_SUCC, MESSAGE_INFO, MESSAGE_WARNING, \
    MSG_RECORD_NOT_EXIST, MSG_DELETE_SUCC, MSG_UPDATE_SUCC, MSG_NO_ID_SUPPLIED, \
    MSG_NO_ENOUGH_PARAMS
from sys2do.model.logic import AppObject, AppArticle

__all__ = ['bpConsoles']

bpConsoles = Blueprint('bpConsoles', __name__)

class ConsolesView(BasicView):

    template_dir = 'consoles'


    @templated()
    def index(self):
        apps = DBSession.query(AppObject)\
            .filter(and_(AppObject.active == 0,
                    AppObject.create_by_id == session['user_profile']['id'])) \
            .order_by(AppObject.create_time)

        return {
                'apps' : apps,
                }


    @templated()
    def createApp(self):
        pass

    def saveNewApp(self):
        appName, appDesc = _gs('appName', 'appDesc')
        if not appName:
            flash(MSG_NO_APP_NAME, MESSAGE_WARNING)
            return redirect(url_for('.view', action = 'createApp'))
        try:
            DBSession.query(AppObject).filter(and_(AppObject.active == 0,
                                            AppObject.name == appName)).one()
        except:
            try:
                DBSession.add(AppObject(
                                        name = appName,
                                        desc = appDesc
                                        ))
                DBSession.commit()
                flash(MSG_SAVE_SUCC, MESSAGE_INFO)
                return redirect(url_for('.view'))
            except:
                DBSession.rollback()
                flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
                return redirect(url_for('.view'))
        else:
            flash(MSG_APP_NAME_DUPLICATED, MESSAGE_WARNING)
            return redirect(url_for('.view', action = 'createApp'))


    @templated()
    def updateApp(self):
        appid = _g('id')
        try:
            app = DBSession.query(AppObject).filter(and_(AppObject.id == appid,
                AppObject.create_by_id == session['user_profile']['id'])).one()
        except:
            flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
            return redirect(url_for('.view'))
        return {
                'app' : app
                }


    def saveApp(self):
        appid, appDesc = _gs('id', 'appDesc')
        try:
            app = DBSession.query(AppObject).filter(and_(AppObject.id == appid,
                AppObject.create_by_id == session['user_profile']['id'])).one()
        except:
            flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
            return redirect(url_for('.view'))

        try:
            app.desc = appDesc
            DBSession.commit()
            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
        except:
            DBSession.rollback()
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
        return redirect(url_for('.view'))


    def delApp(self):
        appid = _g('id')
        try:
            app = DBSession.query(AppObject).filter(and_(AppObject.id == appid,
                AppObject.create_by_id == session['user_profile']['id'])).one()
        except:
            flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
            return redirect(url_for('.view'))
        try:
            app.active = 1
            DBSession.commit()
            flash(MSG_DELETE_SUCC, MESSAGE_INFO)
        except:
            DBSession.rollback()
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
        return redirect(url_for('.view'))


    @templated()
    def listArticle(self):
        appid = _g('appid')
        try:
            app = DBSession.query(AppObject).filter(and_(AppObject.id == appid,
                AppObject.create_by_id == session['user_profile']['id'])).one()
        except:
            flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
            return redirect(url_for('.view'))

        articles = DBSession.query(AppArticle).filter(and_(AppArticle.active == 0,
                AppArticle.app_id == appid)).order_by(AppArticle.seq)

        return {
                'app' : app,
                'articles' : articles
                }


    @templated()
    def createArticle(self):
        return {
                'appid' : _g('appid'),
                }


    def saveNewArticle(self):
        appid, title, sub_title, validate_date, desc, content = _gs('appid', 'title', 'sub_title', 'validate_date', 'desc', 'content')
        if not appid :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_WARNING)
            return redirect(url_for('.view'))

        if not title:
            flash(MSG_NO_ENOUGH_PARAMS, MESSAGE_WARNING)
            return redirect(url_for('.view', action = 'createArticle', appid = appid))

        try:
            article = AppArticle(
                             app_id = appid,
                             title = title,
                             sub_title = sub_title,
                             desc = desc,
                             content = content,
                             validate_date = validate_date,
                             )
            DBSession.add(article)
            DBSession.flush()
            article.seq = article.id
            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for(".view", action = "listArticle", appid = appid))
        except:
            DBSession.rollback()
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            traceback.print_exc()
            return redirect(url_for(".view", action = "listArticle", appid = appid))


    @templated()
    def updateArticle(self):
        aid = _g('id')
        if not aid :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_WARNING)
            return redirect(url_for('.view'))

        article = DBSession.query(AppArticle).get(aid)
        return {
                'article' : article,
                }



    def saveArticle(self):
        aid, title, sub_title, validate_date, desc, content = _gs('id', 'title', 'sub_title', 'validate_date', 'desc', 'content')
        if not aid :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_WARNING)
            return redirect(url_for('.view'))

        if not title:
            flash(MSG_NO_ENOUGH_PARAMS, MESSAGE_WARNING)
            return redirect(url_for('.view', action = 'updateArticle', id = aid))
        try:
            article = DBSession.query(AppArticle).get(aid)
            article.title = title
            article.sub_title = sub_title
            article.validate_date = validate_date
            article.desc = desc
            article.content = content
            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'listArticle', appid = article.app_id))
        except:
            DBSession.rollback()
            traceback.print_exc()
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            return redirect(url_for('.view', action = 'updateArticle', id = aid))


    def delArticle(self):
        aid = _g('id')
        if not aid :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_WARNING)
            return redirect(url_for('.view'))
        try:
            article = DBSession.query(AppArticle).get(aid)
            article.active = 1
            DBSession.commit()
            flash(MSG_DELETE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'listArticle', appid = article.app_id))
        except:
            DBSession.rollback()
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            return redirect(url_for('.view', action = 'updateArticle', id = aid))


bpConsoles.add_url_rule('/', view_func = ConsolesView.as_view('view'), defaults = {'action':'index'})
bpConsoles.add_url_rule('/<action>', view_func = ConsolesView.as_view('view'))
