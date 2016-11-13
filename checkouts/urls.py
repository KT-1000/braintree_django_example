from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from checkouts import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new_checkout, name='new_checkout'),
    # url(r'^(?P<transaction_id>\d+)/$', views.show_checkout, name='show_checkout'),
    # url(r'^checkouts/$', views.create_checkout, name='create_checkout'),
]
