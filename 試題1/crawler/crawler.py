import csv
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # 爬新北市路名
    url = "https://data.moi.gov.tw/MoiOD/System/DownloadFile.aspx?DATA=99E4BBC4-11E2-410C-B749-C604267DA1EE"
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        tmp_list = list(cr)
        new_taipei = [{"city": row[0], "site_id": row[1], "road": row[2]} for row in tmp_list if row[0] == '新北市']
    print(new_taipei)

    # 爬新北營照處各區設置參數id
    url = "https://building-management.publicwork.ntpc.gov.tw/_setData.jsp?rt=D1"
    resp = requests.get(url)
    html = BeautifulSoup(resp.text, 'html.parser')
    body = html.find_all('div')
    area = [{"D1": test.get('onclick')[12:15], "D1V": test.get('onclick')[18:24]} for test in body]
    print(area)
