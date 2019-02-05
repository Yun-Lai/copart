import datetime
from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.db.models.functions import Trunc, TruncYear, TruncDate
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import translation
from django.db.models import Q, Count, CharField, Value
from django.db.models.functions import Cast, ExtractDay, ExtractMonth, ExtractYear, Concat

from product.tasks import *
from product.models import Vehicle, VehicleSold, VehicleMakes, Filter, Location, TYPES


# def switch_language(request, language):
#     translation.activate(language)
#     request.session[translation.LANGUAGE_SESSION_KEY] = language
#     return redirect('/admin/')

# def custom_redirect(url_name, *args, **kwargs):
#     url = reverse(url_name, args=args)
#     params = urlencode(kwargs)
#     return HttpResponseRedirect(url + "?%s" % params)

class SaleDateModel(models.Model):
    sale_day = models.CharField(null=True, blank=True, max_length=12)


def view_scrap_copart_all(request):
    scrap_copart_all.delay()

    return redirect('/admin/')


def view_scrap_copart(request):
    make_id = request.GET.get('id')
    scrap_copart_lots.delay([make_id], {'username': 'vdm.cojocaru@gmail.com', 'password': 'c0p2rt'})

    return redirect('/admin/product/vehiclemakes/')


def view_scrap_iaai(request):
    scrap_iaai_lots.delay()

    return redirect('/admin/')


def view_scrap_auction(request):
    scrap_live_auctions.delay()

    return redirect('/admin/')


def view_scrap_filters_count(request):
    scrap_filters_count.delay()

    return redirect('/admin/')


def view_find_correct_vin(request):
    find_correct_vin.delay()

    return redirect('/admin/')


def view_remove_unavailable_lots(request):
    remove_unavailable_lots.delay()

    return redirect('/admin/')


def ajax_getimages(request):
    lot_id = request.POST.get('lot', '')

    if not lot_id:
        return JsonResponse({'result': False})

    lot = Vehicle.objects.get(lot=int(lot_id))
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
        if Vehicle.objects.filter(lot=int(vin_or_lot)).exists():
            return JsonResponse({'result': True, 'lot': vin_or_lot})
    lot = Vehicle.objects.filter(vin=vin_or_lot).order_by('-id')
    if len(lot):
        return JsonResponse({'result': True, 'lot': lot[0].lot})
    return JsonResponse({'result': False})


def view_ajax_get_makes_of_type(request):
    finder_type = request.GET.get('finder_type', '')
    vehicle_makes = VehicleMakes.objects.filter(type=finder_type)
    return JsonResponse({
        'result': True,
        'makes': [a.description for a in vehicle_makes],
    })


def view_ajax_get_models_of_make(request):
    finder_type = request.GET.get('finder_type', '')
    finder_make = request.GET.get('finder_make', '')
    vehicle_makes = Vehicle.objects.filter(type=finder_type).filter(make__icontains=finder_make).values_list('model',
                                                                                                             flat=True)
    vehicle_makes = sorted(list(set(vehicle_makes)))
    return JsonResponse({
        'result': True,
        'models': [a for a in vehicle_makes],
    })


def index(request):
    new_arrivals = Vehicle.objects.filter(~Q(retail_value=0)).order_by('-id')[:12]
    featured_filters = Filter.objects.filter(type='F')
    vehicle_types = Filter.objects.filter(type='T')
    vehicle_makes = Filter.objects.filter(type='M').order_by('-count')[:55]
    locations = Location.objects.all()

    context = {
        'arrivals': new_arrivals,
        'featured_filters': featured_filters,
        'vehicle_types': vehicle_types,
        'vehicle_makes': vehicle_makes,
        'locations': locations,
        'year_range': range(1920, datetime.datetime.now().year + 2)[::-1],
        'status': '&status=%5B%27Sites%27,%20%27Already%20Sold%27,%20%27Featured%20Items%27,%20%27Make%27%5D',
    }
    return render(request, 'product/index.html', context=context)


def lots_by_search(request):
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
    else:
        sort = dict(sort_by='year', sort_type='desc')

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
            lots = lots.filter(sold_price=0).filter(~Q(buy_today_bid=0))
        elif 'Pure Sale Items' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(~Q(bid_status='PURE SALE'))
        elif 'New Items' == featured_filter.name:
            cur_date = datetime.datetime.now().date()
            from_date = cur_date - datetime.timedelta(days=cur_date.weekday() + 7)
            to_date = from_date + datetime.timedelta(days=6)
            lots = lots.filter(sold_price=0).filter(created_at__range=(from_date, to_date))
        elif 'Lots with Bids' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(~Q(current_bid=0))
        elif 'No Bids Yet' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(current_bid=0)
        elif 'Hybrid Vehicles' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(fuel="HYBRID ENGINE")
        elif 'Repossessions' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(lot_highlights__contains='B')
        elif 'Donations' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(lot_highlights__contains='D').filter(
                ~Q(lot_highlights="Did Not Test Start"))
        elif 'Featured Vehicles' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(lot_highlights__contains='F')
        elif 'Offsite Sales' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(lot_highlights__contains='O')
        elif 'Run and Drive' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(lot_highlights__contains='R')
        elif 'Clean Title' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(~Q(doc_type_td__icontains='salvage'))
        elif 'Salvage Title' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(doc_type_td__icontains='salvage')
        elif 'Front End' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(
                Q(lot_1st_damage__icontains='Front End') or Q(lot_2nd_damage__icontains='Front End'))
        elif 'Hail Damage' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(
                Q(lot_1st_damage__icontains='Hail') or Q(lot_2nd_damage__icontains='Hail'))
        elif 'Normal Wear' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(
                Q(lot_1st_damage__icontains='Normal Wear') or Q(lot_2nd_damage__icontains='Normal Wear'))
        elif 'Minor Dents/Scratch' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(
                Q(lot_1st_damage__icontains='Minor') or Q(lot_2nd_damage__icontains='Minor'))
        elif 'Water/Flood' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(
                Q(lot_1st_damage__icontains='Water/Flood') or Q(lot_2nd_damage__icontains='Water/Flood'))
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
        lots = lots.filter(type=vehicle_type)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        lots = lots.filter(year__range=(from_year, to_year))
    if make:
        lots = lots.filter(make__icontains=make)
        filter_word.append(make)
        initial_status.append('make=' + make)
        filter_makes.append(make.upper())
    if model:
        lots = lots.filter(model=model)
        filter_word.append(model)
        initial_status.append('model=' + model)
        filter_models.append(model)
    if location:
        lots = lots.filter(location=location)
        filter_word.append(location)
        initial_status.append('location=' + location)
        filter_locations.append(location)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        filter_word.append('[' + str(from_year) + ' TO ' + str(to_year) + ']')
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
                    lots_ = lots_.filter(source=True)
                elif 'iaai' == param_value:
                    lots_ = lots_.filter(source=False)
            elif 'featured' == param_key and 'featured' != ignore:
                for feature_ in param_value:
                    if 'Buy It Now' == feature_:
                        lots_ = lots_.filter(~Q(buy_today_bid=0))
                    elif 'Run and Drive' == feature_:
                        lots_ = lots_.filter(lot_highlights__contains='R')
                    elif 'Pure Sale Items' == feature_:
                        lots_ = lots_.filter(~Q(bid_status='PURE SALE'))
                    elif 'New Items' == feature_:
                        c_date = datetime.datetime.now().date()
                        f_date = c_date - datetime.timedelta(days=c_date.weekday() + 7)
                        t_date = f_date + datetime.timedelta(days=6)
                        lots_ = lots_.filter(created_at__range=(f_date, t_date))
            # OR condition filters
            elif 'makes' == param_key and 'makes' != ignore:
                query = Q(make__icontains=param_value[0])
                for make_ in param_value[1:]:
                    query |= Q(make__icontains=make_)
                lots_ = lots_.filter(query)
            elif 'models' == param_key and 'models' != ignore:
                query = Q(model=param_value[0])
                for model_ in param_value[1:]:
                    query |= Q(model=model_)
                lots_ = lots_.filter(query)
            elif 'years' == param_key and 'years' != ignore:
                query = Q(year=param_value[0])
                for year_ in param_value[1:]:
                    query |= Q(year=year_)
                lots_ = lots_.filter(query)
            elif 'odometers' == param_key and 'odometers' != ignore:
                pass
            elif 'locations' == param_key and 'locations' != ignore:
                query = Q(location=param_value[0])
                for location_ in param_value[1:]:
                    query |= Q(location=location_)
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
                query = Q(engine_type=param_value[0])
                for engine_type_ in param_value[1:]:
                    query |= Q(engine_type=engine_type_)
                lots_ = lots_.filter(query)
            elif 'transmissions' == param_key and 'transmissions' != ignore:
                query = Q(transmission=param_value[0])
                for transmission_ in param_value[1:]:
                    query |= Q(transmission=transmission_)
                lots_ = lots_.filter(query)
            elif 'drive_trains' == param_key and 'drive_trains' != ignore:
                query = Q(drive=param_value[0])
                for drive_trains_ in param_value[1:]:
                    query |= Q(drive=drive_trains_)
                lots_ = lots_.filter(query)
            elif 'cylinderss' == param_key and 'cylinderss' != ignore:
                query = Q(cylinders=param_value[0])
                for cylinderss_ in param_value[1:]:
                    query |= Q(cylinders=cylinderss_)
                lots_ = lots_.filter(query)
            elif 'fuels' == param_key and 'fuels' != ignore:
                query = Q(fuel=param_value[0])
                for fuels_ in param_value[1:]:
                    query |= Q(fuel=fuels_)
                lots_ = lots_.filter(query)
            elif 'body_styles' == param_key and 'body_styles' != ignore:
                query = Q(body_style=param_value[0])
                for body_styles_ in param_value[1:]:
                    query |= Q(body_style=body_styles_)
                lots_ = lots_.filter(query)
            elif 'vehicle_types' == param_key and 'vehicle_types' != ignore:
                query = Q(type=param_value[0])
                for vehicle_types_ in param_value[1:]:
                    query |= Q(type=vehicle_types_)
                lots_ = lots_.filter(query)
            elif 'damages' == param_key and 'damages' != ignore:
                query = Q(lot_1st_damage=param_value[0])
                for damages_ in param_value[1:]:
                    query |= Q(lot_1st_damage=damages_)
                lots_ = lots_.filter(query)
            elif 'doctypes' == param_key and 'doctypes' != ignore:
                query = Q(doc_type_td__contains=str(param_value[0]).upper())
                for doctypes_ in param_value[1:]:
                    query |= Q(doc_type_td__contains=str(doctypes_).upper())
                lots_ = lots_.filter(query)

        return lots_

    ##########################

    # get filters count
    copart_count = lots.filter(source=True).count()
    iaai_count = lots.filter(source=False).count()
    sold_count = VehicleSold.objects.count()

    featured_lots = filter_by_filters(lots).order_by(sort_direction + sort['sort_by'])

    flfc21_count = featured_lots.filter(~Q(buy_today_bid=0)).count()
    flfc22_count = featured_lots.filter(lot_highlights__contains='R').count()
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
    count_makes = list(make_lots.values('make').annotate(count=Count('make')))

    model_lots = filter_by_filters(lots, 'models')
    count_models = list(model_lots.values('model').annotate(count=Count('model')))

    year_lots = filter_by_filters(lots, 'years')
    count_years = list(year_lots.values('year').annotate(count=Count('year'))[::-1])

    location_lots = filter_by_filters(lots, 'locations')
    count_locations = list(location_lots.values('location').annotate(count=Count('location')))

    sale_date_lots = filter_by_filters(lots, 'sale_dates').order_by('-sale_date')
    # count_sale_dates = list(
    #     sale_date_lots.annotate(sale_day=TruncDate('sale_date')).values('sale_day').annotate(count=Count('sale_day')))
    # count_sale_dates_for_tag = list(
    #     sale_date_lots.annotate(sale_day='sale_date').values('sale_day').annotate(count=Count('sale_day')))

    test = sale_date_lots.annotate(
            month=Cast(ExtractMonth('sale_date'), CharField()),
            day=Cast(ExtractDay('sale_date'), CharField()),
            year_test=Cast(ExtractYear('sale_date'), CharField()),
            sale_day=Concat('month', Value('/'), 'day', Value('/'), 'year_test')
        ).values('sale_day')

    res = test.values('sale_day').annotate(count=Count('sale_day'))
    # count_sale_dates = list(test.values('sale_day').annotate(count=Count('sale_day')))

    # print('test resullt ----> ', test.values('sale_day').distinct())

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
    print('res: ', count_sale_dates)

    count_sale_dates_for_tag = count_sale_dates.copy()

    for sid, s in enumerate(count_sale_dates):
        if s['sale_day'] is None or s['sale_day'] == "":
            del count_sale_dates[sid]
        else:
            if len(s['sale_day'].split('/')[0]) == 1:
                count_sale_dates[sid]['sale_day'] = "0" + count_sale_dates[sid]['sale_day']
            if len(s['sale_day'].split('/')[1]) == 1:
                count_sale_dates[sid]['sale_day'] = count_sale_dates[sid]['sale_day'][:3]\
                                                    + "0" + count_sale_dates[sid]['sale_day'][3:]

    engine_type_lots = filter_by_filters(lots, 'engine_types')
    count_engine_types = list(engine_type_lots.values('engine_type').annotate(count=Count('engine_type')))
    for sid, count_engine_type_ in enumerate(count_engine_types):
        if count_engine_type_['engine_type'] is None or count_engine_type_['engine_type'] == "":
            del count_engine_types[sid]

    transmission_lots = filter_by_filters(lots, 'transmissions')
    count_transmissions = list(transmission_lots.values('transmission').annotate(count=Count('transmission')))
    for sid, count_transmission_ in enumerate(count_transmissions):
        if count_transmission_['transmission'] is None or count_transmission_['transmission'] == "":
            del count_transmissions[sid]

    drive_train_lots = filter_by_filters(lots, 'drive_trains')
    count_drive_trains = list(drive_train_lots.values('drive').annotate(count=Count('drive')))
    for sid, count_drive_train_ in enumerate(count_drive_trains):
        if count_drive_train_['drive'] is None or count_drive_train_['drive'] == "":
            del count_drive_trains[sid]

    cylinders_lots = filter_by_filters(lots, 'cylinderss')
    count_cylinderss = list(cylinders_lots.values('cylinders').annotate(count=Count('cylinders')))
    for sid, count_cylinders_ in enumerate(count_cylinderss):
        if count_cylinders_['cylinders'] is None or count_cylinders_['cylinders'] == "":
            del count_cylinderss[sid]

    fuel_lots = filter_by_filters(lots, 'fuels')
    count_fuels = list(fuel_lots.values('fuel').annotate(count=Count('fuel')))
    for sid, count_fuel_ in enumerate(count_fuels):
        if count_fuel_['fuel'] is None or count_fuel_['fuel'] == "":
            del count_fuels[sid]

    body_style_lots = filter_by_filters(lots, 'body_styles')
    count_body_styles = list(body_style_lots.values('body_style').annotate(count=Count('body_style')))
    for sid, count_body_style_ in enumerate(count_body_styles):
        if count_body_style_['body_style'] is None or count_body_style_['body_style'] == "":
            del count_body_styles[sid]

    vehicle_type_lots = filter_by_filters(lots, 'vehicle_types')
    count_vehicle_types = list(vehicle_type_lots.values('type').annotate(count=Count('type')))
    for sid, count_vehicle_type_ in enumerate(count_vehicle_types):
        if count_vehicle_type_['type'] is None or count_vehicle_type_['type'] == "":
            del count_vehicle_types[sid]
        else:
            count_vehicle_types[sid]['type'] = dict(TYPES)[count_vehicle_type_['type']]

    damage_lots = filter_by_filters(lots, 'damages')
    count_damages = list(damage_lots.values('lot_1st_damage').annotate(count=Count('lot_1st_damage')))
    for sid, count_damage_ in enumerate(count_damages):
        if count_damage_['lot_1st_damage'] is None or count_damage_['lot_1st_damage'] == "":
            del count_damages[sid]

    doctype_lots = filter_by_filters(lots, 'doctypes')

    count_doctypes = []
    doctype_fields = ['Clean Title', 'Non-Repairable', 'Salvage Title']
    for doctype_field in doctype_fields:
        count_doctypes.append(
            {'doc_type_td': doctype_field,
             'count': doctype_lots.filter(doc_type_td__contains=str(doctype_field).upper()).count()})

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
    }

    print('filter_featured: ', filter_featured)
    print('url: ', params_)
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

    print('Sorting.....', sort_)
    if sort_:
        sort = eval(sort_)
    else:
        sort = dict(sort_by='year', sort_type='desc')
    print('Sort = ', sort)
    sort_direction = ''
    if 'desc' == sort['sort_type']:
        sort_direction = '-'
    print('Direction: ', sort_direction)

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
    if feature:
        featured_filter = Filter.objects.get(id=int(feature))
        filter_word.append(featured_filter.name)
        if 'Buy It Now' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(~Q(buy_today_bid=0))
        elif 'Pure Sale Items' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(~Q(bid_status='PURE SALE'))
        elif 'New Items' == featured_filter.name:
            cur_date = datetime.datetime.now().date()
            from_date = cur_date - datetime.timedelta(days=cur_date.weekday() + 7)
            to_date = from_date + datetime.timedelta(days=6)
            lots = lots.filter(sold_price=0).filter(created_at__range=(from_date, to_date))
        elif 'Lots with Bids' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(~Q(current_bid=0))
        elif 'No Bids Yet' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(current_bid=0)
        elif 'Hybrid Vehicles' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(fuel="HYBRID ENGINE")
        elif 'Repossessions' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(lot_highlights__contains='B')
        elif 'Donations' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(lot_highlights__contains='D').filter(
                ~Q(lot_highlights="Did Not Test Start"))
        elif 'Featured Vehicles' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(lot_highlights__contains='F')
        elif 'Offsite Sales' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(lot_highlights__contains='O')
        elif 'Run and Drive' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(lot_highlights__contains='R')
        elif 'Clean Title' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(~Q(doc_type_td__icontains='salvage'))
        elif 'Salvage Title' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(doc_type_td__icontains='salvage')
        elif 'Front End' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(
                Q(lot_1st_damage__icontains='Front End') or Q(lot_2nd_damage__icontains='Front End'))
        elif 'Hail Damage' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(
                Q(lot_1st_damage__icontains='Hail') or Q(lot_2nd_damage__icontains='Hail'))
        elif 'Normal Wear' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(
                Q(lot_1st_damage__icontains='Normal Wear') or Q(lot_2nd_damage__icontains='Normal Wear'))
        elif 'Minor Dents/Scratch' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(
                Q(lot_1st_damage__icontains='Minor') or Q(lot_2nd_damage__icontains='Minor'))
        elif 'Water/Flood' == featured_filter.name:
            lots = lots.filter(sold_price=0).filter(
                Q(lot_1st_damage__icontains='Water/Flood') or Q(lot_2nd_damage__icontains='Water/Flood'))
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
        lots = lots.filter(type=vehicle_type)
    if year:
        # extract from_year and to_year from year_range
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        lots = lots.filter(year__range=(from_year, to_year))
    if make:
        lots = lots.filter(make__icontains=make)
        filter_word.append(make)
        filter_makes.append(make.upper())
    if model:
        lots = lots.filter(model=model)
        filter_word.append(model)
        filter_models.append(model)
    if location:
        lots = lots.filter(location=location)
        filter_word.append(location)
        filter_locations.append(location)
    if year:
        year_range = year.replace('%2C', ',')[1:-1].split(',')
        from_year = year_range[0]
        to_year = year_range[1]
        filter_word.append('[' + str(from_year) + ' TO ' + str(to_year) + ']')
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
                    lots_ = lots_.filter(source=True)
                elif 'iaai' == param_value:
                    lots_ = lots_.filter(source=False)
            elif 'featured' == param_key and 'featured' != ignore:
                for feature in param_value:
                    if 'Buy It Now' == feature:
                        lots_ = lots_.filter(~Q(buy_today_bid=0))
                    elif 'Run and Drive' == feature:
                        lots_ = lots_.filter(lot_highlights__contains='R')
                    elif 'Pure Sale Items' == feature:
                        lots_ = lots_.filter(~Q(bid_status='PURE SALE'))
                    elif 'New Items' == feature:
                        c_date = datetime.datetime.now().date()
                        f_date = c_date - datetime.timedelta(days=c_date.weekday() + 7)
                        t_date = f_date + datetime.timedelta(days=6)
                        lots_ = lots_.filter(created_at__range=(f_date, t_date))
            # OR condition filters
            elif 'makes' == param_key and 'makes' != ignore:
                query = Q(make__icontains=param_value[0])
                for make_ in param_value[1:]:
                    query |= Q(make__icontains=make_)
                lots_ = lots_.filter(query)
            elif 'models' == param_key and 'models' != ignore:
                query = Q(model=param_value[0])
                for model_ in param_value[1:]:
                    query |= Q(model=model_)
                lots_ = lots_.filter(query)
            elif 'years' == param_key and 'years' != ignore:
                query = Q(year=param_value[0])
                for year in param_value[1:]:
                    query |= Q(year=year)
                lots_ = lots_.filter(query)
            elif 'odometers' == param_key and 'odometers' != ignore:
                pass
            elif 'locations' == param_key and 'locations' != ignore:
                query = Q(location=param_value[0])
                for location_ in param_value[1:]:
                    query |= Q(location=location_)
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
                query = Q(engine_type=param_value[0])
                for engine_type_ in param_value[1:]:
                    query |= Q(engine_type=engine_type_)
                lots_ = lots_.filter(query)
            elif 'transmissions' == param_key and 'transmissions' != ignore:
                query = Q(transmission=param_value[0])
                for transmission_ in param_value[1:]:
                    query |= Q(transmission=transmission_)
                lots_ = lots_.filter(query)
            elif 'drive_trains' == param_key and 'drive_trains' != ignore:
                query = Q(drive=param_value[0])
                for drive_trains_ in param_value[1:]:
                    query |= Q(drive=drive_trains_)
                lots_ = lots_.filter(query)
            elif 'cylinderss' == param_key and 'cylinderss' != ignore:
                query = Q(cylinders=param_value[0])
                for cylinderss_ in param_value[1:]:
                    query |= Q(cylinders=cylinderss_)
                lots_ = lots_.filter(query)
            elif 'fuels' == param_key and 'fuels' != ignore:
                query = Q(fuel=param_value[0])
                for fuels_ in param_value[1:]:
                    query |= Q(fuel=fuels_)
                lots_ = lots_.filter(query)
            elif 'body_styles' == param_key and 'body_styles' != ignore:
                query = Q(body_style=param_value[0])
                for body_styles_ in param_value[1:]:
                    query |= Q(body_style=body_styles_)
                lots_ = lots_.filter(query)
            elif 'vehicle_types' == param_key and 'vehicle_types' != ignore:
                query = Q(type=param_value[0])
                for vehicle_types_ in param_value[1:]:
                    query |= Q(type=vehicle_types_)
                lots_ = lots_.filter(query)
            elif 'damages' == param_key and 'damages' != ignore:
                query = Q(lot_1st_damage=param_value[0])
                for damages_ in param_value[1:]:
                    query |= Q(lot_1st_damage=damages_)
                lots_ = lots_.filter(query)
            elif 'doctypes' == param_key and 'doctypes' != ignore:
                query = Q(doc_type_td__contains=str(param_value[0]).upper())
                for doctypes_ in param_value[1:]:
                    query |= Q(doc_type_td__contains=str(doctypes_).upper())
                lots_ = lots_.filter(query)
        return lots_
        #########################################

    # get filters count
    copart_count = lots.filter(source=True).count()
    iaai_count = lots.filter(source=False).count()
    sold_count = VehicleSold.objects.count()

    # featured_lots = filter_by_filters(lots).order_by(sort_direction + sort['sort_by'])
    featured_lots = filter_by_filters(lots)
    print("Odering ...........",  sort_direction + sort['sort_by'])
    flfc21_count = featured_lots.filter(~Q(buy_today_bid=0)).count()
    flfc22_count = featured_lots.filter(lot_highlights__contains='R').count()
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
    count_makes = list(make_lots.values('make').annotate(count=Count('make')))

    model_lots = filter_by_filters(lots, 'models')
    count_models = list(model_lots.values('model').annotate(count=Count('model')))

    year_lots = filter_by_filters(lots, 'years')
    count_years = list(year_lots.values('year').annotate(count=Count('year'))[::-1])

    odometer_lots = filter_by_filters(lots, 'odometers')
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
    ]

    ############################
    location_lots = filter_by_filters(lots, 'locations')
    count_locations = list(location_lots.values('location').annotate(count=Count('location')))

    sale_date_lots = filter_by_filters(lots, 'sale_dates').order_by('-sale_date')
    test = sale_date_lots.annotate(
        month=Cast(ExtractMonth('sale_date'), CharField()),
        day=Cast(ExtractDay('sale_date'), CharField()),
        year_test=Cast(ExtractYear('sale_date'), CharField()),
        sale_day=Concat('month', Value('/'), 'day', Value('/'), 'year_test')
    ).values('sale_day')

    res = test.values('sale_day').annotate(count=Count('sale_day'))
    # count_sale_dates = list(test.values('sale_day').annotate(count=Count('sale_day')))

    # print('test resullt ----> ', test.values('sale_day').distinct())

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
    print('res: ', count_sale_dates)

    count_sale_dates_for_tag = count_sale_dates.copy()

    engine_type_lots = filter_by_filters(lots, 'engine_types')
    count_engine_types = list(engine_type_lots.values('engine_type').annotate(count=Count('engine_type')))
    for sid, count_engine_type_ in enumerate(count_engine_types):
        if count_engine_type_['engine_type'] is None or count_engine_type_['engine_type'] == "":
            del count_engine_types[sid]

    transmission_lots = filter_by_filters(lots, 'transmissions')
    count_transmissions = list(transmission_lots.values('transmission').annotate(count=Count('transmission')))
    for sid, count_transmission_ in enumerate(count_transmissions):
        if count_transmission_['transmission'] is None or count_transmission_['transmission'] == "":
            del count_transmissions[sid]

    drive_train_lots = filter_by_filters(lots, 'drive_trains')
    count_drive_trains = list(drive_train_lots.values('drive').annotate(count=Count('drive')))
    for sid, count_drive_train_ in enumerate(count_drive_trains):
        if count_drive_train_['drive'] is None or count_drive_train_['drive'] == "":
            del count_drive_trains[sid]

    cylinders_lots = filter_by_filters(lots, 'cylinderss')
    count_cylinderss = list(cylinders_lots.values('cylinders').annotate(count=Count('cylinders')))
    for sid, count_cylinders_ in enumerate(count_cylinderss):
        if count_cylinders_['cylinders'] is None or count_cylinders_['cylinders'] == "":
            del count_cylinderss[sid]

    fuel_lots = filter_by_filters(lots, 'fuels')
    count_fuels = list(fuel_lots.values('fuel').annotate(count=Count('fuel')))
    for sid, count_fuel_ in enumerate(count_fuels):
        if count_fuel_['fuel'] is None or count_fuel_['fuel'] == "":
            del count_fuels[sid]

    body_style_lots = filter_by_filters(lots, 'body_styles')
    count_body_styles = list(body_style_lots.values('body_style').annotate(count=Count('body_style')))
    for sid, count_body_style_ in enumerate(count_body_styles):
        if count_body_style_['body_style'] is None or count_body_style_['body_style'] == "":
            del count_body_styles[sid]

    vehicle_type_lots = filter_by_filters(lots, 'vehicle_types')
    count_vehicle_types = list(vehicle_type_lots.values('type').annotate(count=Count('type')))
    for sid, count_vehicle_type_ in enumerate(count_vehicle_types):
        if count_vehicle_type_['type'] is None or count_vehicle_type_['type'] == "":
            del count_vehicle_types[sid]
        else:
            count_vehicle_types[sid]['type'] = dict(TYPES)[count_vehicle_type_['type']]

    damage_lots = filter_by_filters(lots, 'damages')
    count_damages = list(damage_lots.values('lot_1st_damage').annotate(count=Count('lot_1st_damage')))
    for sid, count_damage_ in enumerate(count_damages):
        if count_damage_['lot_1st_damage'] is None or count_damage_['lot_1st_damage'] == "":
            del count_damages[sid]

    doctype_lots = filter_by_filters(lots, 'doctypes')

    count_doctypes = []
    doctype_fields = ['Clean Title', 'Non-Repairable', 'Salvage Title']
    for doctype_field in doctype_fields:
        count_doctypes.append(
            {'doc_type_td': doctype_field,
             'count': doctype_lots.filter(doc_type_td__contains=str(doctype_field).upper()).count()})

    #################################

    # lots = filter_by_filters(lots).order_by('-year')
    lots = filter_by_filters(lots).order_by(sort_direction + sort['sort_by'])
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

    result_lots = []
    for a in paged_lots:
        a = a.__dict__
        del a['_state']
        result_lots.append(a)
    context = {
        'lots': result_lots,
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
        "cylinders": count_cylinderss,
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
    }
    print('filter_featured: ', filter_featured)
    return render(request, 'product/content.html', context=context)


def detail(request, lot):
    lot = Vehicle.objects.get(lot=int(lot))
    is_similar = True

    similar = Vehicle.objects.filter(make=lot.make).filter(model=lot.model).filter(year=lot.year).filter(
        ~Q(lot=int(lot.lot))).order_by('-id')
    if len(similar) >= 12:
        similar = similar[:12]
    else:
        similar = Vehicle.objects.filter(make=lot.make).filter(model=lot.model).filter(~Q(lot=int(lot.lot))).order_by(
            '-id')
        if len(similar) >= 12:
            similar = similar[:12]
        else:
            similar = Vehicle.objects.filter(~Q(retail_value=0)).filter(~Q(lot=int(lot.lot))).order_by('-id')[:12]
            is_similar = False

    context = {'lot': lot, 'similar': similar, 'is_similar': is_similar}
    return render(request, 'product/detail.html', context=context)
