# -*- coding: utf-8 -*-
from functools import wraps
from flask import request, redirect, url_for, render_template, session, flash

__all__ = ['templated', 'login_required' ]

def templated(template = None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
#                template_name = request.endpoint.replace('.', '/') + '.html'
                template_name = "%s.html" % f.__name__
                _self = args[0]
                if getattr(_self, 'template_dir', None):
                    template_name = '%s/%s' % (_self.template_dir, template_name)

            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx

            return render_template(template_name, **ctx)
        return decorated_function
    return decorator


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('login', None):
            return redirect(url_for('bpRoot.login', next = request.url))
        return f(*args, **kwargs)
    return decorated_function
