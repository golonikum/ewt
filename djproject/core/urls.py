from django.urls import re_path

from core import auth, config, entities, exercises, search

urlpatterns = [
    re_path(r'^ajax/get/(?P<entity>word|sentence|group|exercise)/$', entities.get_all, name='ajax_get_all'),
    re_path(r'^ajax/get/(?P<entity>word|sentence|group|exercise)/(?P<id>\d+)/$', entities.get, name='ajax_get'),
    re_path(r'^ajax/add/(?P<entity>word|sentence|group|exercise)/$', entities.add, name='ajax_add'),
    re_path(r'^ajax/update/(?P<entity>word|sentence|group|exercise)/(?P<id>\d+)/$', entities.update, name='ajax_update'),
    re_path(r'^ajax/remove/(?P<entity>word|sentence|group|exercise)/(?P<id>\d+)/$', entities.remove, name='ajax_remove'),
    re_path(r'^ajax/remove/(?P<entity>word|sentence|group|exercise)/$', entities.remove_some, name='ajax_remove_some'),
    re_path(r'^ajax/set_active/word/$', entities.set_words_active, name='ajax_set_words_active'),
    re_path(r'^ajax/set_inactive/word/$', entities.set_words_inactive, name='ajax_set_words_inactive'),
    re_path(r'^ajax/page/(?P<name>index|word|sentence|group|config|exercise)/$', entities.page, name='ajax_page'),

    re_path(r'^ajax/change/word/(?P<id>\d+)/(?P<what>synonyms|sentences|groups)/$', entities.change_word, name='ajax_change_word'),
    re_path(r'^ajax/change/(?P<who>sentence|group)/(?P<id>\d+)/words/$', entities.change_words, name='ajax_change_words'),
    re_path(r'^ajax/change/get/(?P<what>words|sentences|groups)/$', entities.change_get_entities, name='ajax_change_get_entities'),
]

urlpatterns += [
    re_path(r'^ajax/remove_all/$', config.remove_all, name='ajax_remove_all'),
    re_path(r'^ajax/import/csv/$', config.csv_import, name='ajax_csv_import'),
    re_path(r'^ajax/export/(?P<what>csv|html)/$', config.export, name='export'),
    re_path(r'^ajax/set/entities_per_page/$', config.set_entities_per_page, name='ajax_entities_per_page'),
]

urlpatterns += [
    re_path(r'^ajax/search/$', search.search, name='ajax_search'),
]

urlpatterns += [
    re_path(r'^ajax/exercise/(?P<id>\d+)/$', exercises.exercise, name='ajax_exercise'),
    re_path(r'^ajax/exercise/(?P<id>\d+)/records/$', exercises.get_records, name='ajax_get_records'),
]

urlpatterns += [
    re_path(r'^$', auth.index, name='index'),
    re_path(r'^logout/$', auth.exit, name='logout'),
]
