# JMeter 效能測試：設定值與操作步驟

被測介面：`GET https://automationexercise.com/api/productsList`、`POST .../api/searchProduct`
檔案：`AutomationExercise_效能測試.jmx`

## 0. 安裝（一次性）
1. 安裝 JDK 8+（`java -version` 確認）。
2. 下載 Apache JMeter 5.6.3：https://jmeter.apache.org/download_jmeter.cgi ，解壓。
3. 啟動：Windows 雙擊 `bin/jmeter.bat`；macOS/Linux 執行 `bin/jmeter`。

## A. 最快：直接開現成檔
File → Open → 選 `AutomationExercise_效能測試.jmx` → 跳到「第 4 步」。

## B. 手動建立（理解每個元件設定）

### 步驟 1：Thread Group（執行緒群組）
Test Plan 右鍵 → Add → Threads (Users) → Thread Group。各場景數值：

| 場景 | Name | Threads | Ramp-up(秒) | Loop | On Error |
|---|---|---|---|---|---|
| S1 單使用者基準 | S1 (GET productsList) | 1 | 1 | 10 | Continue |
| S2 輕量併發 | S2 (GET productsList) | 10 | 5 | 10 | Continue |
| S3 中度併發 | S3 (POST searchProduct) | 50 | 10 | 5 | Continue |
| S4 高度併發 | S4 (POST searchProduct) | 100 | 15 | 5 | Continue |
| S5 持續壓力 | S5 (GET productsList) | 30 | 10 | 20 | Continue |

### 步驟 2：HTTP Request（每個群組底下加一個）
群組右鍵 → Add → Sampler → HTTP Request。

GET 類（S1、S2、S5）：
| 欄位 | 值 |
|---|---|
| Protocol | https |
| Server Name or IP | automationexercise.com |
| HTTP Method | GET |
| Path | /api/productsList |

POST 類（S3、S4）：
| 欄位 | 值 |
|---|---|
| Protocol | https |
| Server Name or IP | automationexercise.com |
| HTTP Method | POST |
| Path | /api/searchProduct |
| Parameters | Name=search_product, Value=top |

### 步驟 3：Listeners（Test Plan 右鍵 → Add → Listener）
- Aggregate Report（彙總報告，截此為圖3-2）
- Summary Report
- View Results Tree

### 步驟 3.5：序列化執行
點 Test Plan → 勾選「Run Thread Groups consecutively」，讓 5 場景依序執行。

## 第 4 步：執行與截圖
1. 工具列「掃帚 Clear All」清空舊數據。
2. 綠色 ▶ Start 執行，等執行指示跑完。
3. 點 Aggregate Report，重點欄位：Average（平均回應時間 ms）、Throughput（吞吐量/秒）、Error %、90% Line/Min/Max。
4. 截 Aggregate Report = 圖3-2。
5. 單跑某場景：其他 Thread Group 右鍵 Disable，只留一個 Enable，重跑截圖。

## （選用）命令列 + 自動 HTML 報告
```bash
jmeter -n -t AutomationExercise_效能測試.jmx -l result.jtl -e -o report_html
```
跑完開 `report_html/index.html`，Statistics 表與回應時間圖可直接截圖。

## 數據解讀（寫進結果分析）
- 回應時間隨併發（S1→S4）上升 → 高負載變慢。
- 吞吐量到瓶頸後不再提升。
- S4(100 緒) Error% > 0 多為本機資源或限流 → 寫進 5.1 風險評估並說明降低執行緒分批測。
