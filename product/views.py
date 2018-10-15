import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import translation
from django.db.models import Q

from product.tasks import scrap_copart_all, scrap_copart_lots, scrap_iaai_lots, scrap_live_auctions,\
    scrap_type_lots, scrap_make_lots
from product.models import Vehicle, VehicleMakes, TypesLots, MakesLots, TYPES


# def switch_language(request, language):
#     translation.activate(language)
#     request.session[translation.LANGUAGE_SESSION_KEY] = language
#     return redirect('/admin/')


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


def view_scrap_type_lot(request):
    scrap_type_lots.delay()

    return redirect('/admin/')


def view_scrap_make_lot(request):
    scrap_make_lots.delay()

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
    vehicle_types = TypesLots.objects.all()
    vehicle_makes = MakesLots.objects.all().order_by('-lots')[:55]

    context = {
        'arrivals': new_arrivals,
        'vehicle_types': vehicle_types,
        'vehicle_makes': vehicle_makes,
        'year_range': range(1920, datetime.datetime.now().year + 2)[::-1]
    }
    return render(request, 'product/index.html', context=context)


def lot_list(request):
    types = request.GET.get('type', '')
    from_year = int(request.GET.get('from_year', ''))
    to_year = int(request.GET.get('to_year', ''))
    make = request.GET.get('make', '')
    model = request.GET.get('model', '')

    filter_word = dict(TYPES)[types]

    lots = Vehicle.objects.filter(type=types).filter(year__range=(from_year, to_year))
    if make:
        lots = lots.filter(make=make)
        filter_word += ', ' + make
    if model:
        lots = lots.filter(model=model)
        filter_word += ', ' + model
    filter_word += ', ' + '[' + str(from_year) + ' TO ' + str(to_year) + ']'

    page = int(request.GET.get('page', 1))
    entry = int(request.GET.get('entry', 20))

    paginator = Paginator(lots, entry)
    try:
        paged_lots = paginator.page(page)
    except PageNotAnInteger:
        paged_lots = paginator.page(1)
    except EmptyPage:
        paged_lots = paginator.page(paginator.num_pages)

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
        'filter_word': filter_word,
    }

    return render(request, 'product/list.html', context=context)


def lots_by_type(request, vehicle_type):
    page = int(request.GET.get('page', 1))
    entry = int(request.GET.get('entry', 20))

    lots = Vehicle.objects.filter(type=vehicle_type)
    paginator = Paginator(lots, entry)

    type_lot = TypesLots.objects.get(type=vehicle_type)
    type_lot.lots = paginator.count
    type_lot.save()

    try:
        paged_lots = paginator.page(page)
    except PageNotAnInteger:
        paged_lots = paginator.page(1)
    except EmptyPage:
        paged_lots = paginator.page(paginator.num_pages)

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

    make_lot = MakesLots.objects.get(id=int(vehicle_make))
    lots = Vehicle.objects.filter(make__icontains=make_lot.make)

    paginator = Paginator(lots, entry)
    make_lot.lots = paginator.count
    make_lot.save()
    try:
        paged_lots = paginator.page(page)
    except PageNotAnInteger:
        paged_lots = paginator.page(1)
    except EmptyPage:
        paged_lots = paginator.page(paginator.num_pages)

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
        'filter_word': make_lot.make,
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
