import datetime
from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import translation
from django.db.models import Q, Count

from product.tasks import scrap_copart_all, scrap_copart_lots, scrap_iaai_lots, scrap_live_auctions, scrap_filters_count
from product.models import Vehicle, VehicleSold, VehicleMakes, Filter, Location, TYPES


# def switch_language(request, language):
#     translation.activate(language)
#     request.session[translation.LANGUAGE_SESSION_KEY] = language
#     return redirect('/admin/')

def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name, args=args)
    params = urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


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


def ajax_getimages(request):
    lot_id = request.POST.get('lot', '')

    if not lot_id:
        return JsonResponse({'result': False})

    lot = Vehicle.objects.get(lot=int(lot_id))
    if lot.source:
        images = ['https://cs.copart.com/v1/AUTH_svc.pdoc00001/' + a for a in lot.images.split('|')]
        thumb_images = ['https://cs.copart.com/v1/AUTH_svc.pdoc00001/' + a for a in lot.thumb_images.split('|')]
    else:
        images = ['https://vis.iaai.com:443/resizer?imageKeys=%s&width=640&height=480' % a for a in lot.images.split('|')]
        thumb_images = ['https://vis.iaai.com:443/resizer?imageKeys=%s&width=128&height=96' % a for a in lot.images.split('|')]

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
    vehicle_makes = Vehicle.objects.filter(type=finder_type).filter(make__icontains=finder_make).values_list('model', flat=True)
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
        'year_range': range(1920, datetime.datetime.now().year + 2)[::-1]
    }
    return render(request, 'product/index.html', context=context)


def lots_by_search(request, vehicle_type, from_year, to_year, make, model, location):
    filter_word = dict(TYPES)[vehicle_type]

    lots = Vehicle.objects.filter(type=vehicle_type).filter(year__range=(from_year, to_year))
    sold_lots = VehicleSold.objects.filter(type=vehicle_type).filter(year__range=(from_year, to_year))
    if '_' != make:
        lots = lots.filter(make__icontains=make)
        sold_lots = sold_lots.filter(make__icontains=make)
        filter_word += ', ' + make
    if '_' != model:
        lots = lots.filter(model__icontains=model)
        sold_lots = sold_lots.filter(model__icontains=model)
        filter_word += ', ' + model
    if '_' != location:
        lots = lots.filter(location=location)
        sold_lots = sold_lots.filter(location=location)
        filter_word += ', ' + location
    filter_word += ', ' + '[' + str(from_year) + ' TO ' + str(to_year) + ']'

    page = int(request.GET.get('page', 1))
    entry = int(request.GET.get('entry', 20))

    paginator = Paginator(lots, entry)
    if page > paginator.num_pages:
        return custom_redirect('list_page_by_search', vehicle_type, from_year, to_year, make, model, location,
                               page=paginator.num_pages, entry=entry)
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

    # Filters
    copart_count = lots.filter(source=True).count()
    iaai_count = paginator.count - copart_count
    sold_count = sold_lots.count()

    flfc21_count = lots.filter(~Q(buy_today_bid=0)).count()
    flfc22_count = lots.filter(lot_highlights__contains='R').count()
    flfc23_count = 0
    flfc24_count = lots.filter(~Q(bid_status='PURE SALE')).count()
    flfc25_count = 0
    flfc26_count = 0
    flfc27_count = 0
    flfc28_count = 0
    flfc29_count = 0
    cur_date = datetime.datetime.now().date()
    from_date = cur_date - datetime.timedelta(days=cur_date.weekday() + 7)
    to_date = from_date + datetime.timedelta(days=6)
    flfc30_count = lots.filter(created_at__range=(from_date, to_date)).count()

    makes = lots.values('make').annotate(count=Count('make'))
    models = lots.values('model').annotate(count=Count('model'))
    years = lots.values('year').annotate(count=Count('year'))[::-1]
    odometers = lots.raw(
        'SELECT ROW_NUMBER() OVER (ORDER BY 1) AS id,'
        'SUM(CASE WHEN odometer_orr < 25000 THEN 1 ELSE 0 END) AS count_0,'
        'SUM(CASE WHEN odometer_orr >= 25000 AND odometer_orr <= 50000 THEN 1 ELSE 0 END) AS count_1,'
        'SUM(CASE WHEN odometer_orr > 50000 AND odometer_orr <= 75000 THEN 1 ELSE 0 END) AS count_2,'
        'SUM(CASE WHEN odometer_orr > 75000 AND odometer_orr <= 100000 THEN 1 ELSE 0 END) AS count_3,'
        'SUM(CASE WHEN odometer_orr > 100000 AND odometer_orr <= 150000 THEN 1 ELSE 0 END) AS count_4,'
        'SUM(CASE WHEN odometer_orr > 150000 AND odometer_orr <= 200000 THEN 1 ELSE 0 END) AS count_5,'
        'SUM(CASE WHEN odometer_orr > 200000 THEN 1 ELSE 0 END) AS count_6 '
        'FROM product_vehicle')
    odometers = [
        {'odometer': '< 25,000', 'count': odometers[0].count_0},
        {'odometer': '25,000 to 50,000', 'count': odometers[0].count_1},
        {'odometer': '50,001 to 75,000', 'count': odometers[0].count_2},
        {'odometer': '75,001 to 100,000', 'count': odometers[0].count_3},
        {'odometer': '100,001 to 150,000', 'count': odometers[0].count_4},
        {'odometer': '150,001 to 200,000', 'count': odometers[0].count_5},
        {'odometer': '> 200,000', 'count': odometers[0].count_6},
    ]
    locations = lots.values('location').annotate(count=Count('location'))

    context = {
        'lots': paged_lots,
        'total_lots': paginator.count,
        'pages': pages[::-1],
        'current_page': str(page),
        'current_entry': entry,
        'page_start_index': (page - 1) * entry + 1,
        'page_end_index': page * entry if page != paginator.num_pages else paginator.count,
        'filter_word': filter_word,

        'copart_count': copart_count,
        'iaai_count': iaai_count,
        'sold_count': sold_count,

        'flfc21_count': flfc21_count,
        'flfc22_count': flfc22_count,
        'flfc23_count': flfc23_count,
        'flfc24_count': flfc24_count,
        'flfc25_count': flfc25_count,
        'flfc26_count': flfc26_count,
        'flfc27_count': flfc27_count,
        'flfc28_count': flfc28_count,
        'flfc29_count': flfc29_count,
        'flfc30_count': flfc30_count,

        'makes': makes,
        'models': models,
        'years': years,
        'odometers': odometers,
        'locations': locations,
    }

    return render(request, 'product/list.html', context=context)


def lots_by_feature(request, feature):
    page = int(request.GET.get('page', 1))
    entry = int(request.GET.get('entry', 20))

    featured_filter = Filter.objects.get(id=int(feature))

    if 'Buy It Now' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(~Q(buy_today_bid=0))
    elif 'Pure Sale Items' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(~Q(bid_status='PURE SALE'))
    elif 'New Items' == featured_filter.name:
        cur_date = datetime.datetime.now().date()
        from_date = cur_date - datetime.timedelta(days=cur_date.weekday() + 7)
        to_date = from_date + datetime.timedelta(days=6)
        lots = Vehicle.objects.filter(sold_price=0).filter(created_at__range=(from_date, to_date))
    elif 'Lots with Bids' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(~Q(current_bid=0))
    elif 'No Bids Yet' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(current_bid=0)
    elif 'Hybrid Vehicles' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(fuel="HYBRID ENGINE")
    elif 'Repossessions' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(lot_highlights__contains='B')
    elif 'Donations' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(lot_highlights__contains='D').filter(
            ~Q(lot_highlights="Did Not Test Start"))
    elif 'Featured Vehicles' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(lot_highlights__contains='F')
    elif 'Offsite Sales' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(lot_highlights__contains='O')
    elif 'Run and Drive' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(lot_highlights__contains='R')
    elif 'Clean Title' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(~Q(doc_type_td__icontains='salvage'))
    elif 'Salvage Title' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(doc_type_td__icontains='salvage')
    elif 'Front End' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(
            Q(lot_1st_damage__icontains='Front End') or Q(lot_2nd_damage__icontains='Front End'))
    elif 'Hail Damage' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(
            Q(lot_1st_damage__icontains='Hail') or Q(lot_2nd_damage__icontains='Hail'))
    elif 'Normal Wear' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(
            Q(lot_1st_damage__icontains='Normal Wear') or Q(lot_2nd_damage__icontains='Normal Wear'))
    elif 'Minor Dents/Scratch' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(
            Q(lot_1st_damage__icontains='Minor') or Q(lot_2nd_damage__icontains='Minor'))
    elif 'Water/Flood' == featured_filter.name:
        lots = Vehicle.objects.filter(sold_price=0).filter(
            Q(lot_1st_damage__icontains='Water/Flood') or Q(lot_2nd_damage__icontains='Water/Flood'))
    else:
        lots = Vehicle.objects.all()

    paginator = Paginator(lots, entry)
    featured_filter.count = paginator.count
    featured_filter.save()

    if page > paginator.num_pages:
        return custom_redirect('list_page_by_feature', feature, page=paginator.num_pages, entry=entry)
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
        'filter_word': featured_filter.name,
    }

    return render(request, 'product/list.html', context=context)


def lots_by_type(request, vehicle_type):
    page = int(request.GET.get('page', 1))
    entry = int(request.GET.get('entry', 20))

    lots = Vehicle.objects.filter(type=vehicle_type)
    paginator = Paginator(lots, entry)

    type_filter = Filter.objects.get(name=vehicle_type, type='T')
    type_filter.count = paginator.count
    type_filter.save()

    if page > paginator.num_pages:
        return custom_redirect('list_page_by_type', vehicle_type, page=paginator.num_pages, entry=entry)
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
        'filter_word': dict(TYPES)[vehicle_type],
    }

    return render(request, 'product/list.html', context=context)


def lots_by_make(request, vehicle_make):
    page = int(request.GET.get('page', 1))
    entry = int(request.GET.get('entry', 20))

    make_filter = Filter.objects.get(id=int(vehicle_make))
    lots = Vehicle.objects.filter(make__icontains=make_filter.name)

    paginator = Paginator(lots, entry)
    make_filter.count = paginator.count
    make_filter.save()

    if page > paginator.num_pages:
        return custom_redirect('list_page_by_make', vehicle_make, page=paginator.num_pages, entry=entry)
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
        'filter_word': make_filter.name,
    }

    return render(request, 'product/list.html', context=context)


def detail(request, lot):
    lot = Vehicle.objects.get(lot=int(lot))

    similar = Vehicle.objects.filter(make=lot.make).filter(model=lot.model).filter(year=lot.year).filter(~Q(lot=int(lot.lot))).order_by('-id')
    if len(similar) >= 4:
        similar = similar[:4]
    else:
        similar = Vehicle.objects.filter(make=lot.make).filter(model=lot.model).filter(~Q(lot=int(lot.lot))).order_by('-id')
        if len(similar) >= 4:
            similar = similar[:4]
        else:
            similar = Vehicle.objects.filter(make=lot.make).filter(~Q(lot=int(lot.lot))).order_by('-id')
            if len(similar) >= 4:
                similar = similar[:4]
            else:
                similar = Vehicle.objects.filter(~Q(lot=int(lot.lot))).order_by('-id')[:4]

    context = {'lot': lot, 'similar': similar}
    return render(request, 'product/detail.html', context=context)
