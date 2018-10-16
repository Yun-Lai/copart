from django import template

register = template.Library()


@register.filter
def get_by_index(l, i):
    return l[i]


@register.filter
def get_lot_image(lot, index):
    try:
        if lot.source:
            return 'https://cs.copart.com/v1/AUTH_svc.pdoc00001/' + lot.images.split('|')[index]
        else:
            return 'https://vis.iaai.com:443/resizer?imageKeys=%s&width=640&height=480' % lot.images.split('|')[index]
    except:
        return ""


@register.filter
def get_lot_image4(lot, index):
    try:
        if lot.source:
            return 'https://cs.copart.com/v1/AUTH_svc.pdoc00001/' + lot.images.split('|')[index + 4]
        else:
            return 'https://vis.iaai.com:443/resizer?imageKeys=%s&width=640&height=480' % lot.images.split('|')[index + 4]
    except:
        return ""


@register.filter
def get_lot_image8(lot, index):
    try:
        if lot.source:
            return 'https://cs.copart.com/v1/AUTH_svc.pdoc00001/' + lot.images.split('|')[index + 8]
        else:
            return 'https://vis.iaai.com:443/resizer?imageKeys=%s&width=640&height=480' % lot.images.split('|')[index + 8]
    except:
        return ""


@register.filter
def get_type_description(vehicle_type):
    types = (
        ('A', 'ATV'),
        ('V', 'Automobile'),
        ('M', 'Boat'),
        ('D', 'Dirt Bike'),
        ('U', 'Heavy Duty Trucks'),
        ('E', 'Industrial Equipment'),
        ('J', 'Jet Ski'),
        ('K', 'Medium Duty/Box Trucks'),
        ('C', 'Motorcycle'),
        ('H', 'Other Goods'),
        ('R', 'Recreational Vehicle (RV)'),
        ('S', 'Snowmobile'),
        ('L', 'Trailers'),
    )
    return dict(types)[vehicle_type]


@register.filter
def is_icon(highlights):
    if highlights.isupper() and highlights.isalpha():
        return True
    return False


@register.filter
def get_highlights(highlights):
    icons = (
        ('R', 'Run & Drive'),
        ('C', 'Seller Certified'),
        ('E', 'Enhanced Vehicle'),
        ('C', 'CrashedToys'),
        ('S', 'Engine Start Program'),
        ('F', 'Featured Vehicle'),
        ('O', 'Offsite Sales'),
        ('D', 'Donated Vehicle'),
        ('Q', 'Carb Qualification'),
        ('B', 'Sealed Bid Repossession'),
        ('V', 'VIX'),
        ('F', 'FAST'),
        ('H', 'Hybrid Vehicles'),
        # ('A', 'www.driveautoauctions.com'),
    )
    return dict(icons)[highlights]
