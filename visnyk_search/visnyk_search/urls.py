from django.conf.urls import url
from finder.views import search

urlpatterns = [
    url(r'^$', search),
]
