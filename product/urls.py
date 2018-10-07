from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from product import views

urlpatterns = [
    url(r'^scrap_coparts/', views.view_scrap_copart_all),
    url(r'^scrap_copart/', views.view_scrap_copart),
    url(r'^scrap_iaai/', views.view_scrap_iaai),
    url(r'^scrap_auction/', views.view_scrap_auction),
    url(r'^scrap_type_lot/', views.view_scrap_type_lot),
    url(r'^scrap_make_lot/', views.view_scrap_make_lot),

    url(r'^ajax_getimages/', csrf_exempt(views.ajax_getimages), name='ajax_getimages'),

    url(r'^$', views.index, name='index_page'),
    url(r'^lots/', views.lot_list, name='list_page'),
    url(r'^lot/(?P<lot>[\w-]+)/$', views.detail, name='detail_page'),
]
