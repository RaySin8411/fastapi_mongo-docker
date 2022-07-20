import requests
import urllib.request
import ssl
import tesserocr
from PIL import Image
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context


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


# 對圖片進行降噪,可進行多輪降噪
def noise_reduction(bin_image):
    pixdata = bin_image.load()
    width, height = bin_image.size
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            count = 0
            # 上
            if pixdata[x, y - 1] > 245:
                count = count + 1
            # 下
            if pixdata[x, y + 1] > 245:
                count = count + 1
            # 左
            if pixdata[x - 1, y] > 245:
                count = count + 1
            # 右
            if pixdata[x + 1, y] > 245:
                count = count + 1
            # 左上
            if pixdata[x - 1, y - 1] > 245:
                count = count + 1
            # 左下
            if pixdata[x - 1, y + 1] > 245:
                count = count + 1
            # 右上
            if pixdata[x + 1, y - 1] > 245:
                count = count + 1
            # 右下
            if pixdata[x + 1, y + 1] > 245:
                count = count + 1
            if count > 4:
                pixdata[x, y] = 255
    return bin_image


def deal_image(path):
    img = get_image(path)
    grayImg = to_gray_image(img)
    binImg = to_bin_image(grayImg)
    return noise_reduction(binImg)


def read_verification_code(path):
    img = deal_image(path)
    print(tesserocr.image_to_text(img).strip())


if __name__ == '__main__':
    # 創建隨機請求頭
    header = {'User-Agent': UserAgent().random}
    # 網頁請求地址
    url = 'http://www.goldenjade.com.tw/captchaCheck/check/imgcheck_form.html'
    # 發送網絡請求
    resp = requests.get(url, header)
    resp.encoding = 'utf-8'
    # 解析HTML
    html = BeautifulSoup(resp.text, 'html.parser')

    src = html.find('img').get('src')
    # 組合驗證碼圖片請求地址
    img_url = 'http://www.goldenjade.com.tw/captchaCheck/check/' + src
    # 下載並設置圖片名稱
    urllib.request.urlretrieve(img_url, 'code.png')

    read_verification_code("code.png")
