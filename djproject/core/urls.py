from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^ajax/get/(?P<entity>word|sentence|group|exercise)/$', 'core.entities.get_all', name='ajax_get_all'),
    url(r'^ajax/get/(?P<entity>word|sentence|group|exercise)/(?P<id>\d+)/$', 'core.entities.get', name='ajax_get'),
    url(r'^ajax/add/(?P<entity>word|sentence|group|exercise)/$', 'core.entities.add', name='ajax_add'),
    url(r'^ajax/update/(?P<entity>word|sentence|group|exercise)/(?P<id>\d+)/$', 'core.entities.update', name='ajax_update'),
    url(r'^ajax/remove/(?P<entity>word|sentence|group|exercise)/(?P<id>\d+)/$', 'core.entities.remove', name='ajax_remove'),
    url(r'^ajax/remove/(?P<entity>word|sentence|group|exercise)/$', 'core.entities.remove_some', name='ajax_remove_some'),
    url(r'^ajax/set_active/word/$', 'core.entities.set_words_active', name='ajax_set_words_active'),
    url(r'^ajax/set_inactive/word/$', 'core.entities.set_words_inactive', name='ajax_set_words_inactive'),
    url(r'^ajax/page/(?P<name>index|word|sentence|group|config|exercise)/$', 'core.entities.page', name='ajax_page'),

    url(r'^ajax/change/word/(?P<id>\d+)/(?P<what>synonyms|sentences|groups)/$', 'core.entities.change_word', name='ajax_change_word'),
    url(r'^ajax/change/(?P<who>sentence|group)/(?P<id>\d+)/words/$', 'core.entities.change_words', name='ajax_change_words'),
    url(r'^ajax/change/get/(?P<what>words|sentences|groups)/$', 'core.entities.change_get_entities', name='ajax_change_get_entities'),
)

urlpatterns += patterns('',
    url(r'^ajax/remove_all/$', 'core.config.remove_all', name='ajax_remove_all'),
    url(r'^ajax/import/csv/$', 'core.config.csv_import', name='ajax_csv_import'),
    url(r'^ajax/export/(?P<what>csv|html)/$', 'core.config.export', name='export'),
    url(r'^ajax/set/entities_per_page/$', 'core.config.set_entities_per_page', name='ajax_entities_per_page'),
)

urlpatterns += patterns('',
    url(r'^ajax/search/$', 'core.search.search', name='ajax_search'),
)

urlpatterns += patterns('',
    url(r'^ajax/exercise/(?P<id>\d+)/$', 'core.exercises.exercise', name='ajax_exercise'),
    url(r'^ajax/exercise/(?P<id>\d+)/records/$', 'core.exercises.get_records', name='ajax_get_records'),
)

urlpatterns += patterns('',
    url(r'^$', 'core.auth.index', name='index'),
    url(r'^logout/$', 'core.auth.exit', name='logout'),
)
