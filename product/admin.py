from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.utils.encoding import smart_text
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from product.models import *


class MultipleChangeList(ChangeList):
    def get_query_string(self, new_params=None, remove=None):
        if new_params is None: new_params = {}
        if remove is None: remove = []
        p = self.params.copy()
        for r in remove:
            for k in list(p):
                if k.startswith(r):
                    del p[k]
        for k, v in new_params.items():
            if v is None:
                if k in p:
                    del p[k]
            else:
                if k in p and '__in' in k:
                    in_list = p[k].split(',')
                    if not v in in_list:
                        in_list.append(v)
                    else:
                        in_list.remove(v)
                    p[k] = ','.join(in_list)
                else:
                    p[k] = v
        return '?%s' % urlencode(sorted(p.items()))


class MultipleChoicesFieldListFilter(admin.ChoicesFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super(MultipleChoicesFieldListFilter, self).__init__(field, request, params, model, model_admin, field_path)
        self.lookup_kwarg = '%s__in' % field_path
        self.lookup_val = request.GET.get(self.lookup_kwarg)

    def choices(self, cl):
        yield {
            'selected': self.lookup_val is None,
            'query_string': cl.get_query_string({}, [self.lookup_kwarg]),
            'display': _('All')
        }
        for lookup, title in self.field.flatchoices:
            yield {
                'selected': smart_text(lookup) in str(self.lookup_val),
                'query_string': cl.get_query_string({self.lookup_kwarg: lookup}),
                'display': title,
            }


class DescriptionFilter(admin.SimpleListFilter):
    title = 'Description'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'description'

    def lookups(self, request, model_admin):
        descriptions = []
        if 'type__in' in request.GET:
            makes = VehicleMakes.objects.filter(type__in=request.GET['type__in'])
        else:
            makes = VehicleMakes.objects.all()

        for make in makes:
            descriptions.append((make.id, dict(TYPES)[make.type] + '-' + make.description))
        return descriptions

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        return queryset.filter(id=self.value())


class VehicleMakesAdmin(admin.ModelAdmin):
    list_display = ['type', 'description', 'count', 'scrap_link']
    list_filter = (DescriptionFilter, ('type', MultipleChoicesFieldListFilter))
    search_fields = ['description']

    def get_changelist(self, request, **kwargs):
        return MultipleChangeList


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['avatar_img', 'vin', 'lot', 'year', 'make', 'model', 'color', 'item', 'location', 'lane_row',
                    'sale_date', 'odometer', 'doc_type', 'lot_1st_damage', 'est_retail_value', 'current_bid_', 'sold_price_']

    list_display_links = ['vin', 'lot']

    list_filter = ['make', 'source']

    search_fields = ['name', 'vin', 'lot', 'year', 'make', 'model']

    fieldsets = [
        ('', {'fields': ['vin', 'lot', 'name', 'make', 'model', 'year', 'location']}),
        ('Lot', {'fields': ['doc_type_ts', 'doc_type_stt', 'doc_type_td', 'odometer_orr', 'odometer_ord',
                            'lot_highlights', 'lot_seller', 'lot_1st_damage', 'lot_2nd_damage', 'retail_value']}),
        ('Features', {'fields': ['body_style', 'color', 'engine_type', 'cylinders', 'transmission',
                                 'drive', 'fuel', 'keys', 'notes']}),
        ('Bid Information', {'fields': ['bid_status', 'sale_status', 'current_bid', 'buy_today_bid', 'sold_price', 'currency']}),
        ('Sale Information', {'fields': ['location', 'lane', 'item', 'grid', 'sale_date', 'last_updated']}),
        ('Images', {'fields': ['avatar', 'images', 'thumb_images']}),
        ('Foregoing', {'fields': ['foregoing', 'show', 'source']}),
    ]

    change_list_template = 'admin/change_list_vehicle.html'

    class Media:
        css = {'all': ('product/css/vehicle.css', 'node_modules/font-awesome/font-awesome.min.css')}
        js = ('product/js/vehicle.js',)


# class LocationAdmin(admin.ModelAdmin):
#     list_display = ['phone', 'fax', 'hours', 'free_wifi', 'address', 'mailing_address',
#                     'location', 'general_manager', 'regional_manager']
#
#
# class CronFinderInline(admin.TabularInline):
#     model = CronFinder
#     extra = 3
#     show_change_link = True
#
#
# class CronJobAdmin(admin.ModelAdmin):
#     list_display = ['name']
#     inlines = [CronFinderInline]


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleMakes, VehicleMakesAdmin)
# admin.site.register(Location, LocationAdmin)
# admin.site.register(CronJob, CronJobAdmin)
