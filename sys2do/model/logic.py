# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2012-12-28
#  @author: CL.Lam
#  Description:
###########################################
'''
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Text
from sqlalchemy.orm import relation, backref, synonym
from sys2do.model import DeclarativeBase
from sys2do.model.auth import SysMixin
from system import UploadFile



class AppObject(DeclarativeBase, SysMixin):
    __tablename__ = 'app_object'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text, unique = True, nullable = False)
    desc = Column(Text)
    logo_id = Column(Integer, ForeignKey('system_upload_file.id'))
    logo = relation(UploadFile, primaryjoin = logo_id == UploadFile.id)
    version_code = Column(Integer, default = 1)
    version_name = Column(Text, default = '1.0.0')
    appfile_id = Column(Integer, ForeignKey('system_upload_file.id'))
    appfile = relation(UploadFile, primaryjoin = appfile_id == UploadFile.id)

    def __repr__(self): return self.name
    def __str__(self): return self.name
    def __unicode__(self): return self.name



class AppArticle(DeclarativeBase, SysMixin):
    __tablename__ = 'app_article'

    id = Column(Integer, autoincrement = True, primary_key = True)

    app_id = Column(Integer, ForeignKey('app_object.id'))
    app = relation(AppObject, backref = backref("article", order_by = id),
                        primaryjoin = "and_(AppObject.id == AppArticle.app_id, AppArticle.active == 0)")

    title = Column(Text)
    sub_title = Column(Text)
    desc = Column(Text)
    content = Column(Text)
    validate_date = Column(Text)
    status = Column(Integer, default = 0)
    seq = Column(Integer)


    def __repr__(self): return self.title
    def __str__(self): return self.title
    def __unicode__(self): return self.title
