from werkzeug.middleware.proxy_fix import ProxyFix

from blog import create_app

app = create_app()

app.wsgi_app = ProxyFix(app.wsgi_app)
