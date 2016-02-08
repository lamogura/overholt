# -*- coding: utf-8 -*-
"""
    overholt.factory
    ~~~~~~~~~~~~~~~~

    overholt factory module
"""

import os

from flask import Flask

from .core import db, mail
from .helpers import register_blueprints
from .middleware import HTTPMethodOverrideMiddleware
from .models import User, Role


def create_app(package_name, package_path, settings_override=None):
    """Returns a :class:`Flask` application instance configured with common
    functionality for the Overholt platform.

    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary of settings to override
    :param register_security_blueprint: flag to specify if the Flask-Security
                                        Blueprint should be registered. Defaults
                                        to `True`.
    """
    app = Flask(package_name, instance_relative_config=True)

    app.config.from_object('overholt.settings')
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(settings_override)

    db.init_app(app)
    mail.init_app(app)

    register_blueprints(app, package_name, package_path)

    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    return app