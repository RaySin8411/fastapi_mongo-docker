import csv
import requests
import shutil
import tesserocr
import urllib.request
from PIL import Image
from bs4 import BeautifulSoup


# 獲取圖片img物件
def get_image(path):
    img = Image.open(path)
    return img


# 將彩色圖片轉換為灰度圖片
def to_gray_image(img):
    img_gary = img.convert('L')
    return img_gary


# 將灰度圖片二值化
def to_bin_image(img_gray, threshold=165):
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
        code = int(''.join(filter(str.isdigit, ocr_code)))
    except:
        code = 1234

    url = "https://building-management.publicwork.ntpc.gov.tw/CheckCode"
    resp = requests.post(
        url, cookies=cookies,
        headers={"Content-Type": "application/x-www-form-urlencoded"}, data={"code": code}
    )
    return resp, code


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

    # 檢查驗證碼
    failure_list = []
    for item in data:
        print(item['D1V'])
        for road in item['road_list']:
            print(road)
            params = {"rt": "BM", "PagePT": 0, "A2": 3, "D1V": item['D1V'], "D1": item['D1'], "D3": road}
            resp, code = check_code()
            params.setdefault('Z1', code)
            if resp.status_code == 200:
                if resp.json() == True:
                    # 查詢建照
                    url = "https://building-management.publicwork.ntpc.gov.tw/bm_list.jsp"
                    cookies = resp.cookies.get_dict()
                    resp = requests.post(
                        url, cookies=cookies,
                        headers={"Content-Type": "application/x-www-form-urlencoded"}, data=params
                    )
                    html = BeautifulSoup(resp.text, 'html.parser')
                    print(html.find_all('tbody'))
                else:
                    print('驗證失敗')

                    failure_list.append({"D1V": item['D1V'], "D1": item['D1'], "D3": road})
