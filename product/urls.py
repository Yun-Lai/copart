from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from product import views

urlpatterns = [
    url(r'^scrap_coparts/', views.view_scrap_copart_all),
    url(r'^scrap_copart/', views.view_scrap_copart),
    url(r'^scrap_iaai/', views.view_scrap_iaai),
    url(r'^scrap_auction/', views.view_scrap_auction),
    url(r'^scrap_filters_count/', views.view_scrap_filters_count),
    url(r'^scrap_not_exist/', views.view_scrap_not_exist),
    url(r'^email_test/', views.view_send_vin_error),
    url(r'^find_correct_vin/', views.view_find_correct_vin),
    url(r'^remove_unavailable_lots/', views.view_remove_unavailable_lots),

    url(r'^$', views.index, name='index_page'),
    url(r'^lots_by_search/', views.lots_by_search, name='list_page_by_search'),
    url(r'^lots_search/', views.lots_search, name='list_page_search'),
    url(r'^lot/(?P<lot>[\w-]+)/$', views.detail, name='detail_page'),

    # url(r'^ajax_getimages/', csrf_exempt(views.ajax_getimages), name='ajax_getimages'),
    url(r'^ajax_get_lot/', views.view_ajax_get_lot),
    url(r'^ajax_get_makes/', views.view_ajax_get_makes_of_type),
    url(r'^ajax_get_models/', views.view_ajax_get_models_of_make),

    url(r'^ajax_get_vehicles/', views.ajax_lots_by_search),
    url(r'^ajax_vehicles/', views.ajax_lots_search),
]
