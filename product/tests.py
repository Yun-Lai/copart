import base64
import json
import asyncio
import websockets
import time
from selenium import webdriver
import random
from datetime import datetime

async def copart(param):
    nirvanalv = param.split('-')[1]
    param = param.split('-')[0]
    async with websockets.connect('wss://nirvanarn' + nirvanalv + '.copart.com/sv/ws') as websocket:
        param_1st = 'F=1&Connection-Type=JC&Y=10&V=Netscape&P=nws&W=81457-81457&X=February-12 2016&Z=Linux&S=ANONYMOUS&A=VB3&G=T&D=F&B=&R={}&1Date={}&'.format
        await websocket.send(param_1st(2, str(int(time.time() * 1000))))
        greeting = await websocket.recv()
        print("{}".format(greeting))

        param_2nd = 'F=5&R={}&E=1&N=/COPART{}/outbound,0,,F'.format
        await websocket.send(param_2nd(3, param))
        greeting = await websocket.recv()
        print("{}".format(greeting))

        keep_alive = 'F=3&R={}&'.format
        r = 4

        old = datetime.now()
        while True:
            greeting = await websocket.recv()
            try:
                decoded = base64.b64decode(json.loads(greeting)[0]['d'][1]['Data'])
                data = json.loads(decoded.decode())
                if 'ATTRIBUTE' in data:
                    print(','.join([param, data['LOTNO'], data['BID']]))

                    try:
                        print(data['BID'], data['LOTNO'])
                    except Exception as e:
                        print(e)

                if 'TEXT' in data:
                    break
            except:
                pass
            now = datetime.now()
            if (now - old).seconds > 28:
                await websocket.send(keep_alive(3, r))
                r += 1
                old = datetime.now()


def get_copart_auction(param):
    asyncio.get_event_loop().run_until_complete(copart(param))


def scrap_live_auctions():
    live_auctions = []
    try:
        options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('--disable-extensions')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        while True:
            try:
                driver = webdriver.Chrome(chrome_options=options)
                break
            except:
                time.sleep(1)
        driver.implicitly_wait(300)
        driver.set_page_load_timeout(300)

        driver.get('https://www.copart.com/todaysAuction/')

        auction_live_now = driver.find_element_by_xpath('//table[@id="auctionLiveNow-datatable"]')
        auction_later_today = driver.find_element_by_xpath('//table[@id="auctionLaterToday-datatable"]')
        no_auction = 'There are no auctions available at this time.'
        if auction_live_now.text.__contains__(no_auction) and auction_later_today.text.__contains__(no_auction):
            print(no_auction)
            return

        auction_urls = auction_live_now.find_elements_by_xpath('./tbody/tr/td/ul/li[1]/a')
        auction_urls = [a.get_attribute('href') for a in auction_urls]

        driver.close()
        driver.quit()

        params = []
        for url in auction_urls:
            param = url.split('=')[-1]
            num = '%03d' % int(param.split('-')[0])
            params.append(num + param.split('-')[1])

        for param in params:
            if param in live_auctions:
                continue
            get_copart_auction(param + '-' + str(random.randint(204, 206)))
            print('new auction -', param)
        live_auctions = params
        print(len(params))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # scrap_live_auctions()

    # get average count of VehicleMakes
    data = [0, 9, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 11, 0, 1, 38, 0, 0, 2, 18, 0, 5, 2, 0, 0, 0, 0, 3, 0, 3, 7, 0, 0, 24, 0, 19, 3, 0, 1, 73, 0, 0, 7, 0, 13, 0, 0, 0, 0, 0, 0, 26, 0, 3, 0, 952, 416, 4, 28, 0, 245, 9, 15, 0, 2, 0, 6, 23, 17, 1, 228, 2, 0, 19, 37, 305, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 6, 7, 1, 1, 0, 1, 0, 0, 0, 3, 0, 3, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 1, 0, 2, 0, 5, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 0, 2, 2, 0, 0, 0, 7, 1, 0, 1, 0, 3, 0, 1, 0, 1, 1, 0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 0, 1, 2, 0, 0, 1, 1, 18, 12, 0, 1, 0, 5, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 0, 0, 0, 0, 0, 0, 7, 0, 0, 3, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 9, 1, 16, 1, 0, 6, 47, 0, 0, 29, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 203, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 439, 2, 0, 0, 0, 0, 103, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 45, 35, 0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0, 1, 1, 16, 1, 1, 1, 0, 0, 24, 5, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 4, 2, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 1, 0, 0, 9, 0, 0, 1, 0, 0, 1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 3, 0, 1, 6, 0, 0, 0, 1, 0, 0, 26, 13, 4, 0, 0, 0, 0, 0, 1, 0, 7, 0, 0, 1, 0, 0, 0, 0, 8, 0, 1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 55, 0, 8, 0, 1, 0, 1, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 2, 2, 1, 26, 1, 0, 0, 1, 1, 2, 119, 1, 0, 0, 33, 0, 5, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 11, 3, 1, 0, 1, 0, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 1, 0, 0, 1, 4, 5, 0, 0, 0, 0, 0, 4, 2, 3, 1, 0, 4, 1, 0, 1, 0, 3, 0, 1, 1, 0, 0, 2, 4, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 6, 3, 0, 0, 7, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0, 0, 0, 16, 0, 0, 2, 0, 0, 0, 0, 0, 15, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 2, 5, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 4, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 6, 1, 16, 0, 0, 0, 3, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 8, 1, 0, 0, 2, 0, 0, 0, 0, 5, 1, 3, 0, 3, 0, 4, 0, 0, 2, 0, 0, 1, 0, 0, 26, 25, 0, 0, 2, 0, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 6, 2, 0, 4, 0, 0, 0, 2, 0, 0, 2, 4, 0, 0, 0, 5, 1, 0, 0, 3, 0, 0, 0, 2, 0, 0, 3, 2, 2, 0, 0, 1, 1, 19, 0, 1, 0, 0, 0, 0, 0, 1, 4, 7, 0, 4, 2, 0, 1, 0, 8, 0, 8, 3, 0, 1, 1, 3, 0, 0, 1, 0, 0, 4, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 10, 0, 2, 0, 4, 0, 0, 0, 0, 1, 0, 0, 9, 0, 0, 1, 8, 1, 4, 13, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 10, 3, 6, 43, 0, 32, 7, 3, 22, 23, 3, 6, 0, 32, 1, 0, 0, 33, 62, 107, 0, 0, 4, 4, 0, 3, 1, 0, 2, 25, 7, 0, 0, 13, 2, 0, 44, 34, 95, 1, 6, 2, 7, 3, 7, 0, 0, 2, 0, 1, 0, 3, 0, 0, 0, 0, 3, 3, 0, 3, 6, 11, 108, 6, 2, 8, 17, 1, 8, 10, 6, 22, 0, 1, 0, 3, 17, 7, 12, 5, 26, 2, 5, 1, 6, 0, 9, 2, 9, 3, 0, 0, 1, 1, 0, 0, 4, 1, 3, 0, 0, 14, 3, 18, 5, 4, 0, 0, 1, 0, 7, 3, 17, 0, 0, 5, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 7, 1, 0, 0, 0, 0, 1, 0, 0, 1, 22, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 29, 2, 0, 0, 0, 0, 17, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 146, 3, 0, 0, 0, 0, 78, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 81, 0, 2, 1, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 84, 1, 0, 0, 10, 0, 4, 0, 0, 0, 1318, 24, 2, 3, 0, 7, 1105, 4, 0, 22, 0, 0, 2621, 0, 1802, 1383, 0, 14166, 2949, 0, 1, 3, 0, 7, 0, 0, 5641, 2, 5, 0, 1, 10, 135, 14952, 0, 27, 0, 2483, 68, 9998, 65, 5022, 1181, 17, 98, 257, 3488, 34, 3282, 0, 5, 0, 340, 2183, 884, 5, 35, 1, 2282, 3, 2395, 823, 0, 9, 1, 386, 1089, 0, 2, 9683, 2, 0, 243, 0, 0, 3, 0, 1, 0, 71, 1482, 227, 549, 0, 1, 1, 10, 0, 151, 0, 915, 62, 25, 0, 2, 2064, 357, 49, 16047, 5, 2695, 816, 0, 1, 22, 0]
    total = sum(data)
    sub = 0
    for id, make in enumerate(data):
        if sub >= 31125:
            print(id)
            sub = 0
        sub += make
    print(len(data), sum(data))
    print(sum(data[:1354]), sum(data[1354:1375]), sum(data[1375:1405]), sum(data[1405:]))
