from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djangosite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$','djangosite.views.home',name="home"),
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^browseCategory','djangosite.views.browseCategory',name="browseCategory"),
    #url(r'^browseTag','djangosite.views.browseTag',name="browseTag"),
    #url(r'^itemListing','djangosite.views.itemListing',name="itemListing"),
    #url(r'^search','djangosite.views.search',name="search"),
    #url(r'^shoppingCart','djangosite.views.shoppingCart',name="shoppingCart"),

    url(r'^acc/', include('accountstuff.urls')),
    url(r'^item/', include('itemstuff.urls')),
    url(r'^msg/', include('messagestuff.urls')),
    url(r'^cart/', include('shoppingcart.urls')),

    url(r'^browse/(?P<category>.+)/$', 'itemstuff.views.browseCategory', name="browseCategory"),
    #url(r'^user/settings/$', 'accountstuff.views.settings2', name="getSettings"),
    url(r'^user/(?P<username>[A-Za-z0-9]+)/$', 'accountstuff.views.getProfile', name="getProfile"),
    url(r'^user/(?P<username>[A-Za-z0-9]+)/(?P<itemid>.+)$', 'itemstuff.views.getItem', name="getItem"),
    url(r'^search/$', 'itemstuff.views.search', name="search"),
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
