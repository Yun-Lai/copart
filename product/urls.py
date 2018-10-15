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

    url(r'^$', views.index, name='index_page'),
    url(r'^lots_by_type/(?P<vehicle_type>[\w-]+)/', views.lots_by_type, name='list_page_by_type'),
    url(r'^lots_by_make/(?P<vehicle_make>[\w-]+)/', views.lots_by_make, name='list_page_by_make'),
    url(r'^lots/', views.lot_list, name='list_page'),
    url(r'^lot/(?P<lot>[\w-]+)/$', views.detail, name='detail_page'),

    # url(r'^ajax_getimages/', csrf_exempt(views.ajax_getimages), name='ajax_getimages'),
    url(r'^ajax_get_lot/', views.view_ajax_get_lot),
    url(r'^ajax_get_makes/', views.view_ajax_get_makes_of_type),
    url(r'^ajax_get_models/', views.view_ajax_get_models_of_make),
]
