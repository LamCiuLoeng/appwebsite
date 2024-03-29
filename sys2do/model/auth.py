# -*- coding: utf-8 -*-

import traceback
from datetime import datetime as dt, date
import os
import sys
from sqlalchemy.sql.expression import desc, and_
from sys2do.constant import SYSTEM_DATETIME_FORMAT, SYSTEM_DATE_FORMAT
from sqlalchemy.ext.declarative import declared_attr




try:
    from hashlib import sha1
except ImportError:
    sys.exit('ImportError: No module named hashlib\n'
             'If you are on python2.4 this library is not part of python. '
             'Please install it. Example: easy_install hashlib')



from flask import session
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, DateTime, Text
from sqlalchemy.orm import relation, synonym, backref
from sys2do.model import DeclarativeBase, metadata, DBSession


__all__ = ['User', 'Group', 'Permission', 'SysMixin', ]



def getUserID():
    try:
        return session['user_profile']['id']
    except:
        return None


class SysMixin(object):
    create_time = Column(DateTime, default = dt.now)
    create_by_id = Column(Integer, default = getUserID)
    update_time = Column(DateTime, default = dt.now, onupdate = dt.now)
    update_by_id = Column(Integer, default = getUserID, onupdate = getUserID)
    active = Column(Integer, default = 0)  # 0 is active ,1 is inactive


    @property
    def create_by(self):
        try:
            return DBSession.query(User).get(self.create_by_id)
        except:
            return None

    @property
    def update_by(self):
        try:
            return DBSession.query(User).get(self.update_by_id)
        except:
            return None


# { Association tables


# This is the association table for the many-to-many relationship between
# groups and permissions. This is required by repoze.what.
group_permission_table = Table('system_group_permission', metadata,
    Column('group_id', Integer, ForeignKey('system_group.id',
        onupdate = "CASCADE", ondelete = "CASCADE"), primary_key = True),
    Column('permission_id', Integer, ForeignKey('system_permission.id',
        onupdate = "CASCADE", ondelete = "CASCADE"), primary_key = True)
)

# This is the association table for the many-to-many relationship between
# groups and members - this is, the memberships. It's required by repoze.what.
user_group_table = Table('system_user_group', metadata,
    Column('user_id', Integer, ForeignKey('system_user.id',
        onupdate = "CASCADE", ondelete = "CASCADE"), primary_key = True),
    Column('group_id', Integer, ForeignKey('system_group.id',
        onupdate = "CASCADE", ondelete = "CASCADE"), primary_key = True)
)


# { The auth* model itself


class Group(DeclarativeBase, SysMixin):
    __tablename__ = 'system_group'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text, unique = True, nullable = False)
    desc = Column(Text)
    users = relation('User', secondary = user_group_table, backref = 'groups')

    def __repr__(self): return self.name
    def __str__(self): return self.name
    def __unicode__(self): return self.name

    def populate(self):
        return {
                "id" : self.id,
                "name" :self.name,
                "desc" : self.desc,
                }



# The 'info' argument we're passing to the email_address and password columns
# contain metadata that Rum (http://python-rum.org/) can use generate an
# admin interface for your models.
class User(DeclarativeBase, SysMixin):
    __tablename__ = 'system_user'

    id = Column(Integer, autoincrement = True, primary_key = True)
#    name = Column(Text, unique = True, nullable = False)
    email = Column(Text, unique = True, nullable = False)
    _password = Column('password', Text)

    mobile = Column(Text)
    image_url = Column(Text)
    last_login = Column(DateTime, default = dt.now)

    def __repr__(self): return self.email
    def __str__(self): return self.email
    def __unicode__(self): return self.email


    @property
    def permissions(self):
        """Return a set of strings for the permissions granted."""
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

    @classmethod
    def by_email_address(cls, email):
        """Return the user object whose email address is ``email``."""
        return DBSession.query(cls).filter(cls.email == email).first()

#
#    def validate_password(self, password):
#        return self.password == password


    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        hashed_password = password

        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password

        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(password_8bit + salt.hexdigest())
        hashed_password = salt.hexdigest() + hash.hexdigest()

        # Make sure the hashed password is an UTF-8 object at the end of the
        # process because SQLAlchemy _wants_ a unicode object for Unicode
        # columns
        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')

        self._password = hashed_password

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym('_password', descriptor = property(_get_password, _set_password))

    # }

    def validate_password(self, password):
        """
        Check the password against existing credentials.

        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool

        """
        hashed_pass = sha1()
        hashed_pass.update(password + self.password[:40])
        return self.password[40:] == hashed_pass.hexdigest()


#    @classmethod
#    def identify(cls, value):
#        return DBSession.query(cls).filter(cls.user_name.match(value)).one()

    def populate(self):
        return {
                'id' : self.id,
#                'name' : self.name,
                'password' : self.password,
                'email' : self.email,
                'image_url' : self.image_url,
                }



class Permission(DeclarativeBase, SysMixin):
    __tablename__ = 'system_permission'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text, unique = True, nullable = False)
    desc = Column(Text)
    groups = relation(Group, secondary = group_permission_table, backref = 'permissions')

    def __repr__(self): return self.name
    def __str__(self): return self.name
    def __unicode__(self): return self.name
    def populate(self):  return {"id" : self.id , "name" : self.name, 'desc' : self.desc}




