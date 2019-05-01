import asyncio
import base64
import json
import os
import sys
from datetime import datetime

import django
import time
import websockets

sys.path.append('../copart')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'copart.settings')
django.setup()

from product.models import VehicleInfo, Vehicle, VehicleNotExist
from django.utils.timezone import get_current_timezone
import logging

logger = logging.getLogger(__name__)

TO_DB = True

logger.debug("=="*500)


async def copart(param):
    nirvanalv = param.split('-')[1]
    param = param.split('-')[0]
    connection_params = {
        'origin': 'https://g2auction.copart.com',
        'extra_headers': {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en,ro;q=0.9,en-US;q=0.8',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Origin': 'https://g2auction.copart.com',
            'Host': f'nirvanarn{nirvanalv}.copart.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
        }
    }
    uri = f'wss://nirvanarn{nirvanalv}.copart.com/sv/ws'

    async with websockets.connect(uri, **connection_params) as websocket:
        param_1st = 'F=1&Connection-Type=JC&Y=10&V=Netscape&P=nws&W=81457-81457&X=February-12 2016&Z=MacIntel&S=ANONYMOUS&A=VB3.5&G=T&D=F&B=&R={r}&1Date={date}&'.format
        keep_alive = 'F=3&R={r}&'.format
        param_2nd = 'F=5&R={r}&E=1&N=/COPART{auction_num}/outbound,0,,F'.format

        packet_1 = param_1st(r=2, date=str(int(time.time() * 1000)))
        await websocket.send(packet_1)
        await websocket.recv()

        packet_2 = param_2nd(r=3, auction_num=param)
        await websocket.send(packet_2)
        channel_data = await websocket.recv()

        channel_data = json.loads(channel_data)

        if not channel_data[0]['d'][1][1]:
            print(f"[{param}] {channel_data}")
            print(f"[{param}] Response from WS invalid: %s" % channel_data[0]['d'][1][2])
            return
        else:
            print(f"[{param}] Connected OK!")

        r = 4

        old = datetime.now()
        while True:
            try:
                bids_data = await websocket.recv()

                greeting_data = json.loads(bids_data)
                data = greeting_data[0]['d'][1]
                if isinstance(data, dict):
                    decoded = base64.b64decode(data['Data'])
                    data = json.loads(decoded.decode())

                    if TO_DB:
                        if 'ATTRIBUTE' in data:
                            vehicle_info = VehicleInfo.objects.filter(lot=data['LOTNO']).first()

                            if vehicle_info:
                                vehicle = Vehicle.objects.get(info=vehicle_info)
                                vehicle.set_sold_price(data['BID'])
                                print(f"[{param}] Update: {vehicle}")
                            else:
                                params = {
                                    'lot': data['LOTNO'],
                                    'sold_price': data['BID'],
                                    'sale_date': datetime.now(tz=get_current_timezone())
                                }
                                obj, created = VehicleNotExist.objects.get_or_create(**params)
                                if created:
                                    print(f"[{param}] Saved : {obj}")
                        if 'TEXT' in data:
                            break
            except Exception as e:
                print(f"[{param}] Auction ERROR: ", e)

            now = datetime.now()
            if (now - old).seconds > 28:
                await websocket.send(keep_alive(r=r))
                r += 1
                old = datetime.now()


def get_copart_auction(param):
    asyncio.get_event_loop().run_until_complete(copart(param))


if __name__ == '__main__':
    arg = sys.argv[1:]

    if len(arg) == 1:
        print('started - https://www.copart.com/auctionDashboard?auctionDetails=' + arg[0][:-1].lstrip('0') + '-' +
              arg[0][-1])
        get_copart_auction(arg[0])
    else:
        print('Please input the correct command')
