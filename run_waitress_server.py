import os  
from waitress import serve  
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pizza.settings")  

application = get_wsgi_application()  

serve(application,port=os.environ["PORT"])