from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from product import views

urlpatterns = [
    url(r'^scrap_copart/', views.scrap_copart),
    url(r'^scrap_coparts/', views.scrap_coparts),
    url(r'^scrap_iaai/', views.scrap_iaai),
    url(r'^scrap_auction/', views.scrap_auction),

    url(r'^ajax_getimages/', csrf_exempt(views.ajax_getimages), name='ajax_getimages'),

    url(r'^$', views.index, name='index_page'),
    url(r'^lots/', views.lot_list, name='list_page'),
    url(r'^lot/(?P<lot>[\w-]+)/$', views.detail, name='detail_page'),
]
