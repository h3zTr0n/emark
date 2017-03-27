from __future__ import absolute_import
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from itemstuff.views import search
from itemstuff.views import getItem
from itemstuff.views import browseCategory
from accountstuff.views import getProfile
from accountstuff.views import follow
from accountstuff.views import unfollow

from djangosite.views import handler404
from djangosite.views import handler500

from djangosite.views import home
from djangosite.views import about

urlpatterns = [
    # Examples:
    # url(r'^$', 'djangosite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', home, name="home"),
    url(r'^about/$', about, name="about"),

    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
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

    url(r'^browse/(?P<category>.+)/$',  browseCategory, name="browseCategory"),
    #url(r'^user/settings/$', 'accountstuff.views.settings2', name="getSettings"),
    url(r'^user/(?P<username>[A-Za-z0-9]+)/$',  getProfile, name="getProfile"),
    url(r'^user/follow/(?P<username>[A-Za-z0-9]+)/$', follow, name = "follow"),
    url(r'^user/unfollow/(?P<username>[A-Za-z0-9]+)/$',  unfollow, name = "unfollow"),
    url(r'^user/(?P<username>[A-Za-z0-9]+)/(?P<itemid>.+)$', getItem, name="getItem"),

    url(r'^search/$', search, name="search"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = handler404
handler500 = handler500
