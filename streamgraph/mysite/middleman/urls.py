from django.conf.urls import patterns, include, url
#from middleman.views import AboutView
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'middleman.views.hello_world', name='hello_world'),
    #url(r'^$', AboutView.as_view()),
    #url(r'^$', 'middleman.views.test', name='test'),
    
    #url(r'^middleman/', include('middleman.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()