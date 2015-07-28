import sae
from app.views import app

application = sae.create_wsgi_app(app)