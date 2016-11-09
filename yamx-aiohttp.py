import re
import time
import asyncio
from lxml import etree
from aiohttp import ClientSession


async def down(url,H):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    async with ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            response = await response.text()
            H.append(response)
            print(0)


def getall(html):
    uli = []
    sel = etree.HTML(html)
    links = sel.xpath('//div/div[3]/div[1]/a/@href')
    for i in links:
        uli.append(i)
    return uli 


def geturl(html):
    print('geturl')
    ul = []
    sel = etree.HTML(html)
    links = sel.xpath('//li/@ data-dp-url')
    print(links)
    for i in links:
        link = 'https://www.amazon.cn{}'.format(i)
        ul.append(link)
    return ul


def fen(r):
    sel = etree.HTML(r)
    name = sel.xpath('//*[@id="productTitle"]/text()')
    price = sel.xpath('//*[@id="priceblock_ourprice"]/text()')
    links = sel.xpath('//li/@ data-dp-url')
    if name and price:
        con = name[0].strip() + price[0]
        print(con)
 



if __name__ == '__main__':

    url = 'https://www.amazon.cn/s/ref=sr_pg_3?rh=n%3A2016116051%2Cn%3A%212016117051%2Cn%3A664978051%2Cn%3A665002051%2Cp_89%3AHuawei+华为&page={}&bbn=665002051&ie=UTF8'
    page_urls = [url.format(i) for i in range(1,14)]
    loop = asyncio.get_event_loop()
    HTML = []
    tasks = [down(host,HTML) for host in page_urls]
    loop.run_until_complete(asyncio.wait(tasks))
    chap = []
    for html in HTML:
        print(html)
        chap.extend(getall(html))

    nam = []
    tasks = [down(ul,nam) for ul in chap]
    loop.run_until_complete(asyncio.wait(tasks))
    lin = []
    for htm in nam:        
        lin.extend(geturl(htm))

    res = []
    tasks = [down(url,res) for url in lin]
    loop.run_until_complete(asyncio.wait(tasks))
    for r in res:
        fen(r)
    loop.close
    
