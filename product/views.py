from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import translation

from product.tasks import scrap_copart_lots, scrap_iaai_lots, scrap_live_auctions
from product.tasks import scrap_copart as scrap_copart_lot
from product.models import Vehicle, VehicleMakes


def switch_language(request, language):
    translation.activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language
    return redirect('/')


def scrap_copart(request):
    vtype = request.GET.get('type')
    description = request.GET.get('description')
    code = request.GET.get('code')

    make = VehicleMakes.objects.get(type=vtype, code=code, description=description)

    scrap_copart_lots.delay(make.id, make.id + 1)

    return redirect('/product/vehiclemakes/')


def scrap_coparts(request):
    scrap_copart_lot.delay()

    return redirect('/')


def scrap_iaai(request):
    scrap_iaai_lots.delay()

    return redirect('/')


def scrap_auction(request):
    scrap_live_auctions.delay()

    return redirect('/')


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
