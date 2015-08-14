from django.conf.urls import url
from finder.views import search, preview

urlpatterns = [
    url(r'^$', search),
    url(r'^preview/(?P<doc_id>[\d\w_\-]+)$', preview, name='preview'),
]
