from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^$', views.index, name='landing'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^travels$', views.travels, name='dashboard'),
    url(r'^add$', views.add,name='add'), 
    url(r'^create$', views.create, name='create'),  
    url(r'^delete$',views.delete, name='delete'),  
    url(r'^join/(?P<travel_id>\d+)$', views.join, name='join'),
    url(r'^unjoin$', views.unjoin, name='unjoin'),
    url(r'^show/(?P<travel_id>\d+)$', views.show, name='show'), 
    url(r'^logout$', views.logout, name='logout'),
    ] 