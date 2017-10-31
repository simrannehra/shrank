from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

app_name = 'urlshort'

urlpatterns = [
    url(r'^(?P<url_id>[\w\-]+)/$',views.test,name='test'),
    url(r'^$', views.index, name = 'suceess'),
    url(r'^account/register/$',views.UserFormView.as_view(),name='register'),
    url(r'^account/login/$',views.LoginFormView.as_view(),name='login'),
    url(r'^account/logout/$',views.user_logout,name='logout'),
    url(r'^account/records/$',views.record,name='records'),
]

#the end
