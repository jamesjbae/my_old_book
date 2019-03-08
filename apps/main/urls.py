from django.conf.urls import url
from django.contrib import admin

from django.conf import settings
from django.views.static import serve

from .import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^about$', views.about),
    url(r'^project$', views.project),
    url(r'^my_book_list/(?P<id>\d+)$', views.my_book_list),
    url(r'^upload_new_book$', views.upload_new_book),
    url(r'^process_new_book$', views.process_new_book),
    url(r'^reading_book$', views.reading_book),
    url(r'^reserve_book/(?P<id>\d+)$', views.reserve_book),
    url(r'^show_book_edit/(?P<id>\d+)$', views.show_book_edit),
    url(r'^show_book/(?P<id>\d+)$', views.show_book),
    url(r'^process_book_edit/(?P<id>\d+)$', views.process_book_edit),
    url(r'^cancel/(?P<id>\d+)$', views.cancel),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^book_view/(?P<id>\d+)$', views.book_view)
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root' : settings.MEDIA_ROOT,
        }),
    ]