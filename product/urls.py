from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from product import views

urlpatterns = [
    url(r'^scrap_coparts/', views.view_scrap_copart_all),
    url(r'^scrap_copart/', views.view_scrap_copart),
    url(r'^scrap_iaai/', views.view_scrap_iaai),
    url(r'^scrap_auction/', views.view_scrap_auction),
    url(r'^scrap_filters_count/', views.view_scrap_filters_count),

    url(r'^$', views.index, name='index_page'),
    url(r'^lots_by_feature/(?P<feature>[\d]+)/', views.lots_by_feature, name='list_page_by_feature'),
    url(r'^lots_by_type/(?P<vehicle_type>[\w])/', views.lots_by_type, name='list_page_by_type'),
    url(r'^lots_by_make/(?P<vehicle_make>[\d]+)/', views.lots_by_make, name='list_page_by_make'),
    url(r'^lots_by_search/(?P<vehicle_type>[\w])/(?P<from_year>[\d]+)/(?P<to_year>[\d]+)/(?P<make>[\w]+)/(?P<model>.+)/',
        views.lots_by_search, name='list_page_by_search'),
    url(r'^lot/(?P<lot>[\w-]+)/$', views.detail, name='detail_page'),

    # url(r'^ajax_getimages/', csrf_exempt(views.ajax_getimages), name='ajax_getimages'),
    url(r'^ajax_get_lot/', views.view_ajax_get_lot),
    url(r'^ajax_get_makes/', views.view_ajax_get_makes_of_type),
    url(r'^ajax_get_models/', views.view_ajax_get_models_of_make),
]
