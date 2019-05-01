import asyncio
import base64
import json
import sys
from datetime import datetime

import psycopg2
import time
import websockets

from dbconfig import read_postgres_db_config

TO_DB = True

if TO_DB:
    db_config = read_postgres_db_config()
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()


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
            print(channel_data)
            print("Response from WS invalid: ", channel_data[0]['d'][1][2])
            return
        else:
            print("Connected OK!")

        r = 4

        old = datetime.now()
        while True:
            bids_data = await websocket.recv()
            try:
                greeting_data = json.loads(bids_data)
                data = greeting_data[0]['d'][1]
                if not isinstance(data, dict):
                    print(f"Received {bids_data} but is invalid, keep listening", bids_data)
                    continue

                decoded = base64.b64decode(data['Data'])
                data = json.loads(decoded.decode())

                if TO_DB:
                    if 'ATTRIBUTE' in data:
                        query = "SELECT id FROM product_vehicleinfo WHERE lot = {}".format
                        cursor.execute(query(data['LOTNO']))
                        vehicle_info_item = cursor.fetchone()
                        if vehicle_info_item:
                            query = "UPDATE product_vehicle SET sold_price = {}, sale_status = 'SOLD' WHERE info_id = {}".format
                            cursor.execute(query(data['BID'], vehicle_info_item[0]))
                            conn.commit()
                            print(','.join([param, data['LOTNO'], data['BID'], 'updated']))
                        else:
                            query = "INSERT INTO product_vehiclenotexist(lot, sold_price, sale_date) VALUES ({}, {}, '{}')".format
                            cursor.execute(query(data['LOTNO'], data['BID'], str(datetime.now())[:-7]))
                            conn.commit()
                            print(
                                ','.join([param, data['LOTNO'], data['BID'], 'saved to product_vehiclenotexist table']))

                    if 'TEXT' in data:
                        # conn.commit()
                        cursor.close()
                        conn.close()
                        break
            except Exception as e:
                print("Autction ERROR: ", e)

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
