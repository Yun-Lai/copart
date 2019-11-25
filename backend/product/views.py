from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Count, CharField, Value, F, Avg, Max, Min, Sum
from django.forms.models import model_to_dict
from django.db.models.functions import Cast, ExtractDay, ExtractMonth, ExtractYear, Concat
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from urllib.parse import urlencode

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

from product.tasks import *
from product.utils import filter_by_filters, set_filters_with_featured_name

from copart import settings
from urllib.parse import parse_qs
import requests
import asyncio
from threading import Thread

from subprocess import Popen
from sys import stdout, stdin, stderr

contents = open('/code/host_ip.txt').read()
host = contents[:-1]


def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator


def test1(request):

    filepath = 'urls.txt'
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            url = fp.readline()
            url = url[:-1]
            params = parse_qs(url)
            if url is not '':
                generating_cache(params)
                # generate_cache.delay(host, params)
                # keylist = params.keys()
                # for key in keylist:
                #     params[key] = params[key][0]
                # if 'status' in params:
                #     del params['status']
                # params['page'] = 1
                # params['entry'] = 20
                # query = urlencode(params).replace('%2C', ',').replace('%3A', ':')
                # generate_cache.delay('http://' + host + '/api/api_filter_key/?' + query)
                # generate_cache.delay('http://' + host + '/api/lots_paged_by_search/?' + query)
                #
                # if 'sort' in params:
                #     del params['sort']
                # del params['page']
                # del params['entry']
                # query = urlencode(params).replace('%2C', ',').replace('%3A', ':')
                # generate_cache.delay('http://' + host + '/api/lots_count_searched/?' + query)
                # generate_cache.delay('http://' + host + '/api/lots_by_summary_features/?' + query)
                # generate_cache.delay('http://' + host + '/api/lots_by_summary_year_location/?' + query)
                # generate_cache.delay('http://' + host + '/api/lots_by_summary_vehicle_damage/?' + query)
                # generate_cache.delay('http://' + host + '/api/lots_by_summary_fuel/?' + query)
                # generate_cache.delay('http://' + host + '/api/lots_by_summary_transmission/?' + query)
            else:
                break

    return JsonResponse({"url":  'query'})


@start_new_thread
def generating_cache(params):
    keylist = params.keys()
    for key in keylist:
        params[key] = params[key][0]
    if 'status' in params:
        del params['status']
    params['page'] = 1
    params['entry'] = 20
    query = urlencode(params).replace('%2C', ',').replace('%3A', ':')
    requests.get('http://' + host + '/api/api_filter_key/?' + query)
    requests.get('http://' + host + '/api/lots_paged_by_search/?' + query)

    if 'sort' in params:
        del params['sort']
    del params['page']
    del params['entry']
    query = urlencode(params).replace('%2C', ',').replace('%3A', ':')
    requests.get('http://' + host + '/api/lots_count_searched/?' + query)
    requests.get('http://' + host + '/api/lots_by_summary_features/?' + query)
    requests.get('http://' + host + '/api/lots_by_summary_year_location/?' + query)
    requests.get('http://' + host + '/api/lots_by_summary_vehicle_damage/?' + query)
    requests.get('http://' + host + '/api/lots_by_summary_fuel/?' + query)
    requests.get('http://' + host + '/api/lots_by_summary_transmission/?' + query)


def clear_cache(request):
    command = 'python manage.py clear_cache'
    proc = Popen(command, shell=True, stdin=stdin, stdout=stdout, stderr=stderr)
    return JsonResponse({"url": 'query'})


@login_required
def view_scrap_copart_all(request):
    scrap_copart_all.delay()

    return redirect('/' + settings.COPART_ADMIN_URL)


@login_required
def view_scrap_copart(request):
    make_id = request.GET.get('id')
    scrap_copart_lots.delay([make_id], {'username': 'tatermaz@gmail.com', 'password': '54TrAp34fY'})

    return redirect('/' + settings.COPART_ADMIN_URL + 'product/vehiclemakes/')


@login_required
def view_scrap_iaai(request):
    scrap_iaai_lots.delay()

    return redirect('/' + settings.COPART_ADMIN_URL)


@login_required
def view_scrap_auction(request):
    scrap_live_auctions.delay()

    return redirect('/' + settings.COPART_ADMIN_URL)


@login_required
def view_scrap_filters_count(request):
    scrap_filters_count.delay()

    return redirect('/' + settings.COPART_ADMIN_URL)


@login_required
def view_scrap_not_exist(request):
    scrap_not_exist_lots.delay()

    return redirect('/' + settings.COPART_ADMIN_URL)


@login_required
def view_send_vin_error(request):
    send_vin_error.delay('4T1FA38P56U******', 24095729)

    return redirect('/' + settings.COPART_ADMIN_URL)


@login_required
def view_find_correct_vin(request):
    find_correct_vin.delay()

    return redirect('/' + settings.COPART_ADMIN_URL)


@login_required
def view_remove_unavailable_lots(request):
    remove_unavailable_lots.delay()

    return redirect('/' + settings.COPART_ADMIN_URL)


def view_404(request, **kwargs):
    return redirect('/')


def ajax_getimages(request):
    lot_id = request.POST.get('lot', '')

    if not lot_id:
        return JsonResponse({'result': False})

    lot = VehicleInfo.objects.get(lot=int(lot_id))
    if lot.source:
        images = ['https://cs.copart.com/v1/AUTH_svc.pdoc00001/' + a for a in lot.images.split('|')]
        thumb_images = ['https://cs.copart.com/v1/AUTH_svc.pdoc00001/' + a for a in lot.thumb_images.split('|')]
    else:
        images = ['https://vis.iaai.com:443/resizer?imageKeys=%s&width=640&height=480' % a for a in
                  lot.images.split('|')]
        thumb_images = ['https://vis.iaai.com:443/resizer?imageKeys=%s&width=128&height=96' % a for a in
                        lot.images.split('|')]

    return JsonResponse({
        'result': True,
        'lot_name': lot.name,
        'lot': lot.lot,
        'images': images,
        'thumb_images': thumb_images,
    })


def view_ajax_get_lot(request):
    vin_or_lot = request.GET.get('vin_or_lot', '')
    vin_or_lot = vin_or_lot.strip()
    if 8 == len(vin_or_lot) and vin_or_lot.isnumeric():
        if VehicleInfo.objects.filter(lot=int(vin_or_lot)).exists():
            return JsonResponse({'result': True, 'lot': vin_or_lot})
        else:
            return JsonResponse({'result': False})
    lot = VehicleInfo.objects.filter(vin=vin_or_lot).order_by('-id')
    if len(lot):
        return JsonResponse({'result': True, 'lot': lot[0].lot})
    return JsonResponse({'result': False})


def view_ajax_get_models_of_make(request):
    finder_type = request.GET.get('finder_type', '')
    finder_make = request.GET.get('finder_make', '')
    vehicle_makes = VehicleInfo.objects.filter(type=finder_type).filter(
        make__icontains=finder_make).values_list('model', flat=True)
    vehicle_makes = sorted(list(set(vehicle_makes)))
    return JsonResponse({
        'result': True,
        'models': [a for a in vehicle_makes],
    })


def index(request):
    new_arrivals = VehicleInfo.objects.filter(~Q(retail_value=0)).order_by('-id')[:12]
    featured_filters = Filter.objects.filter(type='F')
    vehicle_types = Filter.objects.filter(type='T')
    vehicle_makes = Filter.objects.filter(type='M').order_by('-count')[:55]
    vehicle_all_makes = list(VehicleMakes.objects.values())
    locations = Location.objects.all()

    context = {
        'arrivals': new_arrivals,
        'featured_filters': featured_filters,
        'vehicle_types': vehicle_types,
        'vehicle_makes': vehicle_makes,
        'vehicle_all_makes': vehicle_all_makes,
        'locations': locations,
        'year_range': range(1920, datetime.datetime.now().year + 2)[::-1],
        'status': '&status=%5B%27Sites%27,%20%27Already%20Sold%27,%20%27Featured%20Items%27,%20%27Make%27%5D',
    }
    return render(request, 'product/index.html', context=context)


def lots_by_search(request):
    if not request.GET:
        return redirect('/')

    # get params from url
    vehicle_type = request.GET.get('type', '')
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')
    location = request.GET.get('location', '')
    params_ = request.GET.get('params', '')
    status = request.GET.get('status', '')
    feature = request.GET.get('feature', '')
    sort_ = request.GET.get('sort', '')

    if sort_:
        sort = eval(sort_)
        sort['sort_by'] = 'info__' + sort['sort_by']
    else:
        sort = dict(sort_by='info__year', sort_type='desc')

    sort_direction = ''
    if 'desc' == sort['sort_type']:
        sort_direction = '-'

    initial_status = []
    filter_word = []
    if vehicle_type:
        initial_status.append('type=' + vehicle_type)
        filter_word.append(dict(TYPES)[vehicle_type])
    if year:
        initial_status.append('year=' + year)
    if feature:
        initial_status.append('feature=' + feature)

    params = {}
    # check if 'Show Real Price' checked
    sold = False
    if params_:
        params = eval(params_)
        if 'sold' in params and 'yes' == params['sold']:
            sold = True

    lots = VehicleSold.objects if sold else Vehicle.objects
    lots_sold = VehicleSold.objects
    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filter_word.append(featured_filter.name)
        if 'Buy It Now' == featured_filter.name:
            lots = lots.filter(~Q(buy_today_bid=0))
        elif 'Pure Sale Items' == featured_filter.name:
            lots = lots.filter(~Q(bid_status='PURE SALE'))
        elif 'New Items' == featured_filter.name:
            cur_date = datetime.datetime.now().date()
            from_date = cur_date - datetime.timedelta(days=cur_date.weekday() + 7)
            to_date = from_date + datetime.timedelta(days=6)
            lots = lots.filter(created_at__range=(from_date, to_date))
        elif 'Lots with Bids' == featured_filter.name:
            lots = lots.filter(~Q(current_bid=0))
        elif 'No Bids Yet' == featured_filter.name:
            lots = lots.filter(current_bid=0)
        elif 'Hybrid Vehicles' == featured_filter.name:
            lots = lots.filter(info__fuel="HYBRID ENGINE")
        elif 'Repossessions' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='B')
        elif 'Donations' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='D').filter(~Q(lot_highlights="Did Not Test Start"))
        elif 'Featured Vehicles' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='F')
        elif 'Offsite Sales' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='O')
        elif 'Run and Drive' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='R')
        elif 'Clean Title' == featured_filter.name:
            lots = lots.filter(~Q(info__doc_type_td__icontains='salvage'))
        elif 'Salvage Title' == featured_filter.name:
            lots = lots.filter(info__doc_type_td__icontains='salvage')
        elif 'Front End' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Front End') or Q(info__2nd_damage__icontains='Front End'))
        elif 'Hail Damage' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Hail') or Q(info__lot_2nd_damage__icontains='Hail'))
        elif 'Normal Wear' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Normal Wear') or Q(info__lot_2nd_damage__icontains='Normal Wear'))
        elif 'Minor Dents/Scratch' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Minor') or Q(info__lot_2nd_damage__icontains='Minor'))
        elif 'Water/Flood' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Water/Flood') or Q(info__lot_2nd_damage__icontains='Water/Flood'))
        else:
            lots = lots.all()

    ##########################
    filter_source = ''
    filter_featured = []
    filter_makes = []
    filter_models = []
    filter_years = []
    filter_odometers = []
    filter_locations = []
    filter_sale_dates = []
    filter_engine_types = []
    filter_transmissions = []
    filter_drive_trains = []
    filter_cylinderss = []
    filter_fuels = []
    filter_body_styles = []
    filter_vehicle_types = []
    filter_damages = []
    filter_doctypes = []
    ############################

    if vehicle_type:
        lots = lots.filter(info__type=vehicle_type)
        lots_sold = lots_sold.filter(info__type=vehicle_type)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        lots = lots.filter(info__year__range=(from_year, to_year))
        lots_sold = lots_sold.filter(info__year__range=(from_year, to_year))
        filter_word.append('[' + str(from_year) + ' TO ' + str(to_year) + ']')
    if make:
        lots = lots.filter(info__make__icontains=make)
        lots_sold = lots_sold.filter(info__make__icontains=make)
        filter_word.append(make)
        initial_status.append('make=' + make)
        filter_makes.append(make.upper())
    if model:
        lots = lots.filter(info__model=model)
        lots_sold = lots_sold.filter(info__model=model)
        filter_word.append(model)
        initial_status.append('model=' + model)
        filter_models.append(model)
    if location:
        lots = lots.filter(info__location=location)
        lots_sold = lots_sold.filter(info__location=location)
        filter_word.append(location)
        initial_status.append('location=' + location)
        filter_locations.append(location)

    # if sort:
    #     lots = lots.order_by(sort_direction + sort['sort_by'])
        # initial_status.append('sort=' + sort_)

    ##########################
    for key, value in params.items():
        # AND condition filters
        if 'source' == key:
            filter_source = value
        elif 'featured' == key:
            filter_featured = value
        # OR condition filters
        elif 'makes' == key:
            filter_makes += value
        elif 'models' == key:
            filter_models += value
        elif 'years' == key:
            filter_years = value
        elif 'odometers' == key:
            filter_odometers = value
        elif 'locations' == key:
            filter_locations += value
        elif 'sale_dates' == key:
            filter_sale_dates += value
        elif 'engine_types' == key:
            filter_engine_types += value
        elif 'transmissions' == key:
            filter_transmissions += value
        elif 'drive_trains' == key:
            filter_drive_trains += value
        elif 'cylinderss' == key:
            filter_cylinderss += value
        elif 'fuels' == key:
            filter_fuels += value
        elif 'body_styles' == key:
            filter_body_styles += value
        elif 'vehicle_types' == key:
            filter_vehicle_types += value
        elif 'damages' == key:
            filter_damages += value
        elif 'doctypes' == key:
            filter_doctypes += value

    ##########################

    ##########################
    def filter_by_filters(lots_, ignore=''):
        for param_key, param_value in params.items():
            # AND condition filters
            if 'source' == param_key and 'source' != ignore:
                if 'copart' == param_value:
                    lots_ = lots_.filter(info__source=True)
                elif 'iaai' == param_value:
                    lots_ = lots_.filter(info__source=False)
            elif 'featured' == param_key and 'featured' != ignore:
                for feature_ in param_value:
                    if 'Buy It Now' == feature_:
                        lots_ = lots_.filter(~Q(buy_today_bid=0))
                    elif 'Run and Drive' == feature_:
                        lots_ = lots_.filter(info__lot_highlights__contains='R')
                    elif 'Pure Sale Items' == feature_:
                        lots_ = lots_.filter(~Q(bid_status='PURE SALE'))
                    elif 'New Items' == feature_:
                        c_date = datetime.datetime.now().date()
                        f_date = c_date - datetime.timedelta(days=c_date.weekday() + 7)
                        t_date = f_date + datetime.timedelta(days=6)
                        lots_ = lots_.filter(created_at__range=(f_date, t_date))
            # OR condition filters
            elif 'makes' == param_key and 'makes' != ignore:
                query = Q(info__make__icontains=param_value[0])
                for make_ in param_value[1:]:
                    query |= Q(info__make__icontains=make_)
                lots_ = lots_.filter(query)
            elif 'models' == param_key and 'models' != ignore:
                query = Q(info__model=param_value[0])
                for model_ in param_value[1:]:
                    query |= Q(info__model=model_)
                lots_ = lots_.filter(query)
            elif 'years' == param_key and 'years' != ignore:
                query = Q(info__year=param_value[0])
                for year_ in param_value[1:]:
                    query |= Q(info__year=year_)
                lots_ = lots_.filter(query)
            elif 'odometers' == param_key and 'odometers' != ignore:
                pass
            elif 'locations' == param_key and 'locations' != ignore:
                query = Q(info__location=param_value[0])
                for location_ in param_value[1:]:
                    query |= Q(info__location=location_)
                lots_ = lots_.filter(query)
            elif 'sale_dates' == param_key and 'sale_dates' != ignore:
                query = Q(sale_date__year=str(param_value[0]).split('/')[2],
                          sale_date__month=str(param_value[0]).split('/')[0],
                          sale_date__day=str(param_value[0]).split('/')[1])
                for sale_date_ in param_value[1:]:
                    query |= Q(sale_date__year=str(sale_date_).split('/')[2],
                               sale_date__month=str(sale_date_).split('/')[0],
                               sale_date__day=str(sale_date_).split('/')[1])
                lots_ = lots_.filter(query)
            elif 'engine_types' == param_key and 'engine_types' != ignore:
                query = Q(info__engine_type=param_value[0])
                for engine_type_ in param_value[1:]:
                    query |= Q(info__engine_type=engine_type_)
                lots_ = lots_.filter(query)
            elif 'transmissions' == param_key and 'transmissions' != ignore:
                query = Q(info__transmission=param_value[0])
                for transmission_ in param_value[1:]:
                    query |= Q(info__transmission=transmission_)
                lots_ = lots_.filter(query)
            elif 'drive_trains' == param_key and 'drive_trains' != ignore:
                query = Q(info__drive=param_value[0])
                for drive_trains_ in param_value[1:]:
                    query |= Q(info__drive=drive_trains_)
                lots_ = lots_.filter(query)
            elif 'cylinderss' == param_key and 'cylinderss' != ignore:
                query = Q(info__cylinders=param_value[0])
                for cylinderss_ in param_value[1:]:
                    query |= Q(info__cylinders=cylinderss_)
                lots_ = lots_.filter(query)
            elif 'fuels' == param_key and 'fuels' != ignore:
                query = Q(info__fuel=param_value[0])
                for fuels_ in param_value[1:]:
                    query |= Q(info__fuel=fuels_)
                lots_ = lots_.filter(query)
            elif 'body_styles' == param_key and 'body_styles' != ignore:
                query = Q(info__body_style=param_value[0])
                for body_styles_ in param_value[1:]:
                    query |= Q(info__body_style=body_styles_)
                lots_ = lots_.filter(query)
            elif 'vehicle_types' == param_key and 'vehicle_types' != ignore:
                query = Q(info__type=param_value[0])
                for vehicle_types_ in param_value[1:]:
                    query |= Q(info__type=vehicle_types_)
                lots_ = lots_.filter(query)
            elif 'damages' == param_key and 'damages' != ignore:
                query = Q(info__lot_1st_damage=param_value[0])
                for damages_ in param_value[1:]:
                    query |= Q(info__lot_1st_damage=damages_)
                lots_ = lots_.filter(query)
            elif 'doctypes' == param_key and 'doctypes' != ignore:
                query = Q(info__doc_type_td__contains=str(param_value[0]).upper())
                for doctypes_ in param_value[1:]:
                    query |= Q(info__doc_type_td__contains=str(doctypes_).upper())
                lots_ = lots_.filter(query)

        return lots_

    ##########################

    # get filters count
    copart_count = lots.filter(info__source=True).count()
    iaai_count = lots.filter(info__source=False).count()
    # sold_count = VehicleSold.objects.count()
    sold_count = lots_sold.count()

    featured_lots = filter_by_filters(lots).order_by(sort_direction + sort['sort_by'])
    if len(featured_lots) == 0:
        return redirect('/')

    flfc21_count = featured_lots.filter(~Q(buy_today_bid=0)).count()
    flfc22_count = featured_lots.filter(info__lot_highlights__contains='R').count()
    flfc23_count = featured_lots.filter(~Q(bid_status='PURE SALE')).count()
    cur_date = datetime.datetime.now().date()
    from_date = cur_date - datetime.timedelta(days=cur_date.weekday() + 7)
    to_date = from_date + datetime.timedelta(days=6)
    flfc24_count = featured_lots.filter(created_at__range=(from_date, to_date)).count()
    # flfc25_count = 0  # No License Required
    # flfc26_count = 0  # Hot Items
    # flfc27_count = 0  # Engine Start Program
    # flfc28_count = 0  # Enhanced Vehicles
    # flfc29_count = 0  # Classics
    # flfc30_count = 0  # Exotics

    ###################################
    make_lots = filter_by_filters(lots, 'makes')
    count_makes = list(make_lots.values('info__make').annotate(make=F('info__make'), count=Count('info__make')))

    model_lots = filter_by_filters(lots, 'models')
    count_models = list(model_lots.values('info__model').annotate(model=F('info__model'), count=Count('info__model')))

    year_lots = filter_by_filters(lots, 'years')
    count_years = list(year_lots.values('info__year').annotate(year=F('info__year'), count=Count('info__year'))[::-1])

    location_lots = filter_by_filters(lots, 'locations')
    count_locations = list(location_lots.values('info__location').annotate(location=F('info__location'), count=Count('info__location')))

    sale_date_lots = filter_by_filters(lots, 'sale_dates').order_by('-sale_date')

    test = sale_date_lots.annotate(
            month=Cast(ExtractMonth('sale_date'), CharField()),
            day=Cast(ExtractDay('sale_date'), CharField()),
            year_test=Cast(ExtractYear('sale_date'), CharField()),
            sale_day=Concat('month', Value('/'), 'day', Value('/'), 'year_test')
        ).values('sale_day')

    res = test.values('sale_day').annotate(count=Count('sale_day'))

    temp_day = []
    temp_count = []
    for dat in res:
        if dat['sale_day'] not in temp_day:
            temp_day.append(dat['sale_day'])
            temp_count.append(dat['count'])
        else:
            temp_count[temp_day.index(dat['sale_day'])] = temp_count[temp_day.index(dat['sale_day'])] + dat['count']
    count_sale_dates = []
    for i, day in enumerate(temp_day):
        count_sale_dates.append({'sale_day': day, 'count': temp_count[i]})

    count_sale_dates_for_tag = count_sale_dates.copy()

    for sid, s in enumerate(count_sale_dates):
        if s['sale_day'] is None or s['sale_day'] == "" or s['sale_day'] == "//":
            del count_sale_dates[sid]
        else:
            if len(s['sale_day'].split('/')[0]) == 1:
                count_sale_dates[sid]['sale_day'] = "0" + count_sale_dates[sid]['sale_day']
            if len(s['sale_day'].split('/')[1]) == 1:
                count_sale_dates[sid]['sale_day'] = count_sale_dates[sid]['sale_day'][:3]\
                                                    + "0" + count_sale_dates[sid]['sale_day'][3:]

    engine_type_lots = filter_by_filters(lots, 'engine_types')
    count_engine_types = list(engine_type_lots.values('info__engine_type').annotate(engine_type=F('info__engine_type'), count=Count('info__engine_type')))
    for sid, count_engine_type_ in enumerate(count_engine_types):
        if count_engine_type_['info__engine_type'] is None or count_engine_type_['info__engine_type'] == "":
            del count_engine_types[sid]

    transmission_lots = filter_by_filters(lots, 'transmissions')
    count_transmissions = list(transmission_lots.values('info__transmission').annotate(transmission=F('info__transmission'), count=Count('info__transmission')))
    for sid, count_transmission_ in enumerate(count_transmissions):
        if count_transmission_['info__transmission'] is None or count_transmission_['info__transmission'] == "":
            del count_transmissions[sid]

    drive_train_lots = filter_by_filters(lots, 'drive_trains')
    count_drive_trains = list(drive_train_lots.values('info__drive').annotate(drive=F('info__drive'), count=Count('info__drive')))
    for sid, count_drive_train_ in enumerate(count_drive_trains):
        if count_drive_train_['info__drive'] is None or count_drive_train_['info__drive'] == "":
            del count_drive_trains[sid]

    cylinders_lots = filter_by_filters(lots, 'cylinderss')
    count_cylinderss = list(cylinders_lots.values('info__cylinders').annotate(cylinders=F('info__cylinders'), count=Count('info__cylinders')))
    for sid, count_cylinders_ in enumerate(count_cylinderss):
        if count_cylinders_['info__cylinders'] is None or count_cylinders_['info__cylinders'] == "":
            del count_cylinderss[sid]

    fuel_lots = filter_by_filters(lots, 'fuels')
    count_fuels = list(fuel_lots.values('info__fuel').annotate(fuel=F('info__fuel'), count=Count('info__fuel')))
    for sid, count_fuel_ in enumerate(count_fuels):
        if count_fuel_['info__fuel'] is None or count_fuel_['info__fuel'] == "":
            del count_fuels[sid]

    body_style_lots = filter_by_filters(lots, 'body_styles')
    count_body_styles = list(body_style_lots.values('info__body_style').annotate(body_style=F('info__body_style'), count=Count('info__body_style')))
    for sid, count_body_style_ in enumerate(count_body_styles):
        if count_body_style_['info__body_style'] is None or count_body_style_['info__body_style'] == "":
            del count_body_styles[sid]

    vehicle_type_lots = filter_by_filters(lots, 'vehicle_types')
    count_vehicle_types = list(vehicle_type_lots.values('info__type').annotate(type=F('info__type'), count=Count('info__type')))
    for sid, count_vehicle_type_ in enumerate(count_vehicle_types):
        if count_vehicle_type_['info__type'] is None or count_vehicle_type_['info__type'] == "":
            del count_vehicle_types[sid]
        else:
            count_vehicle_types[sid]['info__type'] = dict(TYPES)[count_vehicle_type_['info__type']]

    damage_lots = filter_by_filters(lots, 'damages')
    count_damages = list(damage_lots.values('info__lot_1st_damage').annotate(lot_1st_damage=F('info__lot_1st_damage'), count=Count('info__lot_1st_damage')))
    for sid, count_damage_ in enumerate(count_damages):
        if count_damage_['info__lot_1st_damage'] is None or count_damage_['info__lot_1st_damage'] == "":
            del count_damages[sid]

    doctype_lots = filter_by_filters(lots, 'doctypes')

    count_doctypes = []
    doctype_fields = ['Clean Title', 'Non-Repairable', 'Salvage Title']
    for doctype_field in doctype_fields:
        count_doctypes.append(
            {'doc_type_td': doctype_field,
             'count': doctype_lots.filter(info__doc_type_td__contains=str(doctype_field).upper()).count()})

    '''odometer_lots = filter_by_filters(lots, 'odometers')
    odometers = odometer_lots.raw(
        'SELECT ROW_NUMBER() OVER (ORDER BY 1) AS id,'
        'SUM(CASE WHEN odometer_orr < 25000 THEN 1 ELSE 0 END) AS count_0,'
        'SUM(CASE WHEN odometer_orr >= 25000 AND odometer_orr <= 50000 THEN 1 ELSE 0 END) AS count_1,'
        'SUM(CASE WHEN odometer_orr > 50000 AND odometer_orr <= 75000 THEN 1 ELSE 0 END) AS count_2,'
        'SUM(CASE WHEN odometer_orr > 75000 AND odometer_orr <= 100000 THEN 1 ELSE 0 END) AS count_3,'
        'SUM(CASE WHEN odometer_orr > 100000 AND odometer_orr <= 150000 THEN 1 ELSE 0 END) AS count_4,'
        'SUM(CASE WHEN odometer_orr > 150000 AND odometer_orr <= 200000 THEN 1 ELSE 0 END) AS count_5,'
        'SUM(CASE WHEN odometer_orr > 200000 THEN 1 ELSE 0 END) AS count_6 '
        'FROM product_vehicle')
    count_odometers = [
        {'odometer': '< 25,000', 'count': odometers[0].count_0},
        {'odometer': '25,000 to 50,000', 'count': odometers[0].count_1},
        {'odometer': '50,001 to 75,000', 'count': odometers[0].count_2},
        {'odometer': '75,001 to 100,000', 'count': odometers[0].count_3},
        {'odometer': '100,001 to 150,000', 'count': odometers[0].count_4},
        {'odometer': '150,001 to 200,000', 'count': odometers[0].count_5},
        {'odometer': '> 200,000', 'count': odometers[0].count_6},
    ]'''
    count_odometers = [
        {'odometer': '< 25,000', 'count': 0},
        {'odometer': '25,000 to 50,000', 'count': 0},
        {'odometer': '50,001 to 75,000', 'count': 0},
        {'odometer': '75,001 to 100,000', 'count': 0},
        {'odometer': '100,001 to 150,000', 'count': 0},
        {'odometer': '150,001 to 200,000', 'count': 0},
        {'odometer': '> 200,000', 'count': 0},
    ]

    page = int(request.GET.get('page', 1))
    entry = int(request.GET.get('entry', 20))

    paginator = Paginator(featured_lots, entry)
    if page > paginator.num_pages:
        print(request.get_full_path())
        redirect_url = request.get_full_path().split('&')
        for idx, param in enumerate(redirect_url):
            if param.startswith('page='):
                redirect_url[idx] = 'page=' + str(paginator.num_pages)
        return redirect('&'.join(redirect_url))
    paged_lots = paginator.get_page(page)

    pages = ['First', 'Previous']
    if paginator.num_pages <= 7:
        pages += [str(a + 1) for a in range(paginator.num_pages)]
    else:
        if page < 5:
            pages += [str(a + 1) for a in range(5)]
            pages.append('...')
            pages.append(str(paginator.num_pages))
        elif page > paginator.num_pages - 4:
            pages.append('1')
            pages.append('...')
            pages += [str(a + 1) for a in range(paginator.num_pages - 5, paginator.num_pages)]
        else:
            pages.append('1')
            pages.append('...')
            pages.append(str(page - 1))
            pages.append(str(page))
            pages.append(str(page + 1))
            pages.append('...')
            pages.append(str(paginator.num_pages))
    pages += ['Next', 'Last']

    context = {
        'lots': paged_lots,
        'total_lots': paginator.count,
        'pages': pages[::-1],
        'current_page': str(page),
        'current_entry': entry,
        'page_start_index': (page - 1) * entry + 1,
        'page_end_index': page * entry if page != paginator.num_pages else paginator.count,
        'filter_word': ', '.join(filter_word),

        'copart_count': copart_count,
        'iaai_count': iaai_count,
        'sold_count': sold_count,

        'features': [
            {'feature': 'Buy It Now', 'count': flfc21_count},
            {'feature': 'Run and Drive', 'count': flfc22_count},
            {'feature': 'Pure Sale Items', 'count': flfc23_count},
            {'feature': 'New Items', 'count': flfc24_count}
        ],

        ###########################
        'makes': count_makes,
        'models': count_models,
        'years': count_years,
        'odometers': count_odometers,
        'locations': count_locations,
        'sale_dates': count_sale_dates,
        'sale_dates_for_tag': count_sale_dates_for_tag,
        'engine_types': count_engine_types,
        'transmissions': count_transmissions,
        'drive_trains': count_drive_trains,
        'cylinders': count_cylinderss,
        'fuels': count_fuels,
        'body_styles': count_body_styles,
        'vehicle_types': count_vehicle_types,
        'damages': count_damages,
        'doctypes': count_doctypes,

        'applied_filter_source': filter_source,
        'applied_sold': '',
        'applied_filter_features': filter_featured,
        'applied_filter_makes': filter_makes,
        'applied_filter_models': filter_models,
        'applied_filter_years': filter_years,
        'applied_filter_odometers': filter_odometers,
        'applied_filter_locations': filter_locations,
        'applied_filter_sale_dates': filter_sale_dates,
        'applied_filter_engine_types': filter_engine_types,
        'applied_filter_transmissions': filter_transmissions,
        'applied_filter_drive_trains': filter_drive_trains,
        'applied_filter_cylinders': filter_cylinderss,
        'applied_filter_fuels': filter_fuels,
        'applied_filter_body_styles': filter_body_styles,
        'applied_filter_vehicle_types': filter_vehicle_types,
        'applied_filter_damages': filter_damages,
        'applied_filter_doctypes': filter_doctypes,
        ###########################

        'initial': '&'.join(initial_status),
        'url': 'params=' + params_ + '&sort=' + sort_ if params_ else '',
        'status': status,

        'config': config,
    }

    return render(request, 'product/list.html', context=context)


def ajax_lots_by_search(request):
    # get params from url
    vehicle_type = request.GET.get('type', '')
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')
    location = request.GET.get('location', '')
    params = request.GET.get('params', {})
    status = request.GET.get('status', [])
    feature = request.GET.get('feature', '')
    sort_ = request.GET.get('sort', '')

    if sort_:
        sort = eval(sort_)
        sort['sort_by'] = 'info__' + sort['sort_by']
    else:
        sort = dict(sort_by='info__year', sort_type='desc')

    sort_direction = ''
    if 'desc' == sort['sort_type']:
        sort_direction = '-'

    filter_word = []
    if vehicle_type:
        filter_word.append(dict(TYPES)[vehicle_type])

    # check if 'Show Real Price' checked
    sold = False
    if params:
        params = eval(params)
        if 'sold' in params and 'yes' == params['sold']:
            sold = True

    lots = VehicleSold.objects if sold else Vehicle.objects
    lots_sold = VehicleSold.objects
    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filter_word.append(featured_filter.name)
        if 'Buy It Now' == featured_filter.name:
            lots = lots.filter(~Q(buy_today_bid=0))
        elif 'Pure Sale Items' == featured_filter.name:
            lots = lots.filter(~Q(bid_status='PURE SALE'))
        elif 'New Items' == featured_filter.name:
            cur_date = datetime.datetime.now().date()
            from_date = cur_date - datetime.timedelta(days=cur_date.weekday() + 7)
            to_date = from_date + datetime.timedelta(days=6)
            lots = lots.filter(created_at__range=(from_date, to_date))
        elif 'Lots with Bids' == featured_filter.name:
            lots = lots.filter(~Q(current_bid=0))
        elif 'No Bids Yet' == featured_filter.name:
            lots = lots.filter(current_bid=0)
        elif 'Hybrid Vehicles' == featured_filter.name:
            lots = lots.filter(info__fuel="HYBRID ENGINE")
        elif 'Repossessions' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='B')
        elif 'Donations' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='D').filter(~Q(lot_highlights="Did Not Test Start"))
        elif 'Featured Vehicles' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='F')
        elif 'Offsite Sales' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='O')
        elif 'Run and Drive' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='R')
        elif 'Clean Title' == featured_filter.name:
            lots = lots.filter(~Q(info__doc_type_td__icontains='salvage'))
        elif 'Salvage Title' == featured_filter.name:
            lots = lots.filter(info__doc_type_td__icontains='salvage')
        elif 'Front End' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Front End') or Q(info__2nd_damage__icontains='Front End'))
        elif 'Hail Damage' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Hail') or Q(info__lot_2nd_damage__icontains='Hail'))
        elif 'Normal Wear' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Normal Wear') or Q(info__lot_2nd_damage__icontains='Normal Wear'))
        elif 'Minor Dents/Scratch' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Minor') or Q(info__lot_2nd_damage__icontains='Minor'))
        elif 'Water/Flood' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Water/Flood') or Q(info__lot_2nd_damage__icontains='Water/Flood'))
        else:
            lots = lots.all()

    #################################
    filter_source = ''
    filter_featured = []
    filter_makes = []
    filter_models = []
    filter_years = []
    filter_odometers = []
    filter_locations = []
    filter_sale_dates = []
    filter_engine_types = []
    filter_transmissions = []
    filter_drive_trains = []
    filter_cylinderss = []
    filter_fuels = []
    filter_body_styles = []
    filter_vehicle_types = []
    filter_damages = []
    filter_doctypes = []
    ##############################

    if vehicle_type:
        lots = lots.filter(info__type=vehicle_type)
        lots_sold = lots_sold.filter(info__type=vehicle_type)
    if year:
        # extract from_year and to_year from year_range
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        lots = lots.filter(info__year__range=(from_year, to_year))
        lots_sold = lots_sold.filter(info__year__range=(from_year, to_year))
        filter_word.append('[' + str(from_year) + ' TO ' + str(to_year) + ']')
    if make:
        lots = lots.filter(info__make__icontains=make)
        lots_sold = lots_sold.filter(info__make__icontains=make)
        filter_word.append(make)
        filter_makes.append(make.upper())
    if model:
        lots = lots.filter(info__model=model)
        lots_sold = lots_sold.filter(info__model=model)
        filter_word.append(model)
        filter_models.append(model)
    if location:
        lots = lots.filter(info__location=location)
        lots_sold = lots_sold.filter(info__location=location)
        filter_word.append(location)
        filter_locations.append(location)
    # if sort:
    #     lots = lots.order_by(sort_direction + sort['sort_by'])
        # initial_status.append('sort=' + sort_)

    ################################
    for key, value in params.items():
        # AND condition filters
        if 'source' == key:
            filter_source = value
        elif 'featured' == key:
            filter_featured = value
        # OR condition filters
        elif 'makes' == key:
            filter_makes += value
        elif 'models' == key:
            filter_models += value
        elif 'years' == key:
            filter_years = value
        elif 'odometers' == key:
            filter_odometers = value
        elif 'locations' == key:
            filter_locations += value
        elif 'sale_dates' == key:
            filter_sale_dates += value
        elif 'engine_types' == key:
            filter_engine_types += value
        elif 'transmissions' == key:
            filter_transmissions += value
        elif 'drive_trains' == key:
            filter_drive_trains += value
        elif 'cylinderss' == key:
            filter_cylinderss += value
        elif 'fuels' == key:
            filter_fuels += value
        elif 'body_styles' == key:
            filter_body_styles += value
        elif 'vehicle_types' == key:
            filter_vehicle_types += value
        elif 'damages' == key:
            filter_damages += value
        elif 'doctypes' == key:
            filter_doctypes += value

    #########################################

    #########################################
    def filter_by_filters(lots_, ignore=''):
        for param_key, param_value in params.items():
            # AND condition filters
            if 'source' == param_key and 'source' != ignore:
                if 'copart' == param_value:
                    lots_ = lots_.filter(info__source=True)
                elif 'iaai' == param_value:
                    lots_ = lots_.filter(info__source=False)
            elif 'featured' == param_key and 'featured' != ignore:
                for feature in param_value:
                    if 'Buy It Now' == feature:
                        lots_ = lots_.filter(~Q(buy_today_bid=0))
                    elif 'Run and Drive' == feature:
                        lots_ = lots_.filter(info__lot_highlights__contains='R')
                    elif 'Pure Sale Items' == feature:
                        lots_ = lots_.filter(~Q(bid_status='PURE SALE'))
                    elif 'New Items' == feature:
                        c_date = datetime.datetime.now().date()
                        f_date = c_date - datetime.timedelta(days=c_date.weekday() + 7)
                        t_date = f_date + datetime.timedelta(days=6)
                        lots_ = lots_.filter(created_at__range=(f_date, t_date))
            # OR condition filters
            elif 'makes' == param_key and 'makes' != ignore:
                query = Q(info__make__icontains=param_value[0])
                for make_ in param_value[1:]:
                    query |= Q(info__make__icontains=make_)
                lots_ = lots_.filter(query)
            elif 'models' == param_key and 'models' != ignore:
                query = Q(info__model=param_value[0])
                for model_ in param_value[1:]:
                    query |= Q(info__model=model_)
                lots_ = lots_.filter(query)
            elif 'years' == param_key and 'years' != ignore:
                query = Q(info__year=param_value[0])
                for year in param_value[1:]:
                    query |= Q(info__year=year)
                lots_ = lots_.filter(query)
            elif 'odometers' == param_key and 'odometers' != ignore:
                pass
            elif 'locations' == param_key and 'locations' != ignore:
                query = Q(info__location=param_value[0])
                for location_ in param_value[1:]:
                    query |= Q(info__location=location_)
                lots_ = lots_.filter(query)
            elif 'sale_dates' == param_key and 'sale_dates' != ignore:
                query = Q(sale_date__year=str(param_value[0]).split('/')[2],
                          sale_date__month=str(param_value[0]).split('/')[0],
                          sale_date__day=str(param_value[0]).split('/')[1])
                for sale_date_ in param_value[1:]:
                    query |= Q(sale_date__year=str(sale_date_).split('/')[2],
                               sale_date__month=str(sale_date_).split('/')[0],
                               sale_date__day=str(sale_date_).split('/')[1])
                lots_ = lots_.filter(query)
            elif 'engine_types' == param_key and 'engine_types' != ignore:
                query = Q(info__engine_type=param_value[0])
                for engine_type_ in param_value[1:]:
                    query |= Q(info__engine_type=engine_type_)
                lots_ = lots_.filter(query)
            elif 'transmissions' == param_key and 'transmissions' != ignore:
                query = Q(info__transmission=param_value[0])
                for transmission_ in param_value[1:]:
                    query |= Q(info__transmission=transmission_)
                lots_ = lots_.filter(query)
            elif 'drive_trains' == param_key and 'drive_trains' != ignore:
                query = Q(info__drive=param_value[0])
                for drive_trains_ in param_value[1:]:
                    query |= Q(info__drive=drive_trains_)
                lots_ = lots_.filter(query)
            elif 'cylinderss' == param_key and 'cylinderss' != ignore:
                query = Q(info__cylinders=param_value[0])
                for cylinderss_ in param_value[1:]:
                    query |= Q(info__cylinders=cylinderss_)
                lots_ = lots_.filter(query)
            elif 'fuels' == param_key and 'fuels' != ignore:
                query = Q(info__fuel=param_value[0])
                for fuels_ in param_value[1:]:
                    query |= Q(info__fuel=fuels_)
                lots_ = lots_.filter(query)
            elif 'body_styles' == param_key and 'body_styles' != ignore:
                query = Q(info__body_style=param_value[0])
                for body_styles_ in param_value[1:]:
                    query |= Q(info__body_style=body_styles_)
                lots_ = lots_.filter(query)
            elif 'vehicle_types' == param_key and 'vehicle_types' != ignore:
                query = Q(info__type=param_value[0])
                for vehicle_types_ in param_value[1:]:
                    query |= Q(info__type=vehicle_types_)
                lots_ = lots_.filter(query)
            elif 'damages' == param_key and 'damages' != ignore:
                query = Q(info__lot_1st_damage=param_value[0])
                for damages_ in param_value[1:]:
                    query |= Q(info__lot_1st_damage=damages_)
                lots_ = lots_.filter(query)
            elif 'doctypes' == param_key and 'doctypes' != ignore:
                query = Q(info__doc_type_td__contains=str(param_value[0]).upper())
                for doctypes_ in param_value[1:]:
                    query |= Q(info__doc_type_td__contains=str(doctypes_).upper())
                lots_ = lots_.filter(query)
        return lots_
        #########################################

    # get filters count
    copart_count = lots.filter(info__source=True).count()
    iaai_count = lots.filter(info__source=False).count()
    # sold_count = VehicleSold.objects.count()
    sold_count = lots_sold.count()

    # featured_lots = filter_by_filters(lots).order_by(sort_direction + sort['sort_by'])
    featured_lots = filter_by_filters(lots)
    flfc21_count = featured_lots.filter(~Q(buy_today_bid=0)).count()
    flfc22_count = featured_lots.filter(info__lot_highlights__contains='R').count()
    flfc23_count = featured_lots.filter(~Q(bid_status='PURE SALE')).count()
    cur_date = datetime.datetime.now().date()
    from_date = cur_date - datetime.timedelta(days=cur_date.weekday() + 7)
    to_date = from_date + datetime.timedelta(days=6)
    flfc24_count = featured_lots.filter(created_at__range=(from_date, to_date)).count()
    # flfc25_count = 0  # No License Required
    # flfc26_count = 0  # Hot Items
    # flfc27_count = 0  # Engine Start Program
    # flfc28_count = 0  # Enhanced Vehicles
    # flfc29_count = 0  # Classics
    # flfc30_count = 0  # Exotics

    make_lots = filter_by_filters(lots, 'makes')
    count_makes = list(make_lots.values('info__make').annotate(make=F('info__make'), count=Count('info__make')))

    model_lots = filter_by_filters(lots, 'models')
    count_models = list(model_lots.values('info__model').annotate(model=F('info__model'), count=Count('info__model')))

    year_lots = filter_by_filters(lots, 'years')
    count_years = list(year_lots.values('info__year').annotate(year=F('info__year'), count=Count('info__year'))[::-1])

    '''odometer_lots = filter_by_filters(lots, 'odometers')
    odometers = odometer_lots.raw(
        'SELECT ROW_NUMBER() OVER (ORDER BY 1) AS id,'
        'SUM(CASE WHEN odometer_orr < 25000 THEN 1 ELSE 0 END) AS count_0,'
        'SUM(CASE WHEN odometer_orr >= 25000 AND odometer_orr <= 50000 THEN 1 ELSE 0 END) AS count_1,'
        'SUM(CASE WHEN odometer_orr > 50000 AND odometer_orr <= 75000 THEN 1 ELSE 0 END) AS count_2,'
        'SUM(CASE WHEN odometer_orr > 75000 AND odometer_orr <= 100000 THEN 1 ELSE 0 END) AS count_3,'
        'SUM(CASE WHEN odometer_orr > 100000 AND odometer_orr <= 150000 THEN 1 ELSE 0 END) AS count_4,'
        'SUM(CASE WHEN odometer_orr > 150000 AND odometer_orr <= 200000 THEN 1 ELSE 0 END) AS count_5,'
        'SUM(CASE WHEN odometer_orr > 200000 THEN 1 ELSE 0 END) AS count_6 '
        'FROM product_vehicle')
    count_odometers = [
        {'odometer': '< 25,000', 'count': odometers[0].count_0},
        {'odometer': '25,000 to 50,000', 'count': odometers[0].count_1},
        {'odometer': '50,001 to 75,000', 'count': odometers[0].count_2},
        {'odometer': '75,001 to 100,000', 'count': odometers[0].count_3},
        {'odometer': '100,001 to 150,000', 'count': odometers[0].count_4},
        {'odometer': '150,001 to 200,000', 'count': odometers[0].count_5},
        {'odometer': '> 200,000', 'count': odometers[0].count_6},
    ]'''
    count_odometers = [
        {'odometer': '< 25,000', 'count': 0},
        {'odometer': '25,000 to 50,000', 'count': 0},
        {'odometer': '50,001 to 75,000', 'count': 0},
        {'odometer': '75,001 to 100,000', 'count': 0},
        {'odometer': '100,001 to 150,000', 'count': 0},
        {'odometer': '150,001 to 200,000', 'count': 0},
        {'odometer': '> 200,000', 'count': 0},
    ]

    ############################
    location_lots = filter_by_filters(lots, 'locations')
    count_locations = list(location_lots.values('info__location').annotate(location=F('info__location'), count=Count('info__location')))

    sale_date_lots = filter_by_filters(lots, 'sale_dates').order_by('-sale_date')
    test = sale_date_lots.annotate(
        month=Cast(ExtractMonth('sale_date'), CharField()),
        day=Cast(ExtractDay('sale_date'), CharField()),
        year_test=Cast(ExtractYear('sale_date'), CharField()),
        sale_day=Concat('month', Value('/'), 'day', Value('/'), 'year_test')
    ).values('sale_day')

    res = test.values('sale_day').annotate(count=Count('sale_day'))
    # count_sale_dates = list(test.values('sale_day').annotate(count=Count('sale_day')))

    temp_day = []
    temp_count = []
    for dat in res:
        if dat['sale_day'] not in temp_day:
            temp_day.append(dat['sale_day'])
            temp_count.append(dat['count'])
        else:
            temp_count[temp_day.index(dat['sale_day'])] = temp_count[temp_day.index(dat['sale_day'])] + dat['count']
    count_sale_dates = []
    for i, day in enumerate(temp_day):
        count_sale_dates.append({'sale_day': day, 'count': temp_count[i]})

    count_sale_dates_for_tag = count_sale_dates.copy()

    for sid, s in enumerate(count_sale_dates):
        if s['sale_day'] is None or s['sale_day'] == "" or s['sale_day'] == "//":
            del count_sale_dates[sid]
        else:
            if len(s['sale_day'].split('/')[0]) == 1:
                count_sale_dates[sid]['sale_day'] = "0" + count_sale_dates[sid]['sale_day']
            if len(s['sale_day'].split('/')[1]) == 1:
                count_sale_dates[sid]['sale_day'] = count_sale_dates[sid]['sale_day'][:3] \
                                                    + "0" + count_sale_dates[sid]['sale_day'][3:]

    engine_type_lots = filter_by_filters(lots, 'engine_types')
    count_engine_types = list(engine_type_lots.values('info__engine_type').annotate(engine_type=F('info__engine_type'), count=Count('info__engine_type')))
    for sid, count_engine_type_ in enumerate(count_engine_types):
        if count_engine_type_['info__engine_type'] is None or count_engine_type_['info__engine_type'] == "":
            del count_engine_types[sid]

    transmission_lots = filter_by_filters(lots, 'transmissions')
    count_transmissions = list(transmission_lots.values('info__transmission').annotate(transmission=F('info__transmission'), count=Count('info__transmission')))
    for sid, count_transmission_ in enumerate(count_transmissions):
        if count_transmission_['info__transmission'] is None or count_transmission_['info__transmission'] == "":
            del count_transmissions[sid]

    drive_train_lots = filter_by_filters(lots, 'drive_trains')
    count_drive_trains = list(drive_train_lots.values('info__drive').annotate(drive=F('info__drive'), count=Count('info__drive')))
    for sid, count_drive_train_ in enumerate(count_drive_trains):
        if count_drive_train_['info__drive'] is None or count_drive_train_['info__drive'] == "":
            del count_drive_trains[sid]

    cylinders_lots = filter_by_filters(lots, 'cylinderss')
    count_cylinderss = list(cylinders_lots.values('info__cylinders').annotate(cylinders=F('info__cylinders'), count=Count('info__cylinders')))
    for sid, count_cylinders_ in enumerate(count_cylinderss):
        if count_cylinders_['info__cylinders'] is None or count_cylinders_['info__cylinders'] == "":
            del count_cylinderss[sid]

    fuel_lots = filter_by_filters(lots, 'fuels')
    count_fuels = list(fuel_lots.values('info__fuel').annotate(fuel=F('info__fuel'), count=Count('info__fuel')))
    for sid, count_fuel_ in enumerate(count_fuels):
        if count_fuel_['info__fuel'] is None or count_fuel_['info__fuel'] == "":
            del count_fuels[sid]

    body_style_lots = filter_by_filters(lots, 'body_styles')
    count_body_styles = list(body_style_lots.values('info__body_style').annotate(body_style=F('info__body_style'), count=Count('info__body_style')))
    for sid, count_body_style_ in enumerate(count_body_styles):
        if count_body_style_['info__body_style'] is None or count_body_style_['info__body_style'] == "":
            del count_body_styles[sid]

    vehicle_type_lots = filter_by_filters(lots, 'vehicle_types')
    count_vehicle_types = list(vehicle_type_lots.values('info__type').annotate(type=F('info__type'), count=Count('info__type')))
    for sid, count_vehicle_type_ in enumerate(count_vehicle_types):
        if count_vehicle_type_['info__type'] is None or count_vehicle_type_['info__type'] == "":
            del count_vehicle_types[sid]
        else:
            count_vehicle_types[sid]['info__type'] = dict(TYPES)[count_vehicle_type_['info__type']]

    damage_lots = filter_by_filters(lots, 'damages')
    count_damages = list(damage_lots.values('info__lot_1st_damage').annotate(lot_1st_damage=F('info__lot_1st_damage'), count=Count('info__lot_1st_damage')))
    for sid, count_damage_ in enumerate(count_damages):
        if count_damage_['info__lot_1st_damage'] is None or count_damage_['info__lot_1st_damage'] == "":
            del count_damages[sid]

    doctype_lots = filter_by_filters(lots, 'doctypes')

    count_doctypes = []
    doctype_fields = ['Clean Title', 'Non-Repairable', 'Salvage Title']
    for doctype_field in doctype_fields:
        count_doctypes.append(
            {'doc_type_td': doctype_field,
             'count': doctype_lots.filter(info__doc_type_td__contains=str(doctype_field).upper()).count()})

    #################################

    # lots = filter_by_filters(lots).order_by('-year')
    lots = filter_by_filters(lots).order_by(sort_direction + sort['sort_by'])
    if len(lots) == 0:
        return redirect('/')

    page = int(request.GET.get('page', 1))
    entry = int(request.GET.get('entry', 20))

    paginator = Paginator(lots, entry)
    if page > paginator.num_pages:
        print(request.get_full_path())
        redirect_url = request.get_full_path().split('&')
        for idx, param in enumerate(redirect_url):
            if param.startswith('page='):
                redirect_url[idx] = 'page=' + str(paginator.num_pages)
        return redirect('&'.join(redirect_url))
    paged_lots = paginator.get_page(page)

    pages = ['First', 'Previous']
    if paginator.num_pages <= 7:
        pages += [str(a + 1) for a in range(paginator.num_pages)]
    else:
        if page < 5:
            pages += [str(a + 1) for a in range(5)]
            pages.append('...')
            pages.append(str(paginator.num_pages))
        elif page > paginator.num_pages - 4:
            pages.append('1')
            pages.append('...')
            pages += [str(a + 1) for a in range(paginator.num_pages - 5, paginator.num_pages)]
        else:
            pages.append('1')
            pages.append('...')
            pages.append(str(page - 1))
            pages.append(str(page))
            pages.append(str(page + 1))
            pages.append('...')
            pages.append(str(paginator.num_pages))
    pages += ['Next', 'Last']

    # result_lots = []
    # for a in paged_lots:
    #     a = a.__dict__
    #     del a['_state']
    #     result_lots.append(a)

    context = {
        'lots': paged_lots,
        'total_lots': paginator.count,
        'pages': pages[::-1],
        'current_page': str(page),
        'current_entry': entry,
        'page_start_index': (page - 1) * entry + 1,
        'page_end_index': page * entry if page != paginator.num_pages else paginator.count,
        'filter_word': ', '.join(filter_word),

        'copart_count': copart_count,
        'iaai_count': iaai_count,
        'sold_count': sold_count,

        'features': [
            {'feature': 'Buy It Now', 'count': flfc21_count},
            {'feature': 'Run and Drive', 'count': flfc22_count},
            {'feature': 'Pure Sale Items', 'count': flfc23_count},
            {'feature': 'New Items', 'count': flfc24_count}
        ],

        #################################
        'makes': count_makes,
        'models': count_models,
        'years': count_years,
        'odometers': count_odometers,
        'locations': count_locations,
        'sale_dates': count_sale_dates,
        'sale_dates_for_tag': count_sale_dates_for_tag,
        'engine_types': count_engine_types,
        'transmissions': count_transmissions,
        'drive_trains': count_drive_trains,
        'cylinders': count_cylinderss,
        'fuels': count_fuels,
        'body_styles': count_body_styles,
        'vehicle_types': count_vehicle_types,
        'damages': count_damages,
        'doctypes': count_doctypes,

        'applied_filter_source': filter_source,
        'applied_sold': 'yes' if sold else '',
        'applied_filter_features': filter_featured,
        'applied_filter_makes': filter_makes,
        'applied_filter_models': filter_models,
        'applied_filter_years': filter_years,
        'applied_filter_odometers': filter_odometers,
        'applied_filter_locations': filter_locations,
        'applied_filter_sale_dates': filter_sale_dates,
        'applied_filter_engine_types': filter_engine_types,
        'applied_filter_transmissions': filter_transmissions,
        'applied_filter_drive_trains': filter_drive_trains,
        'applied_filter_cylinders': filter_cylinderss,
        'applied_filter_fuels': filter_fuels,
        'applied_filter_body_styles': filter_body_styles,
        'applied_filter_vehicle_types': filter_vehicle_types,
        'applied_filter_damages': filter_damages,
        'applied_filter_doctypes': filter_doctypes,
        ###################################

        'status': status,

        'config': config,
    }
    return render(request, 'product/content.html', context=context)


def detail(request, lot):
    lot = Vehicle.objects.get(info__lot=int(lot))
    is_similar = True

    similar = Vehicle.objects.filter(info__make=lot.info.make).filter(info__model=lot.info.model).filter(info__year=lot.info.year).filter(~Q(info__lot=int(lot.info.lot))).order_by('-id')
    if len(similar) >= 12:
        similar = similar[:12]
    else:
        similar = Vehicle.objects.filter(info__make=lot.info.make).filter(info__model=lot.info.model).filter(~Q(info__lot=int(lot.info.lot))).order_by('-id')
        if len(similar) >= 12:
            similar = similar[:12]
        else:
            similar = Vehicle.objects.filter(info__make=lot.info.make).filter(~Q(info__lot=int(lot.info.lot))).order_by('-id')
            if len(similar) >= 12:
                similar = similar[:12]
            else:
                similar = Vehicle.objects.filter(~Q(info__retail_value=0)).filter(~Q(info__lot=int(lot.info.lot))).order_by('-id')[:12]
                is_similar = False

    context = {'lot': lot, 'similar': similar, 'is_similar': is_similar}
    return render(request, 'product/detail.html', context=context)


def lots_search(request):
    if not request.GET:
        return redirect('/')

    # get params from url
    vehicle_type = request.GET.get('type', '')
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')
    location = request.GET.get('location', '')
    params_ = request.GET.get('params', '')
    status = request.GET.get('status', '')
    feature = request.GET.get('feature', '')
    sort_ = request.GET.get('sort', '')

    if sort_:
        sort = eval(sort_)
        sort['sort_by'] = 'info__' + sort['sort_by']
    else:
        sort = dict(sort_by='info__year', sort_type='desc')

    sort_direction = ''
    if 'desc' == sort['sort_type']:
        sort_direction = '-'

    initial_status = []
    filter_word = []
    if vehicle_type:
        initial_status.append('type=' + vehicle_type)
        filter_word.append(dict(TYPES)[vehicle_type])
    if year:
        initial_status.append('year=' + year)
    if feature:
        initial_status.append('feature=' + feature)

    params = {}
    # check if 'Show Real Price' checked
    sold = False
    if params_:
        params = eval(params_)
        if 'sold' in params and 'yes' == params['sold']:
            sold = True

    lots = VehicleSold.objects if sold else Vehicle.objects
    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filter_word.append(featured_filter.name)
        if 'Buy It Now' == featured_filter.name:
            lots = lots.filter(~Q(buy_today_bid=0))
        elif 'Pure Sale Items' == featured_filter.name:
            lots = lots.filter(~Q(bid_status='PURE SALE'))
        elif 'New Items' == featured_filter.name:
            cur_date = datetime.datetime.now().date()
            from_date = cur_date - datetime.timedelta(days=cur_date.weekday() + 7)
            to_date = from_date + datetime.timedelta(days=6)
            lots = lots.filter(created_at__range=(from_date, to_date))
        elif 'Lots with Bids' == featured_filter.name:
            lots = lots.filter(~Q(current_bid=0))
        elif 'No Bids Yet' == featured_filter.name:
            lots = lots.filter(current_bid=0)
        elif 'Hybrid Vehicles' == featured_filter.name:
            lots = lots.filter(info__fuel="HYBRID ENGINE")
        elif 'Repossessions' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='B')
        elif 'Donations' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='D').filter(~Q(lot_highlights="Did Not Test Start"))
        elif 'Featured Vehicles' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='F')
        elif 'Offsite Sales' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='O')
        elif 'Run and Drive' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='R')
        elif 'Clean Title' == featured_filter.name:
            lots = lots.filter(~Q(info__doc_type_td__icontains='salvage'))
        elif 'Salvage Title' == featured_filter.name:
            lots = lots.filter(info__doc_type_td__icontains='salvage')
        elif 'Front End' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Front End') or Q(info__2nd_damage__icontains='Front End'))
        elif 'Hail Damage' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Hail') or Q(info__lot_2nd_damage__icontains='Hail'))
        elif 'Normal Wear' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Normal Wear') or Q(info__lot_2nd_damage__icontains='Normal Wear'))
        elif 'Minor Dents/Scratch' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Minor') or Q(info__lot_2nd_damage__icontains='Minor'))
        elif 'Water/Flood' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Water/Flood') or Q(info__lot_2nd_damage__icontains='Water/Flood'))
        else:
            lots = lots.all()

    ##########################
    filter_source = ''
    filter_featured = []
    filter_makes = []
    filter_models = []
    filter_years = []
    filter_engine_types = []
    filter_transmissions = []
    filter_drive_trains = []
    filter_fuels = []
    filter_body_styles = []
    ############################

    if vehicle_type:
        lots = lots.filter(info__type=vehicle_type)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        lots = lots.filter(info__year__range=(from_year, to_year))
        filter_word.append('[' + str(from_year) + ' TO ' + str(to_year) + ']')
    if make:
        lots = lots.filter(info__make__icontains=make)
        filter_word.append(make)
        initial_status.append('make=' + make)
        filter_makes.append(make.upper())
    if model:
        lots = lots.filter(info__model=model)
        filter_word.append(model)
        initial_status.append('model=' + model)
        filter_models.append(model)
    if location:
        lots = lots.filter(info__location=location)
        filter_word.append(location)
        initial_status.append('location=' + location)

    ##########################
    for key, value in params.items():
        # AND condition filters
        if 'source' == key:
            filter_source = value
        elif 'featured' == key:
            filter_featured = value
        # OR condition filters
        elif 'makes' == key:
            filter_makes += value
        elif 'models' == key:
            filter_models += value
        elif 'years' == key:
            filter_years = value
        elif 'engine_types' == key:
            filter_engine_types += value
        elif 'transmissions' == key:
            filter_transmissions += value
        elif 'drive_trains' == key:
            filter_drive_trains += value
        elif 'fuels' == key:
            filter_fuels += value
        elif 'body_styles' == key:
            filter_body_styles += value

    ##########################

    ##########################
    def filter_by_filters(lots_, ignore=''):
        for param_key, param_value in params.items():
            # AND condition filters
            if 'source' == param_key and 'source' != ignore:
                if 'copart' == param_value:
                    lots_ = lots_.filter(info__source=True)
                elif 'iaai' == param_value:
                    lots_ = lots_.filter(info__source=False)
            elif 'featured' == param_key and 'featured' != ignore:
                for feature_ in param_value:
                    if 'Buy It Now' == feature_:
                        lots_ = lots_.filter(~Q(buy_today_bid=0))
                    elif 'Run and Drive' == feature_:
                        lots_ = lots_.filter(info__lot_highlights__contains='R')
                    elif 'Pure Sale Items' == feature_:
                        lots_ = lots_.filter(~Q(bid_status='PURE SALE'))
                    elif 'New Items' == feature_:
                        c_date = datetime.datetime.now().date()
                        f_date = c_date - datetime.timedelta(days=c_date.weekday() + 7)
                        t_date = f_date + datetime.timedelta(days=6)
                        lots_ = lots_.filter(created_at__range=(f_date, t_date))
            # OR condition filters
            elif 'makes' == param_key and 'makes' != ignore:
                query = Q(info__make__icontains=param_value[0])
                for make_ in param_value[1:]:
                    query |= Q(info__make__icontains=make_)
                lots_ = lots_.filter(query)
            elif 'models' == param_key and 'models' != ignore:
                query = Q(info__model=param_value[0])
                for model_ in param_value[1:]:
                    query |= Q(info__model=model_)
                lots_ = lots_.filter(query)
            elif 'years' == param_key and 'years' != ignore:
                query = Q(info__year=param_value[0])
                for year_ in param_value[1:]:
                    query |= Q(info__year=year_)
                lots_ = lots_.filter(query)
            elif 'odometers' == param_key and 'odometers' != ignore:
                pass
            elif 'locations' == param_key and 'locations' != ignore:
                query = Q(info__location=param_value[0])
                for location_ in param_value[1:]:
                    query |= Q(info__location=location_)
                lots_ = lots_.filter(query)
            elif 'sale_dates' == param_key and 'sale_dates' != ignore:
                query = Q(sale_date__year=str(param_value[0]).split('/')[2],
                          sale_date__month=str(param_value[0]).split('/')[0],
                          sale_date__day=str(param_value[0]).split('/')[1])
                for sale_date_ in param_value[1:]:
                    query |= Q(sale_date__year=str(sale_date_).split('/')[2],
                               sale_date__month=str(sale_date_).split('/')[0],
                               sale_date__day=str(sale_date_).split('/')[1])
                lots_ = lots_.filter(query)
            elif 'engine_types' == param_key and 'engine_types' != ignore:
                query = Q(info__engine_type=param_value[0])
                for engine_type_ in param_value[1:]:
                    query |= Q(info__engine_type=engine_type_)
                lots_ = lots_.filter(query)
            elif 'transmissions' == param_key and 'transmissions' != ignore:
                query = Q(info__transmission=param_value[0])
                for transmission_ in param_value[1:]:
                    query |= Q(info__transmission=transmission_)
                lots_ = lots_.filter(query)
            elif 'drive_trains' == param_key and 'drive_trains' != ignore:
                query = Q(info__drive=param_value[0])
                for drive_trains_ in param_value[1:]:
                    query |= Q(info__drive=drive_trains_)
                lots_ = lots_.filter(query)
            elif 'cylinderss' == param_key and 'cylinderss' != ignore:
                query = Q(info__cylinders=param_value[0])
                for cylinderss_ in param_value[1:]:
                    query |= Q(info__cylinders=cylinderss_)
                lots_ = lots_.filter(query)
            elif 'fuels' == param_key and 'fuels' != ignore:
                query = Q(info__fuel=param_value[0])
                for fuels_ in param_value[1:]:
                    query |= Q(info__fuel=fuels_)
                lots_ = lots_.filter(query)
            elif 'body_styles' == param_key and 'body_styles' != ignore:
                query = Q(info__body_style=param_value[0])
                for body_styles_ in param_value[1:]:
                    query |= Q(info__body_style=body_styles_)
                lots_ = lots_.filter(query)
            elif 'vehicle_types' == param_key and 'vehicle_types' != ignore:
                query = Q(info__type=param_value[0])
                for vehicle_types_ in param_value[1:]:
                    query |= Q(info__type=vehicle_types_)
                lots_ = lots_.filter(query)
            elif 'damages' == param_key and 'damages' != ignore:
                query = Q(info__lot_1st_damage=param_value[0])
                for damages_ in param_value[1:]:
                    query |= Q(info__lot_1st_damage=damages_)
                lots_ = lots_.filter(query)
            elif 'doctypes' == param_key and 'doctypes' != ignore:
                query = Q(info__doc_type_td__contains=str(param_value[0]).upper())
                for doctypes_ in param_value[1:]:
                    query |= Q(info__doc_type_td__contains=str(doctypes_).upper())
                lots_ = lots_.filter(query)

        return lots_

    ##########################

    featured_lots = filter_by_filters(lots).order_by(sort_direction + sort['sort_by'])
    if len(featured_lots) == 0:
        return redirect('/')

    make_lots = filter_by_filters(lots, 'makes')
    count_makes = sorted(list(set(make_lots.values_list('info__make', flat=True))))

    model_lots = filter_by_filters(lots, 'models')
    count_models = list(model_lots.values('info__model').annotate(model=F('info__model')).distinct())

    year_lots = filter_by_filters(lots, 'years')
    count_years = list(year_lots.values('info__year').annotate(year=F('info__year')).distinct()[::-1])

    engine_type_lots = filter_by_filters(lots, 'engine_types')
    count_engine_types = list(engine_type_lots.values('info__engine_type').annotate(engine_type=F('info__engine_type')).distinct())
    for sid, count_engine_type_ in enumerate(count_engine_types):
        if count_engine_type_['info__engine_type'] is None or count_engine_type_['info__engine_type'] == "":
            del count_engine_types[sid]

    transmission_lots = filter_by_filters(lots, 'transmissions')
    count_transmissions = list(transmission_lots.values('info__transmission').annotate(transmission=F('info__transmission')).distinct())
    for sid, count_transmission_ in enumerate(count_transmissions):
        if count_transmission_['info__transmission'] is None or count_transmission_['info__transmission'] == "":
            del count_transmissions[sid]

    drive_train_lots = filter_by_filters(lots, 'drive_trains')
    count_drive_trains = list(drive_train_lots.values('info__drive').annotate(drive=F('info__drive')).distinct())
    for sid, count_drive_train_ in enumerate(count_drive_trains):
        if count_drive_train_['info__drive'] is None or count_drive_train_['info__drive'] == "":
            del count_drive_trains[sid]

    fuel_lots = filter_by_filters(lots, 'fuels')
    count_fuels = list(fuel_lots.values('info__fuel').annotate(fuel=F('info__fuel')).distinct())
    for sid, count_fuel_ in enumerate(count_fuels):
        if count_fuel_['info__fuel'] is None or count_fuel_['info__fuel'] == "":
            del count_fuels[sid]

    body_style_lots = filter_by_filters(lots, 'body_styles')
    count_body_styles = list(body_style_lots.values('info__body_style').annotate(body_style=F('info__body_style')).distinct())
    for sid, count_body_style_ in enumerate(count_body_styles):
        if count_body_style_['info__body_style'] is None or count_body_style_['info__body_style'] == "":
            del count_body_styles[sid]

    page = int(request.GET.get('page', 1))
    entry = int(request.GET.get('entry', 20))

    paginator = Paginator(featured_lots, entry)
    if page > paginator.num_pages:
        print(request.get_full_path())
        redirect_url = request.get_full_path().split('&')
        for idx, param in enumerate(redirect_url):
            if param.startswith('page='):
                redirect_url[idx] = 'page=' + str(paginator.num_pages)
        return redirect('&'.join(redirect_url))
    paged_lots = paginator.get_page(page)

    pages = ['First', 'Previous']
    if paginator.num_pages <= 7:
        pages += [str(a + 1) for a in range(paginator.num_pages)]
    else:
        if page < 5:
            pages += [str(a + 1) for a in range(5)]
            pages.append('...')
            pages.append(str(paginator.num_pages))
        elif page > paginator.num_pages - 4:
            pages.append('1')
            pages.append('...')
            pages += [str(a + 1) for a in range(paginator.num_pages - 5, paginator.num_pages)]
        else:
            pages.append('1')
            pages.append('...')
            pages.append(str(page - 1))
            pages.append(str(page))
            pages.append(str(page + 1))
            pages.append('...')
            pages.append(str(paginator.num_pages))
    pages += ['Next', 'Last']

    context = {
        'lots': paged_lots,
        'total_lots': paginator.count,
        'pages': pages[::-1],
        'current_page': str(page),
        'current_entry': entry,
        'page_start_index': (page - 1) * entry + 1,
        'page_end_index': page * entry if page != paginator.num_pages else paginator.count,
        'filter_word': ', '.join(filter_word),

        'features': [
            {'feature': 'Buy It Now'},
            {'feature': 'Run and Drive'},
            {'feature': 'Pure Sale Items'},
            {'feature': 'New Items'}
        ],

        ###########################
        'makes': count_makes,
        'models': count_models,
        'years': count_years,
        'engine_types': count_engine_types,
        'transmissions': count_transmissions,
        'drive_trains': count_drive_trains,
        'fuels': count_fuels,
        'body_styles': count_body_styles,

        'applied_filter_source': filter_source,
        'applied_sold': '',
        'applied_filter_features': filter_featured,
        'applied_filter_makes': filter_makes,
        'applied_filter_models': filter_models,
        'applied_filter_years': filter_years,
        'applied_filter_engine_types': filter_engine_types,
        'applied_filter_transmissions': filter_transmissions,
        'applied_filter_drive_trains': filter_drive_trains,
        'applied_filter_fuels': filter_fuels,
        'applied_filter_body_styles': filter_body_styles,
        ###########################

        'initial': '&'.join(initial_status),
        'url': 'params=' + params_ + '&sort=' + sort_ if params_ else '',
        'status': status,

        'config': config,
    }

    return render(request, 'product/list_.html', context=context)


def ajax_lots_search(request):
    # get params from url
    vehicle_type = request.GET.get('type', '')
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')
    location = request.GET.get('location', '')
    params_ = request.GET.get('params', '')
    status = request.GET.get('status', '')
    feature = request.GET.get('feature', '')
    sort_ = request.GET.get('sort', '')

    if sort_:
        sort = eval(sort_)
        sort['sort_by'] = 'info__' + sort['sort_by']
    else:
        sort = dict(sort_by='info__year', sort_type='desc')

    sort_direction = ''
    if 'desc' == sort['sort_type']:
        sort_direction = '-'

    filter_word = []
    if vehicle_type:
        filter_word.append(dict(TYPES)[vehicle_type])

    params = {}
    # check if 'Show Real Price' checked
    sold = False
    if params_:
        params = eval(params_)
        if 'sold' in params and 'yes' == params['sold']:
            sold = True

    lots = VehicleSold.objects if sold else Vehicle.objects
    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filter_word.append(featured_filter.name)
        if 'Buy It Now' == featured_filter.name:
            lots = lots.filter(~Q(buy_today_bid=0))
        elif 'Pure Sale Items' == featured_filter.name:
            lots = lots.filter(~Q(bid_status='PURE SALE'))
        elif 'New Items' == featured_filter.name:
            cur_date = datetime.datetime.now().date()
            from_date = cur_date - datetime.timedelta(days=cur_date.weekday() + 7)
            to_date = from_date + datetime.timedelta(days=6)
            lots = lots.filter(created_at__range=(from_date, to_date))
        elif 'Lots with Bids' == featured_filter.name:
            lots = lots.filter(~Q(current_bid=0))
        elif 'No Bids Yet' == featured_filter.name:
            lots = lots.filter(current_bid=0)
        elif 'Hybrid Vehicles' == featured_filter.name:
            lots = lots.filter(info__fuel="HYBRID ENGINE")
        elif 'Repossessions' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='B')
        elif 'Donations' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='D').filter(~Q(lot_highlights="Did Not Test Start"))
        elif 'Featured Vehicles' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='F')
        elif 'Offsite Sales' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='O')
        elif 'Run and Drive' == featured_filter.name:
            lots = lots.filter(info__lot_highlights__contains='R')
        elif 'Clean Title' == featured_filter.name:
            lots = lots.filter(~Q(info__doc_type_td__icontains='salvage'))
        elif 'Salvage Title' == featured_filter.name:
            lots = lots.filter(info__doc_type_td__icontains='salvage')
        elif 'Front End' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Front End') or Q(info__2nd_damage__icontains='Front End'))
        elif 'Hail Damage' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Hail') or Q(info__lot_2nd_damage__icontains='Hail'))
        elif 'Normal Wear' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Normal Wear') or Q(info__lot_2nd_damage__icontains='Normal Wear'))
        elif 'Minor Dents/Scratch' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Minor') or Q(info__lot_2nd_damage__icontains='Minor'))
        elif 'Water/Flood' == featured_filter.name:
            lots = lots.filter(Q(info__lot_1st_damage__icontains='Water/Flood') or Q(info__lot_2nd_damage__icontains='Water/Flood'))
        else:
            lots = lots.all()

    ##########################
    filter_source = ''
    filter_featured = []
    filter_makes = []
    filter_models = []
    filter_years = []
    filter_engine_types = []
    filter_transmissions = []
    filter_drive_trains = []
    filter_fuels = []
    filter_body_styles = []
    ############################

    if vehicle_type:
        lots = lots.filter(info__type=vehicle_type)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        lots = lots.filter(info__year__range=(from_year, to_year))
        filter_word.append('[' + str(from_year) + ' TO ' + str(to_year) + ']')
    if make:
        lots = lots.filter(info__make__icontains=make)
        filter_word.append(make)
        filter_makes.append(make.upper())
    if model:
        lots = lots.filter(info__model=model)
        filter_word.append(model)
        filter_models.append(model)
    if location:
        lots = lots.filter(info__location=location)
        filter_word.append(location)

    ##########################
    for key, value in params.items():
        # AND condition filters
        if 'source' == key:
            filter_source = value
        elif 'featured' == key:
            filter_featured = value
        # OR condition filters
        elif 'makes' == key:
            filter_makes += value
        elif 'models' == key:
            filter_models += value
        elif 'years' == key:
            filter_years = value
        elif 'engine_types' == key:
            filter_engine_types += value
        elif 'transmissions' == key:
            filter_transmissions += value
        elif 'drive_trains' == key:
            filter_drive_trains += value
        elif 'fuels' == key:
            filter_fuels += value
        elif 'body_styles' == key:
            filter_body_styles += value

    ##########################

    ##########################
    def filter_by_filters(lots_, ignore=''):
        for param_key, param_value in params.items():
            # AND condition filters
            if 'source' == param_key and 'source' != ignore:
                if 'copart' == param_value:
                    lots_ = lots_.filter(info__source=True)
                elif 'iaai' == param_value:
                    lots_ = lots_.filter(info__source=False)
            elif 'featured' == param_key and 'featured' != ignore:
                for feature_ in param_value:
                    if 'Buy It Now' == feature_:
                        lots_ = lots_.filter(~Q(buy_today_bid=0))
                    elif 'Run and Drive' == feature_:
                        lots_ = lots_.filter(info__lot_highlights__contains='R')
                    elif 'Pure Sale Items' == feature_:
                        lots_ = lots_.filter(~Q(bid_status='PURE SALE'))
                    elif 'New Items' == feature_:
                        c_date = datetime.datetime.now().date()
                        f_date = c_date - datetime.timedelta(days=c_date.weekday() + 7)
                        t_date = f_date + datetime.timedelta(days=6)
                        lots_ = lots_.filter(created_at__range=(f_date, t_date))
            # OR condition filters
            elif 'makes' == param_key and 'makes' != ignore:
                query = Q(info__make__icontains=param_value[0])
                for make_ in param_value[1:]:
                    query |= Q(info__make__icontains=make_)
                lots_ = lots_.filter(query)
            elif 'models' == param_key and 'models' != ignore:
                query = Q(info__model=param_value[0])
                for model_ in param_value[1:]:
                    query |= Q(info__model=model_)
                lots_ = lots_.filter(query)
            elif 'years' == param_key and 'years' != ignore:
                query = Q(info__year=param_value[0])
                for year_ in param_value[1:]:
                    query |= Q(info__year=year_)
                lots_ = lots_.filter(query)
            elif 'odometers' == param_key and 'odometers' != ignore:
                pass
            elif 'locations' == param_key and 'locations' != ignore:
                query = Q(info__location=param_value[0])
                for location_ in param_value[1:]:
                    query |= Q(info__location=location_)
                lots_ = lots_.filter(query)
            elif 'sale_dates' == param_key and 'sale_dates' != ignore:
                query = Q(sale_date__year=str(param_value[0]).split('/')[2],
                          sale_date__month=str(param_value[0]).split('/')[0],
                          sale_date__day=str(param_value[0]).split('/')[1])
                for sale_date_ in param_value[1:]:
                    query |= Q(sale_date__year=str(sale_date_).split('/')[2],
                               sale_date__month=str(sale_date_).split('/')[0],
                               sale_date__day=str(sale_date_).split('/')[1])
                lots_ = lots_.filter(query)
            elif 'engine_types' == param_key and 'engine_types' != ignore:
                query = Q(info__engine_type=param_value[0])
                for engine_type_ in param_value[1:]:
                    query |= Q(info__engine_type=engine_type_)
                lots_ = lots_.filter(query)
            elif 'transmissions' == param_key and 'transmissions' != ignore:
                query = Q(info__transmission=param_value[0])
                for transmission_ in param_value[1:]:
                    query |= Q(info__transmission=transmission_)
                lots_ = lots_.filter(query)
            elif 'drive_trains' == param_key and 'drive_trains' != ignore:
                query = Q(info__drive=param_value[0])
                for drive_trains_ in param_value[1:]:
                    query |= Q(info__drive=drive_trains_)
                lots_ = lots_.filter(query)
            elif 'cylinderss' == param_key and 'cylinderss' != ignore:
                query = Q(info__cylinders=param_value[0])
                for cylinderss_ in param_value[1:]:
                    query |= Q(info__cylinders=cylinderss_)
                lots_ = lots_.filter(query)
            elif 'fuels' == param_key and 'fuels' != ignore:
                query = Q(info__fuel=param_value[0])
                for fuels_ in param_value[1:]:
                    query |= Q(info__fuel=fuels_)
                lots_ = lots_.filter(query)
            elif 'body_styles' == param_key and 'body_styles' != ignore:
                query = Q(info__body_style=param_value[0])
                for body_styles_ in param_value[1:]:
                    query |= Q(info__body_style=body_styles_)
                lots_ = lots_.filter(query)
            elif 'vehicle_types' == param_key and 'vehicle_types' != ignore:
                query = Q(info__type=param_value[0])
                for vehicle_types_ in param_value[1:]:
                    query |= Q(info__type=vehicle_types_)
                lots_ = lots_.filter(query)
            elif 'damages' == param_key and 'damages' != ignore:
                query = Q(info__lot_1st_damage=param_value[0])
                for damages_ in param_value[1:]:
                    query |= Q(info__lot_1st_damage=damages_)
                lots_ = lots_.filter(query)
            elif 'doctypes' == param_key and 'doctypes' != ignore:
                query = Q(info__doc_type_td__contains=str(param_value[0]).upper())
                for doctypes_ in param_value[1:]:
                    query |= Q(info__doc_type_td__contains=str(doctypes_).upper())
                lots_ = lots_.filter(query)

        return lots_

    ###################################
    make_lots = filter_by_filters(lots, 'makes')
    count_makes = sorted(list(set(make_lots.values_list('info__make', flat=True))))

    model_lots = filter_by_filters(lots, 'models')
    count_models = list(model_lots.values('info__model').annotate(model=F('info__model')).distinct())

    year_lots = filter_by_filters(lots, 'years')
    count_years = list(year_lots.values('info__year').annotate(year=F('info__year')).distinct()[::-1])

    engine_type_lots = filter_by_filters(lots, 'engine_types')
    count_engine_types = list(engine_type_lots.values('info__engine_type').annotate(engine_type=F('info__engine_type')).distinct())
    for sid, count_engine_type_ in enumerate(count_engine_types):
        if count_engine_type_['info__engine_type'] is None or count_engine_type_['info__engine_type'] == "":
            del count_engine_types[sid]

    transmission_lots = filter_by_filters(lots, 'transmissions')
    count_transmissions = list(transmission_lots.values('info__transmission').annotate(transmission=F('info__transmission')).distinct())
    for sid, count_transmission_ in enumerate(count_transmissions):
        if count_transmission_['info__transmission'] is None or count_transmission_['info__transmission'] == "":
            del count_transmissions[sid]

    drive_train_lots = filter_by_filters(lots, 'drive_trains')
    count_drive_trains = list(drive_train_lots.values('info__drive').annotate(drive=F('info__drive')).distinct())
    for sid, count_drive_train_ in enumerate(count_drive_trains):
        if count_drive_train_['info__drive'] is None or count_drive_train_['info__drive'] == "":
            del count_drive_trains[sid]

    fuel_lots = filter_by_filters(lots, 'fuels')
    count_fuels = list(fuel_lots.values('info__fuel').annotate(fuel=F('info__fuel')).distinct())
    for sid, count_fuel_ in enumerate(count_fuels):
        if count_fuel_['info__fuel'] is None or count_fuel_['info__fuel'] == "":
            del count_fuels[sid]

    body_style_lots = filter_by_filters(lots, 'body_styles')
    count_body_styles = list(body_style_lots.values('info__body_style').annotate(body_style=F('info__body_style')).distinct())
    for sid, count_body_style_ in enumerate(count_body_styles):
        if count_body_style_['info__body_style'] is None or count_body_style_['info__body_style'] == "":
            del count_body_styles[sid]

    lots = filter_by_filters(lots).order_by(sort_direction + sort['sort_by'])
    if len(lots) == 0:
        return redirect('/')

    page = int(request.GET.get('page', 1))
    entry = int(request.GET.get('entry', 20))

    paginator = Paginator(lots, entry)
    if page > paginator.num_pages:
        print(request.get_full_path())
        redirect_url = request.get_full_path().split('&')
        for idx, param in enumerate(redirect_url):
            if param.startswith('page='):
                redirect_url[idx] = 'page=' + str(paginator.num_pages)
        return redirect('&'.join(redirect_url))
    paged_lots = paginator.get_page(page)

    pages = ['First', 'Previous']
    if paginator.num_pages <= 7:
        pages += [str(a + 1) for a in range(paginator.num_pages)]
    else:
        if page < 5:
            pages += [str(a + 1) for a in range(5)]
            pages.append('...')
            pages.append(str(paginator.num_pages))
        elif page > paginator.num_pages - 4:
            pages.append('1')
            pages.append('...')
            pages += [str(a + 1) for a in range(paginator.num_pages - 5, paginator.num_pages)]
        else:
            pages.append('1')
            pages.append('...')
            pages.append(str(page - 1))
            pages.append(str(page))
            pages.append(str(page + 1))
            pages.append('...')
            pages.append(str(paginator.num_pages))
    pages += ['Next', 'Last']

    # result_lots = []
    # for a in paged_lots:
    #     a = a.__dict__
    #     del a['_state']
    #     result_lots.append(a)

    context = {
        'lots': paged_lots,
        'total_lots': paginator.count,
        'pages': pages[::-1],
        'current_page': str(page),
        'current_entry': entry,
        'page_start_index': (page - 1) * entry + 1,
        'page_end_index': page * entry if page != paginator.num_pages else paginator.count,
        'filter_word': ', '.join(filter_word),

        'features': [
            {'feature': 'Buy It Now'},
            {'feature': 'Run and Drive'},
            {'feature': 'Pure Sale Items'},
            {'feature': 'New Items'}
        ],

        'makes': count_makes,
        'models': count_models,
        'years': count_years,
        'engine_types': count_engine_types,
        'transmissions': count_transmissions,
        'drive_trains': count_drive_trains,
        'fuels': count_fuels,
        'body_styles': count_body_styles,

        'applied_filter_source': filter_source,
        'applied_sold': 'yes' if sold else '',
        'applied_filter_features': filter_featured,
        'applied_filter_makes': filter_makes,
        'applied_filter_models': filter_models,
        'applied_filter_years': filter_years,
        'applied_filter_engine_types': filter_engine_types,
        'applied_filter_transmissions': filter_transmissions,
        'applied_filter_drive_trains': filter_drive_trains,
        'applied_filter_fuels': filter_fuels,
        'applied_filter_body_styles': filter_body_styles,

        'status': status,

        'config': config,
    }
    return render(request, 'product/content_.html', context=context)


def test(request):
    return HttpResponse("Server is OK", content_type="text/plain")


@cache_page(CACHE_TTL)
def get_models_of_make_api(request):
    finder_type = request.GET.get('finder_type', '')
    finder_make = request.GET.get('finder_make', '')
    vehicle_makes = VehicleInfo.objects.filter(type=finder_type).filter(
        make__icontains=finder_make).values_list('model', flat=True)
    vehicle_makes = sorted(list(set(vehicle_makes)))
    return JsonResponse({
        'result': True,
        'models': [a for a in vehicle_makes],
    })


@cache_page(CACHE_TTL)
def status_api(request):
    context = {
        'status': ['Sites', 'Already Sold', 'Featured Items', 'Make']
    }
    return JsonResponse(context)


@cache_page(CACHE_TTL)
def years_api(request):
    context = {
        'year_range': list(range(1920, datetime.datetime.now().year + 2)[::-1]),
    }
    return JsonResponse(context)


@cache_page(CACHE_TTL)
def all_vehicle_makes_api(request):
    vehicle_type = request.GET.get('type', '')
    vehicle_all_makes = list(VehicleMakes.objects.values().filter(type=vehicle_type).order_by('code').distinct('code'))

    context = {
        'vehicle_all_makes': vehicle_all_makes,
    }
    return JsonResponse(context)


@cache_page(CACHE_TTL)
def locations_api(request):
    locations = list(Location.objects.all().values())
    # locations = serializers.serialize('python', Location.objects.all())

    context = {
        'locations': locations,
    }
    return JsonResponse(context)


@cache_page(CACHE_TTL)
def vehicle_makes_api(request):
    vehicle_makes = list(Filter.objects.values().filter(type='M').order_by('-count')[:55])
    # vehicle_makes = serializers.serialize('python', Filter.objects.filter(type='M').order_by('-count')[:55])

    context = {
        'vehicle_makes': vehicle_makes,
    }
    return JsonResponse(context)


@cache_page(CACHE_TTL)
def filtered_items_api(request):
    featured_filters = list(Filter.objects.values().filter(type='F'))

    context = {
        'featured_filters': featured_filters,
    }
    return JsonResponse(context)


@cache_page(CACHE_TTL)
def new_arrivals_api(request):
    new_arrivals = list(VehicleInfo.objects.values().filter(~Q(retail_value=0)).order_by('-id')[:12])

    context = {
        'arrivals': new_arrivals
    }
    return JsonResponse(context)


@cache_page(CACHE_TTL)
def vehicle_types_api(request):
    vehicle_types = list(Filter.objects.values().filter(type='T'))
    context = {
        'vehicle_types': vehicle_types
    }
    return JsonResponse(context)


@cache_page(CACHE_TTL)
def lots_by_summary_api(request):
    vehicle_type = request.GET.get('type', '')
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')
    location = request.GET.get('location', '')
    params_ = request.GET.get('params', '')
    feature = request.GET.get('feature', '')
    sort_ = request.GET.get('sort', '')

    if sort_:
        sort = eval(sort_)
        sort['sort_by'] = 'info__' + sort['sort_by']
    else:
        sort = dict(sort_by='info__year', sort_type='desc')

    sort_direction = ''
    if 'desc' == sort['sort_type']:
        sort_direction = '-'

    params = {}
    # check if 'Show Real Price' checked
    sold = False
    if params_:
        params = eval(params_)
        if 'sold' in params and 'yes' == params['sold']:
            sold = True

    lots = VehicleSold.objects if sold else Vehicle.objects

    filters = Q()

    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filters = set_filters_with_featured_name(filters, featured_filter.name)

    if vehicle_type:
        filters = filters & Q(info__type=vehicle_type)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        filters = filters & Q(info__year__range=(from_year, to_year))
    if make:
        filters = filters & Q(info__make__icontains=make)
    if model:
        filters = filters & Q(info__model=model)
    if location:
        filters = filters & Q(info__location=location)
    ##########################

    lots = lots.filter(filters)

    featured_lots = filter_by_filters(lots, params).order_by(sort_direction + sort['sort_by'])
    flfc21_count = featured_lots.filter(~Q(buy_today_bid=0)).count()
    flfc22_count = featured_lots.filter(info__lot_highlights__contains='R').count()
    flfc23_count = featured_lots.filter(~Q(bid_status='PURE SALE')).count()
    cur_date = datetime.datetime.now().date()
    from_date = cur_date - datetime.timedelta(days=cur_date.weekday() + 7)
    to_date = from_date + datetime.timedelta(days=6)
    flfc24_count = featured_lots.filter(created_at__range=(from_date, to_date)).count()
    #
    make_lots = filter_by_filters(lots, params, 'makes')
    count_makes = list(make_lots.values('info__make').annotate(make=F('info__make'), count=Count('info__make')))

    model_lots = filter_by_filters(lots, params, 'models')
    count_models = list(model_lots.values('info__model').annotate(model=F('info__model'), count=Count('info__model')))

    year_lots = filter_by_filters(lots, params, 'years')
    count_years = list(year_lots.values('info__year').annotate(year=F('info__year'), count=Count('info__year'))[::-1])

    location_lots = filter_by_filters(lots, params, 'locations')
    count_locations = list(location_lots.values('info__location').annotate(location=F('info__location'), count=Count('info__location')))

    sale_date_lots = filter_by_filters(lots, params, 'sale_dates').order_by('-sale_date')

    test = sale_date_lots.annotate(
        month=Cast(ExtractMonth('sale_date'), CharField()),
        day=Cast(ExtractDay('sale_date'), CharField()),
        year_test=Cast(ExtractYear('sale_date'), CharField()),
        sale_day=Concat('month', Value('/'), 'day', Value('/'), 'year_test')
    ).values('sale_day')

    res = test.values('sale_day').annotate(count=Count('sale_day'))

    temp_day = []
    temp_count = []
    for dat in res:
        if dat['sale_day'] not in temp_day:
            temp_day.append(dat['sale_day'])
            temp_count.append(dat['count'])
        else:
            temp_count[temp_day.index(dat['sale_day'])] = temp_count[temp_day.index(dat['sale_day'])] + dat['count']
    count_sale_dates = []
    for i, day in enumerate(temp_day):
        count_sale_dates.append({'sale_day': day, 'count': temp_count[i]})

    count_sale_dates_for_tag = count_sale_dates.copy()

    for sid, s in enumerate(count_sale_dates):
        if s['sale_day'] is None or s['sale_day'] == "" or s['sale_day'] == "//":
            del count_sale_dates[sid]
        else:
            if len(s['sale_day'].split('/')[0]) == 1:
                count_sale_dates[sid]['sale_day'] = "0" + count_sale_dates[sid]['sale_day']
            if len(s['sale_day'].split('/')[1]) == 1:
                count_sale_dates[sid]['sale_day'] = count_sale_dates[sid]['sale_day'][:3] \
                                                    + "0" + count_sale_dates[sid]['sale_day'][3:]

    engine_type_lots = filter_by_filters(lots, params, 'engine_types')
    count_engine_types = list(engine_type_lots.values('info__engine_type').annotate(engine_type=F('info__engine_type'), count=Count('info__engine_type')))
    for sid, count_engine_type_ in enumerate(count_engine_types):
        if count_engine_type_['info__engine_type'] is None or count_engine_type_['info__engine_type'] == "":
            del count_engine_types[sid]

    transmission_lots = filter_by_filters(lots, params, 'transmissions')
    count_transmissions = list(transmission_lots.values('info__transmission').annotate(transmission=F('info__transmission'), count=Count('info__transmission')))
    for sid, count_transmission_ in enumerate(count_transmissions):
        if count_transmission_['info__transmission'] is None or count_transmission_['info__transmission'] == "":
            del count_transmissions[sid]

    drive_train_lots = filter_by_filters(lots, params, 'drive_trains')
    count_drive_trains = list(drive_train_lots.values('info__drive').annotate(drive=F('info__drive'), count=Count('info__drive')))
    for sid, count_drive_train_ in enumerate(count_drive_trains):
        if count_drive_train_['info__drive'] is None or count_drive_train_['info__drive'] == "":
            del count_drive_trains[sid]

    cylinders_lots = filter_by_filters(lots, params, 'cylinderss')
    count_cylinderss = list(cylinders_lots.values('info__cylinders').annotate(cylinders=F('info__cylinders'), count=Count('info__cylinders')))
    for sid, count_cylinders_ in enumerate(count_cylinderss):
        if count_cylinders_['info__cylinders'] is None or count_cylinders_['info__cylinders'] == "":
            del count_cylinderss[sid]

    fuel_lots = filter_by_filters(lots, params, 'fuels')
    count_fuels = list(fuel_lots.values('info__fuel').annotate(fuel=F('info__fuel'), count=Count('info__fuel')))
    for sid, count_fuel_ in enumerate(count_fuels):
        if count_fuel_['info__fuel'] is None or count_fuel_['info__fuel'] == "":
            del count_fuels[sid]

    body_style_lots = filter_by_filters(lots, params, 'body_styles')
    count_body_styles = list(body_style_lots.values('info__body_style').annotate(body_style=F('info__body_style'), count=Count('info__body_style')))
    for sid, count_body_style_ in enumerate(count_body_styles):
        if count_body_style_['info__body_style'] is None or count_body_style_['info__body_style'] == "":
            del count_body_styles[sid]

    vehicle_type_lots = filter_by_filters(lots, params, 'vehicle_types')
    count_vehicle_types = list(vehicle_type_lots.values('info__type').annotate(type=F('info__type'), count=Count('info__type')))
    for sid, count_vehicle_type_ in enumerate(count_vehicle_types):
        if count_vehicle_type_['info__type'] is None or count_vehicle_type_['info__type'] == "":
            del count_vehicle_types[sid]
        else:
            count_vehicle_types[sid]['info__type'] = dict(TYPES)[count_vehicle_type_['info__type']]

    damage_lots = filter_by_filters(lots, params, 'damages')
    count_damages = list(damage_lots.values('info__lot_1st_damage').annotate(lot_1st_damage=F('info__lot_1st_damage'), count=Count('info__lot_1st_damage')))
    for sid, count_damage_ in enumerate(count_damages):
        if count_damage_['info__lot_1st_damage'] is None or count_damage_['info__lot_1st_damage'] == "":
            del count_damages[sid]

    doctype_lots = filter_by_filters(lots, params, 'doctypes')

    count_doctypes = []
    doctype_fields = ['Clean Title', 'Non-Repairable', 'Salvage Title']
    for doctype_field in doctype_fields:
        count_doctypes.append(
            {'doc_type_td': doctype_field,
             'count': doctype_lots.filter(info__doc_type_td__contains=str(doctype_field).upper()).count()})

    '''odometer_lots = filter_by_filters(lots, 'odometers')
    odometers = odometer_lots.raw(
        'SELECT ROW_NUMBER() OVER (ORDER BY 1) AS id,'
        'SUM(CASE WHEN odometer_orr < 25000 THEN 1 ELSE 0 END) AS count_0,'
        'SUM(CASE WHEN odometer_orr >= 25000 AND odometer_orr <= 50000 THEN 1 ELSE 0 END) AS count_1,'
        'SUM(CASE WHEN odometer_orr > 50000 AND odometer_orr <= 75000 THEN 1 ELSE 0 END) AS count_2,'
        'SUM(CASE WHEN odometer_orr > 75000 AND odometer_orr <= 100000 THEN 1 ELSE 0 END) AS count_3,'
        'SUM(CASE WHEN odometer_orr > 100000 AND odometer_orr <= 150000 THEN 1 ELSE 0 END) AS count_4,'
        'SUM(CASE WHEN odometer_orr > 150000 AND odometer_orr <= 200000 THEN 1 ELSE 0 END) AS count_5,'
        'SUM(CASE WHEN odometer_orr > 200000 THEN 1 ELSE 0 END) AS count_6 '
        'FROM product_vehicle')
    count_odometers = [
        {'odometer': '< 25,000', 'count': odometers[0].count_0},
        {'odometer': '25,000 to 50,000', 'count': odometers[0].count_1},
        {'odometer': '50,001 to 75,000', 'count': odometers[0].count_2},
        {'odometer': '75,001 to 100,000', 'count': odometers[0].count_3},
        {'odometer': '100,001 to 150,000', 'count': odometers[0].count_4},
        {'odometer': '150,001 to 200,000', 'count': odometers[0].count_5},
        {'odometer': '> 200,000', 'count': odometers[0].count_6},
    ]'''
    count_odometers = [
        {'odometer': '< 25,000', 'count': 0},
        {'odometer': '25,000 to 50,000', 'count': 0},
        {'odometer': '50,001 to 75,000', 'count': 0},
        {'odometer': '75,001 to 100,000', 'count': 0},
        {'odometer': '100,001 to 150,000', 'count': 0},
        {'odometer': '150,001 to 200,000', 'count': 0},
        {'odometer': '> 200,000', 'count': 0},
    ]

    context = {
        'features': [
            {'feature': 'Buy It Now', 'count': flfc21_count},
            {'feature': 'Run and Drive', 'count': flfc22_count},
            {'feature': 'Pure Sale Items', 'count': flfc23_count},
            {'feature': 'New Items', 'count': flfc24_count}
        ],
        'makes': list(count_makes),
        'models': list(count_models),
        'years': count_years,
        'odometers': count_odometers,
        'locations': count_locations,
        'sale_dates': count_sale_dates,
        'sale_dates_for_tag': count_sale_dates_for_tag,
        'engine_types': count_engine_types,
        'transmissions': count_transmissions,
        'drive_trains': count_drive_trains,
        'cylinders': count_cylinderss,
        'fuels': count_fuels,
        'body_styles': count_body_styles,
        'vehicle_types': count_vehicle_types,
        'damages': count_damages,
        'doctypes': count_doctypes,
    }

    return JsonResponse(context)


@cache_page(CACHE_TTL)
# @start_new_thread
def lots_paged_by_search_api(request):
    vehicle_type = request.GET.get('type', '')
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')
    location = request.GET.get('location', '')
    params_ = request.GET.get('params', '')
    feature = request.GET.get('feature', '')
    sort_ = request.GET.get('sort', '')

    if sort_:
        sort = eval(sort_)
        if sort['sort_by'] != 'sale_date' and sort['sort_by'] != 'current_bid':
            sort['sort_by'] = 'info__' + sort['sort_by']
    else:
        sort = dict(sort_by='info__year', sort_type='desc')

    sort_direction = ''
    if 'desc' == sort['sort_type']:
        sort_direction = '-'
    initial_status = []
    filter_word = []

    params = {}
    # check if 'Show Real Price' checked
    sold = False
    if params_:
        params = eval(params_)
        if 'sold' in params and 'yes' == params['sold']:
            sold = True

    lots = VehicleSold.objects if sold else Vehicle.objects

    filters = Q()

    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filters = set_filters_with_featured_name(filters, featured_filter.name)

    if vehicle_type:
        filters = filters & Q(info__type=vehicle_type)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        filters = filters & Q(info__year__range=(from_year, to_year))
    if make:
        filters = filters & Q(info__make__icontains=make)
    if model:
        filters = filters & Q(info__model=model)
    if location:
        filters = filters & Q(info__location=location)

    lots = lots.filter(filters)

    featured_lots = filter_by_filters(lots, params).order_by(sort_direction + sort['sort_by'])
    # searched_lot = featured_lots[0].to_json()
    # #

    page = int(request.GET.get('page', 1))
    entry = int(request.GET.get('entry', 20))

    paginator = Paginator(featured_lots, entry)
    paged_lots = paginator.get_page(page)
    # paged_lots = featured_lots[entry*(page-1):entry*page]

    pages = ['First', 'Previous']
    if paginator.num_pages <= 7:
        pages += [str(a + 1) for a in range(paginator.num_pages)]
    else:
        if page < 5:
            pages += [str(a + 1) for a in range(5)]
            pages.append('...')
            pages.append(str(paginator.num_pages))
        elif page > paginator.num_pages - 4:
            pages.append('1')
            pages.append('...')
            pages += [str(a + 1) for a in range(paginator.num_pages - 5, paginator.num_pages)]
        else:
            pages.append('1')
            pages.append('...')
            pages.append(str(page - 1))
            pages.append(str(page))
            pages.append(str(page + 1))
            pages.append('...')
            pages.append(str(paginator.num_pages))
    pages += ['Next', 'Last']

    def model_to_return(lot):
        info = model_to_dict(lot.info)
        lot = model_to_dict(lot)
        lot['info'] = info
        return lot
        # return lot.to_json()
    # return_lots = list(map(lambda x: model_to_dict(x), paged_lots))
    # return_lots = list(map(lambda x: model_to_return(x), paged_lots))
    return_lots = list(map(lambda x: x.to_json(), paged_lots))


    context = {
        'lots': return_lots,
        'total_lots': paginator.count,
        'pages': pages[::-1],
        'current_page': str(page),
        'current_entry': entry,
        'page_start_index': (page - 1) * entry + 1,
        'page_end_index': page * entry if page != paginator.num_pages else paginator.count
    }

    return JsonResponse(context)


# @cache_page(CACHE_TTL)
# @start_new_thread
def lots_count_searched_api(request):
    vehicle_type = request.GET.get('type', '')
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')
    location = request.GET.get('location', '')
    params_ = request.GET.get('params', '')
    feature = request.GET.get('feature', '')
    sort_ = request.GET.get('sort', '')

    if sort_:
        sort = eval(sort_)
        sort['sort_by'] = 'info__' + sort['sort_by']
    else:
        sort = dict(sort_by='info__year', sort_type='desc')

    sort_direction = ''
    if 'desc' == sort['sort_type']:
        sort_direction = '-'

    params = {}
    # check if 'Show Real Price' checked
    sold = False
    if params_:
        params = eval(params_)
        if 'sold' in params and 'yes' == params['sold']:
            sold = True

    lots = VehicleSold.objects.select_related('vehicle') if sold else Vehicle.objects.select_related('vehicle')
    lots_sold = VehicleSold.objects.select_related('vehicle')

    filters = Q()
    filters_sold = Q()

    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filters = set_filters_with_featured_name(filters, featured_filter.name)
    if vehicle_type:
        filters = filters & Q(info__type=vehicle_type)
        filters_sold = filters_sold & Q(info__type=vehicle_type)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        filters = filters & Q(info__year__range=(from_year, to_year))
    if make:
        filters = filters & Q(info__make__icontains=make)
        filters_sold = filters_sold & Q(info__make__icontains=make)
    if model:
        filters = filters & Q(info__model=model)
        filters_sold = filters_sold & Q(info__model=model)
    if location:
        filters = filters & Q(info__location=location)
        filters_sold = filters_sold & Q(info__location=location)

    lots = lots.filter(filters)

    copart_count = lots.filter(filters).filter(info__source=True).count()
    iaai_count = lots.filter(filters).filter(info__source=False).count()
    sold_count = lots_sold.filter(filters_sold).count()

    context = {
        'copart_count': copart_count,
        'iaai_count': iaai_count,
        'sold_count': sold_count,
        'config': {
            "SHOW_SOLD": config.SHOW_SOLD,
            "SHOW_SITES": config.SHOW_SITES,
            "SCRAP_IAAI_LOTS": config.SCRAP_IAAI_LOTS,
            "SCRAP_COPART_NOT_EXIST_LOTS": config.SCRAP_COPART_NOT_EXIST_LOTS,
            "SCRAP_COPART_LOTS": config.SCRAP_COPART_LOTS,
            "SCRAP_COPART_INSERT_ONLY": config.SCRAP_COPART_INSERT_ONLY,
            "SCRAP_COPART_AUCTIONS": config.SCRAP_COPART_AUCTIONS,
            "REMOVE_NOT_EXIST_LOTS": config.REMOVE_NOT_EXIST_LOTS
        }
    }

    return JsonResponse(context)


@cache_page(CACHE_TTL)
# @start_new_thread
def lots_by_summary_api_features_make_model(request):

    vehicle_type = request.GET.get('type', '')
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')
    location = request.GET.get('location', '')
    params_ = request.GET.get('params', '')
    feature = request.GET.get('feature', '')
    sort_ = request.GET.get('sort', '')

    if sort_:
        sort = eval(sort_)
        sort['sort_by'] = 'info__' + sort['sort_by']
    else:
        sort = dict(sort_by='info__year', sort_type='desc')

    sort_direction = ''
    if 'desc' == sort['sort_type']:
        sort_direction = '-'

    params = {}
    # check if 'Show Real Price' checked
    sold = False
    if params_:
        params = eval(params_)
        if 'sold' in params and 'yes' == params['sold']:
            sold = True

    lots = VehicleSold.objects.select_related('vehicle') if sold else Vehicle.objects.select_related('vehicle')

    filters = Q()

    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filters = set_filters_with_featured_name(filters, featured_filter.name)

    if vehicle_type:
        filters = filters & Q(info__type=vehicle_type)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        filters = filters & Q(info__year__range=(from_year, to_year))
    if make:
        filters = filters & Q(info__make__icontains=make)
    if model:
        filters = filters & Q(info__model=model)
    if location:
        filters = filters & Q(info__location=location)
    ##########################

    lots = lots.filter(filters)

    featured_lots = filter_by_filters(lots, params).order_by(sort_direction + sort['sort_by'])
    flfc21_count = featured_lots.filter(~Q(buy_today_bid=0)).count()
    flfc22_count = featured_lots.filter(info__lot_highlights__contains='R').count()
    flfc23_count = featured_lots.filter(~Q(bid_status='PURE SALE')).count()
    cur_date = datetime.datetime.now().date()
    from_date = cur_date - datetime.timedelta(days=cur_date.weekday() + 7)
    to_date = from_date + datetime.timedelta(days=6)
    flfc24_count = featured_lots.filter(created_at__range=(from_date, to_date)).count()
    #

    make_lots = filter_by_filters(lots, params, 'makes')
    count_makes = list(make_lots.values('info__make').order_by('info__make').annotate(make=F('info__make'), count=Count('info__make')))

    model_lots = filter_by_filters(lots, params, 'models')
    count_models = list(model_lots.values('info__model').order_by('info__model').annotate(model=F('info__model'), count=Count('info__model')))

    context = {
        'features': [
            {'feature': 'Buy It Now', 'count': flfc21_count},
            {'feature': 'Run and Drive', 'count': flfc22_count},
            {'feature': 'Pure Sale Items', 'count': flfc23_count},
            {'feature': 'New Items', 'count': flfc24_count}
        ],
        'makes': list(count_makes),
        'models': list(count_models),
    }

    return JsonResponse(context)


@cache_page(CACHE_TTL)
# @start_new_thread
def lots_by_summary_api_features(request):

    vehicle_type = request.GET.get('type', '')
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')
    location = request.GET.get('location', '')
    params_ = request.GET.get('params', '')
    feature = request.GET.get('feature', '')
    sort_ = request.GET.get('sort', '')

    if sort_:
        sort = eval(sort_)
        sort['sort_by'] = 'info__' + sort['sort_by']
    else:
        sort = dict(sort_by='info__year', sort_type='desc')

    sort_direction = ''
    if 'desc' == sort['sort_type']:
        sort_direction = '-'

    params = {}
    # check if 'Show Real Price' checked
    sold = False
    if params_:
        params = eval(params_)
        if 'sold' in params and 'yes' == params['sold']:
            sold = True

    lots = VehicleSold.objects.select_related('vehicle') if sold else Vehicle.objects.select_related('vehicle')

    filters = Q()

    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filters = set_filters_with_featured_name(filters, featured_filter.name)

    if vehicle_type:
        filters = filters & Q(info__type=vehicle_type)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        filters = filters & Q(info__year__range=(from_year, to_year))
    if make:
        filters = filters & Q(info__make__icontains=make)
    if model:
        filters = filters & Q(info__model=model)
    if location:
        filters = filters & Q(info__location=location)
    ##########################

    lots = lots.filter(filters)

    featured_lots = filter_by_filters(lots, params).order_by(sort_direction + sort['sort_by'])
    flfc21_count = featured_lots.filter(~Q(buy_today_bid=0)).count()
    flfc22_count = featured_lots.filter(info__lot_highlights__contains='R').count()
    flfc23_count = featured_lots.filter(~Q(bid_status='PURE SALE')).count()
    cur_date = datetime.datetime.now().date()
    from_date = cur_date - datetime.timedelta(days=cur_date.weekday() + 7)
    to_date = from_date + datetime.timedelta(days=6)
    flfc24_count = featured_lots.filter(created_at__range=(from_date, to_date)).count()

    context = {
        'features': [
            {'feature': 'Buy It Now', 'count': flfc21_count},
            {'feature': 'Run and Drive', 'count': flfc22_count},
            {'feature': 'Pure Sale Items', 'count': flfc23_count},
            {'feature': 'New Items', 'count': flfc24_count}
        ]
    }

    return JsonResponse(context)


@cache_page(CACHE_TTL)
# @start_new_thread
def lots_by_summary_api_make(request):

    vehicle_type = request.GET.get('type', '')
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')
    location = request.GET.get('location', '')
    params_ = request.GET.get('params', '')
    feature = request.GET.get('feature', '')
    sort_ = request.GET.get('sort', '')

    if sort_:
        sort = eval(sort_)
        sort['sort_by'] = 'info__' + sort['sort_by']
    else:
        sort = dict(sort_by='info__year', sort_type='desc')

    sort_direction = ''
    if 'desc' == sort['sort_type']:
        sort_direction = '-'

    params = {}
    # check if 'Show Real Price' checked
    sold = False
    if params_:
        params = eval(params_)
        if 'sold' in params and 'yes' == params['sold']:
            sold = True

    lots = VehicleSold.objects.select_related('vehicle') if sold else Vehicle.objects.select_related('vehicle')

    filters = Q()

    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filters = set_filters_with_featured_name(filters, featured_filter.name)

    if vehicle_type:
        filters = filters & Q(info__type=vehicle_type)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        filters = filters & Q(info__year__range=(from_year, to_year))
    if make:
        filters = filters & Q(info__make__icontains=make)
    if model:
        filters = filters & Q(info__model=model)
    if location:
        filters = filters & Q(info__location=location)
    ##########################

    lots = lots.filter(filters)

    make_lots = filter_by_filters(lots, params, 'makes')
    count_makes = list(make_lots.values('info__make').annotate(make=F('info__make'), count=Count('info__make')))

    context = {
        'makes': list(count_makes)
    }

    return JsonResponse(context)


@cache_page(CACHE_TTL)
# @start_new_thread
def lots_by_summary_api_model(request):

    vehicle_type = request.GET.get('type', '')
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')
    location = request.GET.get('location', '')
    params_ = request.GET.get('params', '')
    feature = request.GET.get('feature', '')
    sort_ = request.GET.get('sort', '')

    if sort_:
        sort = eval(sort_)
        sort['sort_by'] = 'info__' + sort['sort_by']
    else:
        sort = dict(sort_by='info__year', sort_type='desc')

    sort_direction = ''
    if 'desc' == sort['sort_type']:
        sort_direction = '-'

    params = {}
    # check if 'Show Real Price' checked
    sold = False
    if params_:
        params = eval(params_)
        if 'sold' in params and 'yes' == params['sold']:
            sold = True

    lots = VehicleSold.objects.select_related('vehicle') if sold else Vehicle.objects.select_related('vehicle')

    filters = Q()

    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filters = set_filters_with_featured_name(filters, featured_filter.name)

    if vehicle_type:
        filters = filters & Q(info__type=vehicle_type)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        filters = filters & Q(info__year__range=(from_year, to_year))
    if make:
        filters = filters & Q(info__make__icontains=make)
    if model:
        filters = filters & Q(info__model=model)
    if location:
        filters = filters & Q(info__location=location)
    ##########################

    lots = lots.filter(filters)

    model_lots = filter_by_filters(lots, params, 'models')
    count_models = list(model_lots.values('info__model').annotate(model=F('info__model'), count=Count('info__model')))

    context = {
        'models': list(count_models),
    }

    return JsonResponse(context)


@cache_page(CACHE_TTL)
# @start_new_thread
def lots_by_summary_api_year_date(request):

    vehicle_type = request.GET.get('type', '')
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')
    location = request.GET.get('location', '')
    params_ = request.GET.get('params', '')
    feature = request.GET.get('feature', '')
    sort_ = request.GET.get('sort', '')

    if sort_:
        sort = eval(sort_)
        sort['sort_by'] = 'info__' + sort['sort_by']
    else:
        sort = dict(sort_by='info__year', sort_type='desc')

    sort_direction = ''
    if 'desc' == sort['sort_type']:
        sort_direction = '-'

    params = {}
    # check if 'Show Real Price' checked
    sold = False
    if params_:
        params = eval(params_)
        if 'sold' in params and 'yes' == params['sold']:
            sold = True

    lots = VehicleSold.objects.select_related('vehicle') if sold else Vehicle.objects.select_related('vehicle')

    filters = Q()

    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filters = set_filters_with_featured_name(filters, featured_filter.name)

    if vehicle_type:
        filters = filters & Q(info__type=vehicle_type)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        filters = filters & Q(info__year__range=(from_year, to_year))
    if make:
        filters = filters & Q(info__make__icontains=make)
    if model:
        filters = filters & Q(info__model=model)
    if location:
        filters = filters & Q(info__location=location)
    ##########################

    lots = lots.filter(filters)

    year_lots = filter_by_filters(lots, params, 'years')
    count_years = list(year_lots.values('info__year').order_by('info__year').annotate(year=F('info__year'), count=Count('info__year'))[::-1])

    location_lots = filter_by_filters(lots, params, 'locations')
    count_locations = list(location_lots.values('info__location').order_by('info__location').annotate(location=F('info__location'), count=Count('info__location')))

    sale_date_lots = filter_by_filters(lots, params, 'sale_dates').order_by('-sale_date')

    test = sale_date_lots.annotate(
        month=Cast(ExtractMonth('sale_date'), CharField()),
        day=Cast(ExtractDay('sale_date'), CharField()),
        year_test=Cast(ExtractYear('sale_date'), CharField()),
        sale_day=Concat('month', Value('/'), 'day', Value('/'), 'year_test')
    ).values('sale_day')

    res = test.values('sale_day').annotate(count=Count('sale_day'))

    temp_day = []
    temp_count = []
    for dat in res:
        if dat['sale_day'] not in temp_day:
            temp_day.append(dat['sale_day'])
            temp_count.append(dat['count'])
        else:
            temp_count[temp_day.index(dat['sale_day'])] = temp_count[temp_day.index(dat['sale_day'])] + dat['count']
    count_sale_dates = []
    for i, day in enumerate(temp_day):
        count_sale_dates.append({'sale_day': day, 'count': temp_count[i]})

    count_sale_dates_for_tag = count_sale_dates.copy()

    context = {

        'years': count_years,
        'locations': count_locations,
        'sale_dates': count_sale_dates,
    }

    return JsonResponse(context)


@cache_page(CACHE_TTL)
# @start_new_thread
def lots_by_summary_api_vehicle_damage(request):

    vehicle_type = request.GET.get('type', '')
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')
    location = request.GET.get('location', '')
    params_ = request.GET.get('params', '')
    feature = request.GET.get('feature', '')
    sort_ = request.GET.get('sort', '')

    if sort_:
        sort = eval(sort_)
        sort['sort_by'] = 'info__' + sort['sort_by']
    else:
        sort = dict(sort_by='info__year', sort_type='desc')

    sort_direction = ''
    if 'desc' == sort['sort_type']:
        sort_direction = '-'

    params = {}
    # check if 'Show Real Price' checked
    sold = False
    if params_:
        params = eval(params_)
        if 'sold' in params and 'yes' == params['sold']:
            sold = True

    lots = VehicleSold.objects.select_related('vehicle') if sold else Vehicle.objects.select_related('vehicle')

    filters = Q()

    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filters = set_filters_with_featured_name(filters, featured_filter.name)

    if vehicle_type:
        filters = filters & Q(info__type=vehicle_type)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        filters = filters & Q(info__year__range=(from_year, to_year))
    if make:
        filters = filters & Q(info__make__icontains=make)
    if model:
        filters = filters & Q(info__model=model)
    if location:
        filters = filters & Q(info__location=location)
    ##########################

    lots = lots.filter(filters)

    vehicle_type_lots = filter_by_filters(lots, params, 'vehicle_types')
    count_vehicle_types = list(vehicle_type_lots.values('info__type').order_by('info__type').annotate(type=F('info__type'), count=Count('info__type')))
    for sid, count_vehicle_type_ in enumerate(count_vehicle_types):
        if count_vehicle_type_['info__type'] is None or count_vehicle_type_['info__type'] == "":
            del count_vehicle_types[sid]
        else:
            count_vehicle_types[sid]['info__type'] = dict(TYPES)[count_vehicle_type_['info__type']]

    damage_lots = filter_by_filters(lots, params, 'damages')
    count_damages = list(damage_lots.values('info__lot_1st_damage').order_by('info__lot_1st_damage').annotate(lot_1st_damage=F('info__lot_1st_damage'), count=Count('info__lot_1st_damage')))
    for sid, count_damage_ in enumerate(count_damages):
        if count_damage_['info__lot_1st_damage'] is None or count_damage_['info__lot_1st_damage'] == "":
            del count_damages[sid]

    doctype_lots = filter_by_filters(lots, params, 'doctypes')

    count_doctypes = []
    doctype_fields = ['Clean Title', 'Non-Repairable', 'Salvage Title']
    for doctype_field in doctype_fields:
        count_doctypes.append(
            {'doc_type_td': doctype_field,
             'count': doctype_lots.filter(info__doc_type_td__contains=str(doctype_field).upper()).count()})

    '''odometer_lots = filter_by_filters(lots, 'odometers')
    odometers = odometer_lots.raw(
        'SELECT ROW_NUMBER() OVER (ORDER BY 1) AS id,'
        'SUM(CASE WHEN odometer_orr < 25000 THEN 1 ELSE 0 END) AS count_0,'
        'SUM(CASE WHEN odometer_orr >= 25000 AND odometer_orr <= 50000 THEN 1 ELSE 0 END) AS count_1,'
        'SUM(CASE WHEN odometer_orr > 50000 AND odometer_orr <= 75000 THEN 1 ELSE 0 END) AS count_2,'
        'SUM(CASE WHEN odometer_orr > 75000 AND odometer_orr <= 100000 THEN 1 ELSE 0 END) AS count_3,'
        'SUM(CASE WHEN odometer_orr > 100000 AND odometer_orr <= 150000 THEN 1 ELSE 0 END) AS count_4,'
        'SUM(CASE WHEN odometer_orr > 150000 AND odometer_orr <= 200000 THEN 1 ELSE 0 END) AS count_5,'
        'SUM(CASE WHEN odometer_orr > 200000 THEN 1 ELSE 0 END) AS count_6 '
        'FROM product_vehicle')
    count_odometers = [
        {'odometer': '< 25,000', 'count': odometers[0].count_0},
        {'odometer': '25,000 to 50,000', 'count': odometers[0].count_1},
        {'odometer': '50,001 to 75,000', 'count': odometers[0].count_2},
        {'odometer': '75,001 to 100,000', 'count': odometers[0].count_3},
        {'odometer': '100,001 to 150,000', 'count': odometers[0].count_4},
        {'odometer': '150,001 to 200,000', 'count': odometers[0].count_5},
        {'odometer': '> 200,000', 'count': odometers[0].count_6},
    ]'''
    count_odometers = [
        {'odometer': '< 25,000', 'count': 0},
        {'odometer': '25,000 to 50,000', 'count': 0},
        {'odometer': '50,001 to 75,000', 'count': 0},
        {'odometer': '75,001 to 100,000', 'count': 0},
        {'odometer': '100,001 to 150,000', 'count': 0},
        {'odometer': '150,001 to 200,000', 'count': 0},
        {'odometer': '> 200,000', 'count': 0},
    ]

    context = {
        'odometers': count_odometers,
        'vehicle_types': count_vehicle_types,
        'damages': count_damages,
        'doctypes': count_doctypes,
    }

    return JsonResponse(context)


@cache_page(CACHE_TTL)
# @start_new_thread
def lots_by_summary_api_fuel(request):

    vehicle_type = request.GET.get('type', '')
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')
    location = request.GET.get('location', '')
    params_ = request.GET.get('params', '')
    feature = request.GET.get('feature', '')
    sort_ = request.GET.get('sort', '')

    if sort_:
        sort = eval(sort_)
        sort['sort_by'] = 'info__' + sort['sort_by']
    else:
        sort = dict(sort_by='info__year', sort_type='desc')

    sort_direction = ''
    if 'desc' == sort['sort_type']:
        sort_direction = '-'

    params = {}
    # check if 'Show Real Price' checked
    sold = False
    if params_:
        params = eval(params_)
        if 'sold' in params and 'yes' == params['sold']:
            sold = True

    lots = VehicleSold.objects.select_related('vehicle') if sold else Vehicle.objects.select_related('vehicle')

    filters = Q()

    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filters = set_filters_with_featured_name(filters, featured_filter.name)

    if vehicle_type:
        filters = filters & Q(info__type=vehicle_type)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        filters = filters & Q(info__year__range=(from_year, to_year))
    if make:
        filters = filters & Q(info__make__icontains=make)
    if model:
        filters = filters & Q(info__model=model)
    if location:
        filters = filters & Q(info__location=location)
    ##########################

    lots = lots.filter(filters)

    engine_type_lots = filter_by_filters(lots, params, 'engine_types')
    count_engine_types = list(engine_type_lots.values('info__engine_type').order_by('info__engine_type').annotate(engine_type=F('info__engine_type'), count=Count('info__engine_type')))
    for sid, count_engine_type_ in enumerate(count_engine_types):
        if count_engine_type_['info__engine_type'] is None or count_engine_type_['info__engine_type'] == "":
            del count_engine_types[sid]

    fuel_lots = filter_by_filters(lots, params, 'fuels')
    count_fuels = list(fuel_lots.values('info__fuel').order_by('info__fuel').annotate(fuel=F('info__fuel'), count=Count('info__fuel')))
    for sid, count_fuel_ in enumerate(count_fuels):
        if count_fuel_['info__fuel'] is None or count_fuel_['info__fuel'] == "":
            del count_fuels[sid]

    body_style_lots = filter_by_filters(lots, params, 'body_styles')
    count_body_styles = list(body_style_lots.values('info__body_style').order_by('info__body_style').annotate(body_style=F('info__body_style'), count=Count('info__body_style')))
    for sid, count_body_style_ in enumerate(count_body_styles):
        if count_body_style_['info__body_style'] is None or count_body_style_['info__body_style'] == "":
            del count_body_styles[sid]
    context = {
        'engine_types': count_engine_types,
        'fuels': count_fuels,
        'body_styles': count_body_styles,
    }

    return JsonResponse(context)


@cache_page(CACHE_TTL)
# @start_new_thread
def lots_by_summary_api_transmission(request):

    vehicle_type = request.GET.get('type', '')
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')
    location = request.GET.get('location', '')
    params_ = request.GET.get('params', '')
    feature = request.GET.get('feature', '')
    sort_ = request.GET.get('sort', '')

    if sort_:
        sort = eval(sort_)
        sort['sort_by'] = 'info__' + sort['sort_by']
    else:
        sort = dict(sort_by='info__year', sort_type='desc')

    sort_direction = ''
    if 'desc' == sort['sort_type']:
        sort_direction = '-'

    params = {}
    # check if 'Show Real Price' checked
    sold = False
    if params_:
        params = eval(params_)
        if 'sold' in params and 'yes' == params['sold']:
            sold = True

    lots = VehicleSold.objects.select_related('vehicle') if sold else Vehicle.objects.select_related('vehicle')

    filters = Q()

    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filters = set_filters_with_featured_name(filters, featured_filter.name)

    if vehicle_type:
        filters = filters & Q(info__type=vehicle_type)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        filters = filters & Q(info__year__range=(from_year, to_year))
    if make:
        filters = filters & Q(info__make__icontains=make)
    if model:
        filters = filters & Q(info__model=model)
    if location:
        filters = filters & Q(info__location=location)
    ##########################

    lots = lots.filter(filters)

    transmission_lots = filter_by_filters(lots, params, 'transmissions')
    count_transmissions = list(transmission_lots.values('info__transmission').order_by('info__transmission').annotate(transmission=F('info__transmission'), count=Count('info__transmission')))
    for sid, count_transmission_ in enumerate(count_transmissions):
        if count_transmission_['info__transmission'] is None or count_transmission_['info__transmission'] == "":
            del count_transmissions[sid]

    drive_train_lots = filter_by_filters(lots, params, 'drive_trains')
    count_drive_trains = list(drive_train_lots.values('info__drive').order_by('info__drive').annotate(drive=F('info__drive'), count=Count('info__drive')))
    for sid, count_drive_train_ in enumerate(count_drive_trains):
        if count_drive_train_['info__drive'] is None or count_drive_train_['info__drive'] == "":
            del count_drive_trains[sid]

    cylinders_lots = filter_by_filters(lots, params, 'cylinderss')
    count_cylinderss = list(cylinders_lots.values('info__cylinders').order_by('info__cylinders').annotate(cylinders=F('info__cylinders'), count=Count('info__cylinders')))
    for sid, count_cylinders_ in enumerate(count_cylinderss):
        if count_cylinders_['info__cylinders'] is None or count_cylinders_['info__cylinders'] == "":
            del count_cylinderss[sid]

    context = {

        'transmissions': count_transmissions,
        'drive_trains': count_drive_trains,
        'cylinders': count_cylinderss,
    }

    return JsonResponse(context)


@cache_page(CACHE_TTL)
# @start_new_thread
def detail_api_similar(request, lot):
    lots = Vehicle.objects.filter(info__lot=int(lot)).order_by('-created_at')
    if len(lots) == 0:
        lots = VehicleSold.objects.filter(info__lot=int(lot)).order_by('-created_at')
        if len(lots) == 0:
            return JsonResponse({"Waring": 'Data is not exist'})
    lotDetail = lots[0]

    is_similar = True
    similar = Vehicle.objects.filter(info__make=lotDetail.info.make)\
        .filter(info__model=lotDetail.info.model).filter(info__year=lotDetail.info.year).filter(~Q(info__lot=int(lotDetail.info.lot))).order_by('-id')
    if len(similar) >= 12:
        similar = similar[:12]
    else:
        similar = Vehicle.objects.filter(info__make=lotDetail.info.make)\
            .filter(info__model=lotDetail.info.model).filter(~Q(info__lot=int(lotDetail.info.lot))).order_by('-id')
        if len(similar) >= 12:
            similar = similar[:12]
        else:
            similar = Vehicle.objects.filter(info__make=lotDetail.info.make).filter(~Q(info__lot=int(lotDetail.info.lot))).order_by('-id')
            if len(similar) >= 12:
                similar = similar[:12]
            else:
                similar = Vehicle.objects.filter(~Q(info__retail_value=0)).filter(~Q(info__lot=int(lotDetail.info.lot))).order_by('-id')[:12]
                is_similar = False

    context = {'similar': list(map(lambda x: x.to_json(), similar)), 'is_similar': is_similar}
    return JsonResponse(context)


@cache_page(CACHE_TTL)
# @start_new_thread
def detail_api_info(request, lot):
    context = {'sold': False}
    lot_details = Vehicle.objects.filter(info__lot=int(lot)).order_by('created_at')
    if len(lot_details) == 0:
        context['sold'] = True
        lot_details = VehicleSold.objects.filter(info__lot=int(lot)).order_by('-created_at')
        if len(lot_details) == 0:
            return JsonResponse({'status': "Could not find"})
    lot_detail = lot_details[0]
    context['lot'] = lot_detail.to_json()
    return JsonResponse(context)


@cache_page(CACHE_TTL)
# @start_new_thread
def details_api_bid_info(request, vin):

    vehicles = list(map(lambda x: x.to_json(), Vehicle.objects.filter(info__vin=vin).order_by('-created_at')))

    vehicle_solds = list(map(lambda x: x.to_json(), VehicleSold.objects.filter(info__vin=vin).order_by('-info_id', '-created_at').distinct('info_id')))

    return JsonResponse({'solds': vehicle_solds, 'vehicle': vehicles})


@cache_page(CACHE_TTL)
# @start_new_thread
def details_api_winning_bid_info(request, lot):
    vehicle_solds = list(map(lambda x: x.to_json(), VehicleSold.objects.filter(info__lot=lot).exclude(sold_price=0).order_by('-created_at')))
    return JsonResponse({'solds': vehicle_solds})


@cache_page(CACHE_TTL)
# @start_new_thread
def get_api_chart_data(request):
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')

    lots = VehicleSold.objects.filter(Q(sale_status='SOLD') & Q(info__year=year) & Q(info__make__icontains=make) & Q(info__model=model)).order_by('info__vin', '-sale_date').distinct('info__vin')

    data = VehicleSold.objects.filter(Q(sale_status='SOLD') & Q(info__year=int(year)) & Q(info__make__icontains=make) & Q(info__model=model)).aggregate(Avg('sold_price'), Min('sold_price'), Max('sold_price'))

    context = {
        'lots': list(map(lambda x: x.to_json(), lots)),
        'data': data
    }

    return JsonResponse(context)


@cache_page(CACHE_TTL)
# @start_new_thread
def get_api_lot_or_vin(request, id):
    vehicle = VehicleInfo.objects.values('lot').filter(vin=id).order_by('id')[:1]
    if len(vehicle) > 0:
        return JsonResponse({'lot': vehicle[0]['lot'], "status": True})
    vehicle = VehicleInfo.objects.filter(lot=int(id))
    if len(vehicle) > 0:
        return JsonResponse({"lot": id, "status": True})
    return JsonResponse({'status': False})


@cache_page(CACHE_TTL)
# @start_new_thread
def api_filter_key(request):
    vehicle_type = request.GET.get('type', '')
    year = request.GET.get('year', '')
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')
    location = request.GET.get('location', '')
    feature = request.GET.get('feature', '')

    filter_word = []
    if vehicle_type:
        filter_word.append(dict(TYPES)[vehicle_type])
    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filter_word.append(featured_filter.name)
    ##########################
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        filter_word.append('[' + str(from_year) + ' TO ' + str(to_year) + ']')
    if make:
        filter_word.append(make)
    if model:
        filter_word.append(model)
    if location:
        filter_word.append(location)

    context = {
        'filter_word': ', '.join(filter_word)
    }

    return JsonResponse(context)
