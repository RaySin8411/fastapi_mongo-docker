## 破解網站圖片驗證碼
### 想法

使用tesserocr去識別驗證碼

### 步驟

1. 抓取圖片
2. 對圖片做處理
    a. 灰階化
    b. 二值化
    c. 降躁
3. 使用tesserocr去識別驗證碼
4. 將取得的驗證碼輸入完成驗證(尚未完成)

### 優化方式
下載隨機圖片多張並標記，然後訓練模型替換tesserocr，增加通過率

### Reference
* [Tesseract](https://tesseract-ocr.github.io/tessdoc/Downloads.html)
* [Tesserocr](https://github.com/sirfz/tesserocr)
* [Github - UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
* [Tesseract安裝](https://ithelp.ithome.com.tw/articles/10233316)
* [python 圖片處理](https://www.796t.com/article.php?id=196117)
