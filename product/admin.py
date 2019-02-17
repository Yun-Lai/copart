from django.contrib import admin

from product.models import *
from product.filters import DescriptionFilter, MultipleChoicesFieldListFilter, MultipleChangeList, SourceFilter, SoldFilter


class VehicleMakesAdmin(admin.ModelAdmin):
    list_display = ['type', 'description', 'scrap_link']
    list_filter = (DescriptionFilter, ('type', MultipleChoicesFieldListFilter))
    search_fields = ['description']

    def get_changelist(self, request, **kwargs):
        return MultipleChangeList


class FilterAdmin(admin.ModelAdmin):
    list_display = ['name', 'count', 'type']


class VehicleInfoAdmin(admin.ModelAdmin):
    list_display = ['avatar_img', 'vin', 'lot_', 'year', 'make', 'model', 'est_retail_value',
                    'odometer', 'lot_1st_damage', 'source_']

    list_display_links = ['vin']

    list_filter = [SourceFilter, 'make']

    search_fields = ['name', 'vin', 'lot', 'year', 'make', 'model']

    readonly_fields = ['source_', 'images_', 'thumb_images_']

    fieldsets = [
        ('', {'fields': ['vin', 'lot', 'type', 'name', 'make', 'model', 'year', 'currency', 'source_']}),
        ('Lot', {'fields': ['doc_type_ts', 'doc_type_stt', 'doc_type_td', 'odometer_orr', 'odometer_ord',
                            'lot_highlights', 'lot_seller', 'lot_1st_damage', 'lot_2nd_damage', 'retail_value']}),
        ('Features', {'fields': ['body_style', 'color', 'engine_type', 'cylinders', 'transmission',
                                 'drive', 'fuel', 'keys', 'notes']}),
        ('Location', {'fields': ['location', 'lane', 'item', 'grid']}),
        ('Images', {'fields': ['avatar', 'images_', 'thumb_images_']}),
    ]


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['avatar_img', 'vin', 'lot', 'year', 'make', 'model_', 'est_retail_value',
                    'current_bid_', 'sale_date', 'odometer', 'primary_damage', 'source']

    list_display_links = ['vin']

    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        ('Bid Information', {'fields': ['bid_status', 'sale_status', 'current_bid', 'buy_today_bid', 'sold_price']}),
        ('Sale Information', {'fields': ['sale_date', 'last_updated']}),
        ('Dates', {'fields': ['created_at', 'updated_at']}),
    ]


class VehicleSoldAdmin(admin.ModelAdmin):
    list_display = ['avatar_img', 'vin', 'lot', 'year', 'make', 'model_', 'est_retail_value',
                    'current_bid_', 'sold_price_', 'sale_date', 'odometer', 'primary_damage', 'source']

    list_display_links = ['vin']

    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        ('Bid Information', {'fields': ['bid_status', 'sale_status', 'current_bid', 'buy_today_bid', 'sold_price']}),
        ('Sale Information', {'fields': ['sale_date', 'last_updated']}),
        ('Dates', {'fields': ['created_at', 'updated_at']}),
    ]


class LocationAdmin(admin.ModelAdmin):
    list_filter = ['source']
    list_display = ['location', 'count', 'source']


class ForegoingAdmin(admin.ModelAdmin):
    list_filter = ['sold']
    search_fields = ['parent_lot', 'foregoing_lot']
    list_display = ['parent_lot', 'foregoing_lot', 'sold']


admin.site.register(VehicleInfo, VehicleInfoAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleSold, VehicleSoldAdmin)
admin.site.register(VehicleMakes, VehicleMakesAdmin)
admin.site.register(Filter, FilterAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Foregoing, ForegoingAdmin)
