import csv
import requests
import shutil
import tesserocr
import urllib.request
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urlencode


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


def check_code():
    img_url = "https://building-management.publicwork.ntpc.gov.tw/ImageServlet"
    resp = requests.get(img_url, stream=True)
    cookies = resp.cookies.get_dict()
    if resp.status_code == 200:
        with open("code.png", 'wb') as f:
            for chunk in resp:
                f.write(chunk)

    ocr_code = read_verification_code("code.png")
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

    final_data = []
    for item in data:
        print(item['D1V'] + f": road {len(item['road_list'])}")
        item.setdefault('road_item_count', item['road_list'])
        cnt = 0
        road_dict = {}
        for road in item['road_list']:

            params = dict()
            info = check_code()
            resp = info['resp']
            while resp.status_code != 200 or resp.json() != True:
                info = check_code()
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
            session = requests.Session()
            resp = session.post(
                url, cookies=cookies, headers=headers, data=params_big5
            )
            html = BeautifulSoup(resp.text, 'html.parser')
            road_count = int(html.find('span').get_text())
            print(road + f':{road_count}')
            road_dict.setdefault(item['D1V'], road_count)
            cnt += road_count

        item.setdefault('road_dict', road_dict)
        del item['road_list']
        item.setdefault('road_total_count', cnt)
        final_data.append(item)
        print('*' * 20)

    print(final_data)
