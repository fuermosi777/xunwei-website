from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^froala_editor/', include('froala_editor.urls')),
)

urlpatterns += patterns('web.views',
    url(r'^$', 'home'),
    url(r'^post/(?P<post_id>[0-9]+)/$', 'post'),
    url(r'^business/(?P<business_id>[0-9]+)/$', 'business'),
    url(r'^tag/(?P<tag_name>\w+)/$', 'tag'),
    url(r'^area/(?P<area_name>\w+)/$', 'area'),

    url(r'^restaurant/(?P<restaurant>\w+)/$', 'old'),
    url(r'^search/', 'old'),

    # user
    url(r'^secret/$', TemplateView.as_view(template_name='base.html')),
)

urlpatterns += patterns('api.views',
    url(r'^api/business_list/$', 'business_list'),
    url(r'^api/business/$', 'business'),
    url(r'^api/post_list/$', 'post_list'),
    url(r'^api/post/$', 'post'),
    url(r'^api/tag_list/$', 'tag_list'),

    # self admin use
    url(r'^api/upload_image/$', 'upload_image'),
    url(r'^api/upload_image_url/$', 'upload_image_url'),
    url(r'^api/add_post/$', 'add_post'),
    url(r'^api/secret_add_post/$', 'secret_add_post'),
    url(r'^api/star_post/$', 'star_post'),
    url(r'^api/post/star/$', 'post_star'),
)

urlpatterns += patterns('api.auth',
    url(r'^api/auth/check_user_exist/$', 'check_user_exist'),
    url(r'^api/auth/check_status/$', 'check_status'),
    url(r'^api/auth/login/$', 'login'),
    url(r'^api/auth/signup/$', 'signup'),
)

urlpatterns += patterns('api.robot',
    url(r'^robot/post/$', 'post'),
    url(r'^robot/business/$', 'business'),
)