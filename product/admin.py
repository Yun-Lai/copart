from django.contrib import admin

from product.models import *
from product.filters import DescriptionFilter, MultipleChoicesFieldListFilter, MultipleChangeList, SourceFilter, SoldFilter


class VehicleMakesAdmin(admin.ModelAdmin):
    list_display = ['type', 'description', 'scrap_link']
    list_filter = (DescriptionFilter, ('type', MultipleChoicesFieldListFilter))
    search_fields = ['description']

    def get_changelist(self, request, **kwargs):
        return MultipleChangeList


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['avatar_img', 'vin', 'lot', 'year', 'make', 'model', 'color', 'item', 'location', 'lane_row',
                    'sale_date', 'odometer', 'doc_type', 'lot_1st_damage', 'est_retail_value',
                    'current_bid_', 'sold_price_', 'source_']

    list_display_links = ['vin', 'lot']

    list_filter = [SourceFilter, SoldFilter]

    search_fields = ['name', 'vin', 'lot', 'year', 'make', 'model']

    readonly_fields = ['source_', 'images_', 'thumb_images_']

    fieldsets = [
        ('', {'fields': ['vin', 'lot', 'name', 'make', 'model', 'year', 'location', 'source_']}),
        ('Lot', {'fields': ['doc_type_ts', 'doc_type_stt', 'doc_type_td', 'odometer_orr', 'odometer_ord',
                            'lot_highlights', 'lot_seller', 'lot_1st_damage', 'lot_2nd_damage', 'retail_value']}),
        ('Features', {'fields': ['body_style', 'color', 'engine_type', 'cylinders', 'transmission',
                                 'drive', 'fuel', 'keys', 'notes']}),
        ('Bid Information', {'fields': ['bid_status', 'sale_status', 'current_bid', 'buy_today_bid', 'sold_price', 'currency']}),
        ('Sale Information', {'fields': ['location', 'lane', 'item', 'grid', 'sale_date', 'last_updated']}),
        ('Images', {'fields': ['avatar', 'images_', 'thumb_images_']}),
        ('Foregoing', {'fields': ['foregoing', 'show']}),
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
