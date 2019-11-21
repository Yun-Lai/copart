import os
import uuid
from django.db.models import Q
import datetime
import subprocess
import threading



def create_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def unique_string(length=10):
    return uuid.uuid4().hex[:length]


def filter_by_filters(lots_, params, ignore=''):
    for param_key, param_value in params.items():
        # AND condition filters
        if 'source' == param_key and 'source' != ignore:
            if 'copart' == param_value:
                lots_ = lots_.filter(info__source=True)
                # filters_ = filters_ & Q(info__source=True)
            elif 'iaai' == param_value:
                lots_ = lots_.filter(info__source=False)
                # filters_ = filters_ & Q(info__source=False)
        elif 'featured' == param_key and 'featured' != ignore:
            if len(param_value) == 0:
                pass
            for feature_ in param_value:
                if 'Buy It Now' == feature_:
                    lots_ = lots_.filter(~Q(buy_today_bid=0))
                    # filters_ = filters_ & (~Q(buy_today_bid=0))
                elif 'Run and Drive' == feature_:
                    lots_ = lots_.filter(info__lot_highlights__contains='R')
                    # filters_ = filters_ & Q(info__lot_highlights__contains='R')
                elif 'Pure Sale Items' == feature_:
                    lots_ = lots_.filter(~Q(bid_status='PURE SALE'))
                    # filters_ = filters_ & (~Q(bid_status='PURE SALE'))
                elif 'New Items' == feature_:
                    c_date = datetime.datetime.now().date()
                    f_date = c_date - datetime.timedelta(days=c_date.weekday() + 7)
                    t_date = f_date + datetime.timedelta(days=6)
                    lots_ = lots_.filter(created_at__range=(f_date, t_date))
        # OR condition filters
        elif 'makes' == param_key and 'makes' != ignore:
            if len(param_value) == 0:
                continue
            query = Q(info__make__icontains=param_value[0])
            for make_ in param_value[1:]:
                query |= Q(info__make__icontains=make_)
            lots_ = lots_.filter(query)
            # filters_ = filters_ & query
        elif 'models' == param_key and 'models' != ignore:
            if len(param_value) == 0:
                continue
            query = Q(info__model=param_value[0])
            for model_ in param_value[1:]:
                query |= Q(info__model=model_)
            lots_ = lots_.filter(query)
        elif 'years' == param_key and 'years' != ignore:
            if len(param_value) == 0:
                continue
            query = Q(info__year=param_value[0])
            for year_ in param_value[1:]:
                query |= Q(info__year=year_)
            lots_ = lots_.filter(query)
        elif 'odometers' == param_key and 'odometers' != ignore:
            pass
        elif 'locations' == param_key and 'locations' != ignore:
            if len(param_value) == 0:
                continue
            query = Q(info__location=param_value[0])
            for location_ in param_value[1:]:
                query |= Q(info__location=location_)
            lots_ = lots_.filter(query)
            # filters_ = filters_ & query
        elif 'sale_dates' == param_key and 'sale_dates' != ignore:
            if len(param_value) == 0:
                continue
            query = Q(sale_date__year=str(param_value[0]).split('/')[2],
                      sale_date__month=str(param_value[0]).split('/')[0],
                      sale_date__day=str(param_value[0]).split('/')[1])
            for sale_date_ in param_value[1:]:
                query |= Q(sale_date__year=str(sale_date_).split('/')[2],
                           sale_date__month=str(sale_date_).split('/')[0],
                           sale_date__day=str(sale_date_).split('/')[1])
            lots_ = lots_.filter(query)
            # filters_ = filters_ & query
        elif 'engine_types' == param_key and 'engine_types' != ignore:
            if len(param_value) == 0:
                continue
            query = Q(info__engine_type=param_value[0])
            for engine_type_ in param_value[1:]:
                query |= Q(info__engine_type=engine_type_)
            lots_ = lots_.filter(query)
        elif 'transmissions' == param_key and 'transmissions' != ignore:
            if len(param_value) == 0:
                continue
            query = Q(info__transmission=param_value[0])
            for transmission_ in param_value[1:]:
                query |= Q(info__transmission=transmission_)
            lots_ = lots_.filter(query)
        elif 'drive_trains' == param_key and 'drive_trains' != ignore:
            if len(param_value) == 0:
                continue
            query = Q(info__drive=param_value[0])
            for drive_trains_ in param_value[1:]:
                query |= Q(info__drive=drive_trains_)
            lots_ = lots_.filter(query)
        elif 'cylinderss' == param_key and 'cylinderss' != ignore:
            if len(param_value) == 0:
                continue
            query = Q(info__cylinders=param_value[0])
            for cylinderss_ in param_value[1:]:
                query |= Q(info__cylinders=cylinderss_)
            lots_ = lots_.filter(query)
        elif 'fuels' == param_key and 'fuels' != ignore:
            if len(param_value) == 0:
                continue
            query = Q(info__fuel=param_value[0])
            for fuels_ in param_value[1:]:
                query |= Q(info__fuel=fuels_)
            lots_ = lots_.filter(query)
        elif 'body_styles' == param_key and 'body_styles' != ignore:
            if len(param_value) == 0:
                continue
            query = Q(info__body_style=param_value[0])
            for body_styles_ in param_value[1:]:
                query |= Q(info__body_style=body_styles_)
            lots_ = lots_.filter(query)
        elif 'vehicle_types' == param_key and 'vehicle_types' != ignore:
            if len(param_value) == 0:
                continue
            query = Q(info__type=param_value[0])
            for vehicle_types_ in param_value[1:]:
                query |= Q(info__type=vehicle_types_)
            lots_ = lots_.filter(query)
        elif 'damages' == param_key and 'damages' != ignore:
            if len(param_value) == 0:
                continue
            query = Q(info__lot_1st_damage=param_value[0])
            for damages_ in param_value[1:]:
                query |= Q(info__lot_1st_damage=damages_)
            lots_ = lots_.filter(query)
        elif 'doctypes' == param_key and 'doctypes' != ignore:
            if len(param_value) == 0:
                continue
            query = Q(info__doc_type_td__contains=str(param_value[0]).upper())
            for doctypes_ in param_value[1:]:
                query |= Q(info__doc_type_td__contains=str(doctypes_).upper())
            lots_ = lots_.filter(query)
    return lots_


def set_filters_with_featured_name(filters, name):
    if 'Buy It Now' == name:
        filters = filters & (~Q(buy_today_bid=0))
    elif 'Pure Sale Items' == name:
        filters = filters & (~Q(bid_status='PURE SALE'))
    elif 'New Items' == name:
        cur_date = datetime.datetime.now().date()
        from_date = cur_date - datetime.timedelta(days=cur_date.weekday() + 7)
        to_date = from_date + datetime.timedelta(days=6)
        filters = filters & Q(created_at__range=(from_date, to_date))
    elif 'Lots with Bids' == name:
        filters = filters & (~Q(current_bid=0))
    elif 'No Bids Yet' == name:
        filters = filters & Q(current_bid=0)
    elif 'Hybrid Vehicles' == name:
        filters = filters & Q(info__fuel="HYBRID ENGINE")
    elif 'Repossessions' == name:
        filters = filters & Q(info__lot_highlights__contains='B')
    elif 'Donations' == name:
        filters = filters & Q(info__lot_highlights__contains='D')
    elif 'Featured Vehicles' == name:
        filters = filters & Q(info__lot_highlights__contains='F')
    elif 'Offsite Sales' == name:
        filters = filters & Q(info__lot_highlights__contains='O')
    elif 'Run and Drive' == name:
        filters = filters & Q(info__lot_highlights__contains='R')
    elif 'Clean Title' == name:
        filters = filters & (~Q(info__doc_type_td__icontains='salvage'))
    elif 'Salvage Title' == name:
        filters = filters & Q(info__doc_type_td__icontains='salvage')
    elif 'Front End' == name:
        filters = filters & Q(
            Q(info__lot_1st_damage__icontains='Front End') or Q(info__2nd_damage__icontains='Front End'))
    elif 'Hail Damage' == name:
        filters = filters & Q(
            Q(info__lot_1st_damage__icontains='Hail') or Q(info__lot_2nd_damage__icontains='Hail'))
    elif 'Normal Wear' == name:
        filters = filters & Q(
            Q(info__lot_1st_damage__icontains='Normal Wear') or Q(info__lot_2nd_damage__icontains='Normal Wear'))
    elif 'Minor Dents/Scratch' == name:
        filters = filters & Q(
            Q(info__lot_1st_damage__icontains='Normal Wear') or Q(info__lot_2nd_damage__icontains='Normal Wear'))
    elif 'Water/Flood' == name:
        filters = filters & Q(
            Q(info__lot_1st_damage__icontains='Water/Flood') or Q(info__lot_2nd_damage__icontains='Water/Flood'))
    return filters
