# FastAPI + MongoDB

A simple starter for building RESTful APIs with FastAPI and MongoDB. 

## 部屬
### 本地
* Install Package
```console
pip install -r requirements.txt
```


#### OCR 相關套件

[it邦幫忙-Windows 安裝方式](https://ithelp.ithome.com.tw/articles/10233316)

[github-tesserocr](https://github.com/sirfz/tesserocr/blob/master/README.rst)

* API Server
```console
python main.py
```

### docker-compose
Init

```console
docker-compose up -d
```

Rebuild API

```console
docker-compose up web --build -d
```

## 爬蟲
### Step
1. 爬新北市路名

參考網址: [全國路名資料](https://data.gov.tw/dataset/35321)

2. 爬新北營照處各區設置參數id

參考網址: [新北市政府-建管便民服務資訊網](https://building-management.publicwork.ntpc.gov.tw/_setData.jsp?rt=D1)

3. 將上訴兩表格合併

4. 跑異步架構

### 程式
```console
python crawler\async_clawer.py
```

## 參考網址
* [台北市建築管理工程處-雙語詞彙](https://dba.gov.taipei/cp.aspx?n=E8A756CFF2A5C236)