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
    scrap_live_auctions()