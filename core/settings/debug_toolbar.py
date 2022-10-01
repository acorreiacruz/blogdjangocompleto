from .installed_apps import INSTALLED_APPS
from .middlewares import MIDDLEWARE
import mimetypes


# Solving the problem of not showing Django Debug Toolbar
mimetypes.add_type("application/javascript", ".js", True)

INSTALLED_APPS += ['debug_toolbar',]

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware',] + MIDDLEWARE

INTERNAL_IPS = [
    '127.0.0.1'
]