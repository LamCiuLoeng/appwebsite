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



class AppObject(DeclarativeBase, SysMixin):
    __tablename__ = 'app_object'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text, unique = True, nullable = False)
    desc = Column(Text)



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
