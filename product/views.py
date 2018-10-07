import datetime

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import translation
from django.db.models import Q

from product.tasks import scrap_copart_all, scrap_copart_lots, scrap_iaai_lots, scrap_live_auctions, scrap_type_lots, scrap_make_lots
from product.models import Vehicle, TypesLots, MakesLots


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


def index(request):
    new_arrivals = Vehicle.objects.all().order_by('-id')[:12]
    vehicle_types = TypesLots.objects.all()
    vehicle_makes = MakesLots.objects.all()

    context = {
        'arrivals': new_arrivals,
        'vehicle_types': vehicle_types,
        'vehicle_makes': vehicle_makes,
        'year_range': range(1920, datetime.datetime.now().year + 1)[::-1]
    }
    return render(request, 'product/index.html', context=context)


def lot_list(request):
    from_year = request.GET.get('from_year', '')
    to_year = request.GET.get('to_year', '')

    context = {}

    lots = Vehicle.objects.all()
    if from_year:
        lots = lots.filter(year__gte=int(from_year))
        context['from_year'] = from_year
    if to_year:
        lots = lots.filter(year__lte=int(to_year))
        context['to_year'] = to_year

    context['lots'] = lots[:50]

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
