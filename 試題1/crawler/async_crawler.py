import asyncio
import time
import csv
import requests
import tesserocr
from aiohttp import ClientSession, TCPConnector
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urlencode


# 定義協程(coroutine)
async def main(item):
    async with ClientSession() as session:
        length = len(item['road_list'])
        tasks = [asyncio.create_task(fetch(road, item, session, index)) for road, index in
                 zip(item['road_list'], range(length))]
        await asyncio.gather(*tasks)


async def fetch(road, item, session, index):
    params = dict()
    info = check_code(f'code_{index}')
    resp = info['resp']
    while resp.status_code != 200 or resp.json() != True:
        info = check_code(f'code_{index}')
        resp = info['resp']
    code = info['code']
    cookies = info['cookies']
    params.setdefault('rt', "BM")
    params.setdefault('PagePT', 0)
    params.setdefault('A2', 3)
    params.setdefault('D1V', item['D1V'])
    params.setdefault('D1', int(item['D1']))
    params.setdefault('D3', road)
    params.setdefault('Z1', code)
    # 查詢建照
    url = "https://building-management.publicwork.ntpc.gov.tw/bm_list.jsp"
    try:
        params_big5 = urlencode(params, encoding='big5')
    except:
        params_big5 = params
    headers = {
        "User-Agent":
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
            "like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"}
    async with session.post(url, cookies=cookies, headers=headers, data=params_big5) as response:
        html_body = await response.text()
        html = BeautifulSoup(html_body, 'html.parser')
        road_count = int(html.find('span').get_text())
        print(road + f':{road_count}')
        if road_count != 0:
            pages = road_count // 7 + 1
            asyncio.create_task(create_buildings(html, item, road, session))
            if pages > 1:
                del params['rt']
                for para_1 in range(2, pages + 1):
                    params.update({'PagePT': para_1})
                    try:
                        params_big5 = urlencode(params, encoding='big5')
                    except:
                        params_big5 = params
                    async with session.post(url, cookies=cookies, headers=headers, data=params_big5) as response:
                        html_body = await response.text()
                        html = BeautifulSoup(html_body, 'html.parser')
                        asyncio.create_task(create_buildings(html, item, road, session))
                time.sleep(0.1)
            time.sleep(0.1)
        time.sleep(0.1)
        print(f'{item["D1V"]} {road} finished')



async def create_buildings(html, item, road, session):
    for row in html.find_all('tbody')[0].find_all('tr'):
        part_data = [td.text for td in row.find_all('td')]
        post_dict = {
            "city_area": item['D1V'], "area_id": item['D1'], "road": road, "use_license": part_data[0],
            "construction_license": part_data[1], "applicant": part_data[2], "designer": part_data[3],
            "address": part_data[4], "date": part_data[5]
        }
        async with session.post(
                url="http://127.0.0.1:80/building/",
                headers={"Content-Type": "application/json"}, json=post_dict) as resp:
            print(await resp.text())


def integrate_new_city_data():
    # 爬新北市路名
    url = "https://data.moi.gov.tw/MoiOD/System/DownloadFile.aspx?DATA=99E4BBC4-11E2-410C-B749-C604267DA1EE"
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        tmp_list = list(cr)
        new_taipei = [{"city": row[0], "site_id": row[1], "road": row[2]} for row in tmp_list if row[0] == '新北市']

    # 爬新北營照處各區設置參數id
    url = "https://building-management.publicwork.ntpc.gov.tw/_setData.jsp?rt=D1"
    resp = requests.get(url)
    html = BeautifulSoup(resp.text, 'html.parser')
    body = html.find_all('div')
    area = [{"D1": test.get('onclick')[12:15], "D1V": test.get('onclick')[18:24]} for test in body]

    # 整合上方資料
    data = []
    for item in area:
        road_list = []
        for x in new_taipei:
            if x['site_id'] == item['D1V']:
                road_list.append(x['road'])
        item['road_list'] = road_list
        data.append(item)
    return data


# 獲取圖片img物件
def get_image(path):
    img = Image.open(path)
    return img


# 將彩色圖片轉換為灰度圖片
def to_gray_image(img):
    img_gary = img.convert('L')
    return img_gary


# 將灰度圖片二值化
def to_bin_image(img_gray, threshold=150):
    pixdata = img_gray.load()
    width, height = img_gray.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img_gray


def deal_image(path):
    img = get_image(path)
    grayImg = to_gray_image(img)
    return to_bin_image(grayImg)


def read_verification_code(path):
    img = deal_image(path)
    return tesserocr.image_to_text(img)


def check_code(image_name):
    img_url = "https://building-management.publicwork.ntpc.gov.tw/ImageServlet"
    resp = requests.get(img_url, stream=True)
    cookies = resp.cookies.get_dict()
    if resp.status_code == 200:
        with open(f"{image_name}.png", 'wb') as f:
            for chunk in resp:
                f.write(chunk)

    ocr_code = read_verification_code(f"{image_name}.png")
    try:
        code = ''.join(filter(str.isdigit, ocr_code))
    except:
        code = '1234'

    url = "https://building-management.publicwork.ntpc.gov.tw/CheckCode"
    resp = requests.post(
        url, cookies=cookies,
        headers={"Content-Type": "application/x-www-form-urlencoded"}, data={"code": code}
    )
    return {"resp": resp, "code": code, "cookies": cookies}


if __name__ == '__main__':
    new_taipei = integrate_new_city_data()
    start_time = time.time()  # 開始執行時間
    for item in new_taipei:
        print(item['D1V'] + f": road {len(item['road_list'])}")
        loop = asyncio.get_event_loop()  # 建立事件迴圈(Event Loop)
        loop.run_until_complete(main(item))  # 執行協程(coroutine)
    print("花費:" + str(time.time() - start_time) + "秒")
