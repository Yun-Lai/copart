from django import template

register = template.Library()


@register.filter
def get_by_index(l, i):
    return l[i]


@register.filter
def get_lot_image(lot, index):
    if lot.source:
        return 'https://cs.copart.com/v1/AUTH_svc.pdoc00001/' + lot.images.split('|')[index]
    else:
        return 'https://vis.iaai.com:443/resizer?imageKeys=%s&width=640&height=480' + lot.images.split('|')[index]


@register.filter
def get_lot_image4(lot, index):
    if lot.source:
        return 'https://cs.copart.com/v1/AUTH_svc.pdoc00001/' + lot.images.split('|')[index + 4]
    else:
        return 'https://vis.iaai.com:443/resizer?imageKeys=%s&width=640&height=480' + lot.images.split('|')[index + 4]


@register.filter
def get_lot_image8(lot, index):
    if lot.source:
        return 'https://cs.copart.com/v1/AUTH_svc.pdoc00001/' + lot.images.split('|')[index + 8]
    else:
        return 'https://vis.iaai.com:443/resizer?imageKeys=%s&width=640&height=480' + lot.images.split('|')[index + 8]


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
