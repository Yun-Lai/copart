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
    url(r'^ajax_get_models/', views.view_ajax_get_models_of_make),

    url(r'^ajax_get_vehicles/', views.ajax_lots_by_search),
    url(r'^ajax_vehicles/', views.ajax_lots_search),

    url(r'^api/test/', views.test, name='test'),
    url(r'^api/test1/', views.test1, name='test1'),
    url(r'^api/clear/', views.clear_cache, name='clear_cache'),
    url(r'^api/vechiletyps/', views.vehicle_types_api, name='vehicle_types_api'),
    url(r'^api/newarrivals/', views.new_arrivals_api, name='new_arrivals_api'),
    url(r'^api/filtereditems/', views.filtered_items_api, name='filtered_items_api'),
    url(r'^api/vehiclemakes/', views.vehicle_makes_api, name='vehicle_makes_api'),
    # url(r'^api/vehiclemakes/', views.all_vehicle_makes_api, name='all_vehicle_makes_api'),
    url(r'^api/allvehiclemakes/', views.all_vehicle_makes_api, name='all_vehicle_makes_api'),
    url(r'^api/locations/', views.locations_api, name='locations_api'),
    url(r'^api/years/', views.years_api, name='years_api'),
    url(r'^api/status/', views.status_api, name='status_api'),
    url(r'^api/getmodels/', views.get_models_of_make_api, name='get_models_of_make_api'),
    url(r'^api/lots_by_summary/', views.lots_by_summary_api, name='lots_by_summary_api'),

    url(r'^api/lots_paged_by_search/', views.lots_paged_by_search_api, name='lots_paged_by_search_api'),
    url(r'^api/lots_count_searched/', views.lots_count_searched_api, name='lots_count_searched_api'),
    url(r'^api/lots_by_summary_features/', views.lots_by_summary_api_features_make_model, name='lots_by_summary_api_features'),
    url(r'^api/lots_by_summary_make/', views.lots_by_summary_api_make, name='lots_by_summary_api_make'),
    url(r'^api/lots_by_summary_model/', views.lots_by_summary_api_model, name='lots_by_summary_api_model'),
    url(r'^api/lots_by_summary_year_location/', views.lots_by_summary_api_year_date, name='lots_by_summary_api_year_date'),
    url(r'^api/lots_by_summary_transmission/', views.lots_by_summary_api_transmission, name='lots_by_summary_api_transmission'),
    url(r'^api/lots_by_summary_fuel/', views.lots_by_summary_api_fuel, name='lots_by_summary_api_fuel'),
    url(r'^api/lots_by_summary_vehicle_damage/', views.lots_by_summary_api_vehicle_damage, name='lots_by_summary_api_vehicle_damage'),
    url(r'^api/lot_similar_with_lot/(?P<lot>[\w-]+)/', views.detail_api_similar, name='detail_api_similar'),
    url(r'^api/lot_info_with_lot/(?P<lot>[\w-]+)/', views.detail_api_info, name='detail_api_info'),
    url(r'^api/bid_info_with_lot/(?P<vin>[\w-]+)/', views.details_api_bid_info, name='details_api_bid_info'),
    url(r'^api/winning_bid_with_lot/(?P<lot>[\w-]+)/', views.details_api_winning_bid_info, name='details_api_winning_bid_info'),
    url(r'^api/get_chart_data/(?P<vin>[\w-]+)/', views.get_api_chart_data, name='get_api_chart_data'),
    url(r'^api/api_chart/', views.get_api_chart_data, name='get_api_chart_data'),
    url(r'^api/api_get_lot_vin/(?P<id>[\w-]+)/', views.get_api_lot_or_vin, name='get_api_lot_or_vin'),
    url(r'^api/api_filter_key/', views.api_filter_key, name='api_filter_key'),
]






