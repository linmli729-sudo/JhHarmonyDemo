# Selenium 瀏覽器功能自動化測試

對 Automation Exercise (https://automationexercise.com) 的關鍵功能流程做自動化，
每個測試結束自動截圖到 `screenshots/`，可直接放入報告（對應圖4-1 來源）。

## 前置需求
- Python 3.9+
- Google Chrome（已安裝即可；Selenium 4.6+ 內建 Selenium Manager 會自動下載對應 chromedriver）

## 安裝
```bash
cd 軟體測試大作業/selenium
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 執行
```bash
pytest -v                              # 有頭模式，會開啟瀏覽器看執行過程
HEADLESS=1 pytest -v                   # 無頭模式（伺服器/CI）
pytest -v --html=report.html --self-contained-html   # 另產出 HTML 報告可截圖
```

## 涵蓋的測試（對應功能模組）
| 測試函式 | 對應案例 | 模組 |
|---|---|---|
| test_register_new_user | TC-002/028/030 | 註冊（建立→登入→刪除清理）|
| test_login_invalid | TC-032 | 登入（無效帳密）|
| test_search_product | TC-059 | 搜尋（關鍵字 top）|
| test_add_to_cart | TC-109 | 購物車（加入商品）|
| test_contact_us | TC-161 | 聯絡我們（表單送出）|
| test_subscription | TC-183 | 訂閱（頁尾電子報）|

## 截圖與報告
- 執行後 `screenshots/` 內每支測試各一張 PNG。
- 終端機的 `PASSED/FAILED` 綠紅結果，或 `report.html`，都可截圖作為自動化執行證明。

## 注意事項
- 該網站含 Google 廣告 iframe，偶爾會蓋住元素；腳本已用 JS 點擊與捲動降低干擾，
  若某次因廣告失敗，重跑一次即可。
- 註冊測試使用時間戳唯一 Email，並於結尾刪除帳號，避免殘留資料。
