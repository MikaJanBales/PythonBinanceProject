import websockets
import asyncio
import json


async def binance_xrp_exchange():
    url = 'wss://stream.binance.com:9443/stream?streams=xrpusdt@kline_1h'
    async with websockets.connect(url) as client:
        while True:
            data = json.loads(await client.recv())['data']
            title = data['s']
            high_price_1h = data['k']['h']
            price_real_time = data['k']['c']
            delta = 100 * (1 - (float(price_real_time) / float(high_price_1h)))
            if delta >= 1:
                print('Цена упала на 1% от максимальной цены за последний час!')
            print(title, price_real_time)


async def binance_all_exchange():
    url = 'wss://stream.binance.com:9443/stream?streams=!ticker_1h@arr'
    async with websockets.connect(url) as client:
        while True:
            answer_data = []
            string = 'Цена упала на 1% от максимальной цены за последний час!'
            data = json.loads(await client.recv())['data']
            for data_courses in data:
                data_one = [data_courses['s'], data_courses['c']]
                delta = 100 * (1 - (float(data_one[1]) / float(data_courses['h'])))
                if delta >= 1:
                    data_one[1] += ' - ' + string
                answer_data.append(data_one)
            print(answer_data)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(binance_xrp_exchange())
