# -*- coding: utf-8 -*-
"""產生《軟體測試》大作業——白盒測試報告 Word 檔。
內容：白盒測試概述、兩個核心模組原始碼、程式流程圖（圖B-1/B-2）、
語句覆蓋／判定覆蓋／條件覆蓋測試用例、覆蓋率匯總與結論。
"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE = os.path.dirname(os.path.abspath(__file__))
CN_FONT = "標楷體"
BODY_CN = "仿宋"
BODY_EN = "Times New Roman"
CODE_EN = "Consolas"
RED = RGBColor(0xC0, 0x00, 0x00)


def _set_run_font(r, cn=BODY_CN, en=BODY_EN, size=12, bold=False, color=None):
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.name = en
    rpr = r._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:eastAsia"), cn)
    if color is not None:
        r.font.color.rgb = color


def heading(doc, text, level=1):
    sizes = {1: 16, 2: 14, 3: 13}
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.style = doc.styles["Heading %d" % level]
    r = p.add_run(text)
    _set_run_font(r, cn=CN_FONT, size=sizes.get(level, 13), bold=True)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p


def body(doc, text, red=False, indent=True, size=12):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = 1.5
    pf.space_after = Pt(4)
    if indent:
        pf.first_line_indent = Pt(size * 2)
    r = p.add_run(text)
    _set_run_font(r, cn=BODY_CN, size=size, color=RED if red else None)
    return p


def code_block(doc, code):
    """以等寬字型呈現原始碼，淺灰底框。"""
    for line in code.split("\n"):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.left_indent = Pt(12)
        r = p.add_run(line if line else " ")
        _set_run_font(r, cn=BODY_CN, en=CODE_EN, size=9.5)


def add_image(doc, path, width_cm=15):
    if not os.path.exists(path):
        body(doc, "〔流程圖檔不存在：%s〕" % os.path.basename(path), red=True)
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(path, width=Cm(width_cm))


def caption(doc, text, above=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6 if above else 2)
    p.paragraph_format.space_after = Pt(2 if above else 6)
    r = p.add_run(text)
    _set_run_font(r, cn=CN_FONT, size=10.5, bold=True)
    return p


def make_table(doc, headers, rows, widths=None, header_size=10, body_size=9.5):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        _set_run_font(r, cn=CN_FONT, size=header_size, bold=True)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            r = p.add_run(str(val))
            _set_run_font(r, cn=BODY_CN, size=body_size)
    if widths:
        for i, w in enumerate(widths):
            for row in t.rows:
                row.cells[i].width = Cm(w)
    return t


def cover(doc):
    def c_title(text, size, bold=True, sb=0, sa=12):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(sb); p.paragraph_format.space_after = Pt(sa)
        r = p.add_run(text); _set_run_font(r, cn=CN_FONT, size=size, bold=bold)
    c_title("台灣國立大學", 26, sb=24, sa=40)
    c_title("《軟體測試》", 30, sa=6)
    c_title("白盒測試報告", 30, sa=30)
    c_title("—— 核心邏輯模組之語句／判定／條件覆蓋測試 ——", 14, bold=False, sa=48)
    fields = [
        ("課程名稱", "軟體測試"),
        ("被測系統", "Automation Exercise 核心邏輯模組"),
        ("測試方法", "白盒測試（覆蓋率分析）"),
        ("姓　　名", "〔手寫〕"),
        ("學　　號", "〔手寫〕"),
        ("指導老師", "張　導師"),
        ("日　　期", "中華民國　　年　　月　　日"),
    ]
    table = doc.add_table(rows=len(fields), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    for i, (k, v) in enumerate(fields):
        c0, c1 = table.rows[i].cells
        c0.width = Cm(3.5); c1.width = Cm(10.5)
        for cell, val, bold, al in ((c0, k, True, WD_ALIGN_PARAGRAPH.CENTER), (c1, v, False, WD_ALIGN_PARAGRAPH.LEFT)):
            cell.text = ""; p = cell.paragraphs[0]; p.alignment = al
            r = p.add_run(val); _set_run_font(r, cn=CN_FONT, size=14, bold=bold)
    doc.add_page_break()


CODE_CALC = '''def calc_order_amount(items, member_level, coupon=0):
    subtotal = 0                                  # S1
    for price, qty in items:                      # S2  迴圈
        subtotal += price * qty                   # S3
    if member_level == 2:                          # D1
        discount = 0.90                            # S5
    elif member_level == 1:                        # D2
        discount = 0.95                            # S7
    else:
        discount = 1.0                             # S8
    total = subtotal * discount                    # S9
    if member_level >= 1 and subtotal >= 1000:     # D3 (C1 且 C2)
        total -= 100                               # S11
    total -= coupon                                # S12
    if total < 0:                                  # D4
        total = 0                                  # S14
    return round(total, 2)                          # S15'''

CODE_SORT = '''def bubble_sort_by_price(products):
    arr = list(products)                # B1
    n = len(arr)                        # B1
    for i in range(n - 1):              # B2 外層迴圈  DB1: i < n-1
        swapped = False                 # B3
        for j in range(n - 1 - i):      # B4 內層迴圈  DB2: j < n-1-i
            if arr[j][1] > arr[j+1][1]: # B5  DB3: 相鄰價格比較
                arr[j], arr[j+1] = arr[j+1], arr[j]   # B6
                swapped = True          # B6
        if not swapped:                 # B7  DB4: 本趟未交換
            break                       # B7  提前結束
    return arr                          # B8'''


def build():
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Cm(2.5); sec.bottom_margin = Cm(2.5)
    sec.left_margin = Cm(2.5); sec.right_margin = Cm(2.5)

    cover(doc)

    # 一、白盒測試概述
    heading(doc, "一、白盒測試概述", 1)
    heading(doc, "1.1 測試目的與方法", 2)
    body(doc, "白盒測試（又稱結構測試）以程式的內部邏輯結構為依據設計測試用例，要求測試人員了解原始碼的控制流程。本報告針對 Automation Exercise 電子商務系統之兩個核心邏輯模組——「購物車訂單金額計算」與「商品價格冒泡排序」——繪製程式流程圖，並依下列三種邏輯覆蓋準則設計測試用例，量化覆蓋程度：")
    make_table(doc, ["覆蓋準則", "定義", "強度"], [
        ["語句覆蓋 (Statement)", "設計用例使程式中每一條可執行語句至少被執行一次", "最弱"],
        ["判定覆蓋 (Decision/Branch)", "使每個判定（分支）的取真與取假至少各執行一次", "較強"],
        ["條件覆蓋 (Condition)", "使每個判定中每一個原子條件的真、假取值至少各出現一次", "較強"],
    ], widths=[4.5, 8.5, 2], body_size=10, header_size=10)
    body(doc, "三者強弱關係：語句覆蓋 ＜ 判定覆蓋；條件覆蓋著重於複合判定中各原子條件的取值，常與判定覆蓋互補。本報告對含複合條件的判定（D3）特別進行條件覆蓋設計。")
    heading(doc, "1.2 被測核心模組", 2)
    make_table(doc, ["模組", "函式", "說明", "對應業務"], [
        ["模組一", "calc_order_amount", "依會員等級折扣、滿額立減、優惠券計算訂單應付金額", "購物車結帳金額"],
        ["模組二", "bubble_sort_by_price", "將商品依價格升序排序（冒泡排序，含提前結束最佳化）", "商品排序顯示"],
    ], widths=[2, 4.2, 6.3, 2.5], body_size=9.5, header_size=10)

    # 二、模組一
    heading(doc, "二、模組一：購物車訂單金額計算（calc_order_amount）", 1)
    heading(doc, "2.1 被測原始碼", 2)
    code_block(doc, CODE_CALC)
    heading(doc, "2.2 程式流程圖", 2)
    add_image(doc, os.path.join(BASE, "圖表", "圖B-1_購物車金額計算流程圖.png"), width_cm=13)
    caption(doc, "圖B-1　calc_order_amount 程式流程圖", above=False)
    heading(doc, "2.3 控制流程節點與判定", 2)
    body(doc, "本模組共有 4 個判定節點，其中 D3 為複合條件判定，包含兩個原子條件：")
    make_table(doc, ["判定", "條件式", "說明"], [
        ["D1", "member_level == 2", "是否 VIP（折扣 0.90）"],
        ["D2", "member_level == 1", "是否一般會員（折扣 0.95）"],
        ["D3", "member_level >= 1 且 subtotal >= 1000", "複合條件：C1=會員、C2=滿千 → 立減 100"],
        ["D4", "total < 0", "金額是否為負（防負歸零）"],
    ], widths=[1.6, 6.4, 7], body_size=9.5, header_size=10)
    heading(doc, "2.4 語句覆蓋測試用例", 2)
    body(doc, "下列 4 條用例使 S1～S15 之每一條可執行語句皆至少執行一次，語句覆蓋率達 100%。")
    caption(doc, "表B-1　語句覆蓋測試用例")
    make_table(doc, ["用例", "items（單價,數量）", "member", "coupon", "涵蓋語句", "預期回傳"], [
        ["TC-W01", "[(600,2)]→1200", "2", "0", "S1-S3,S5,S9,S11,S15", "980.0"],
        ["TC-W02", "[(300,1)]→300", "1", "0", "S7,S9,S12,S15", "285.0"],
        ["TC-W03", "[(100,1)]→100", "0", "0", "S8,S9,S15", "100.0"],
        ["TC-W04", "[(50,1)]→50", "1", "80", "S7,S12,S14,S15", "0"],
    ], widths=[1.8, 3.6, 1.4, 1.5, 4.2, 2.2], body_size=9, header_size=9.5)
    heading(doc, "2.5 判定覆蓋測試用例", 2)
    body(doc, "下列用例使 D1～D4 每個判定的「真」「假」分支各至少執行一次，判定覆蓋率達 100%。")
    caption(doc, "表B-2　判定覆蓋測試用例")
    make_table(doc, ["判定", "取真（T）用例", "取假（F）用例"], [
        ["D1 member==2", "TC-W01（member=2）", "TC-W02/03/04（member≠2）"],
        ["D2 member==1", "TC-W02（member=1）", "TC-W03（member=0）"],
        ["D3 會員且滿千", "TC-W01（會員且1200）", "TC-W02/03/04"],
        ["D4 total<0", "TC-W04（-32.5→0）", "TC-W01/02/03"],
    ], widths=[3.5, 5.5, 6], body_size=9.5, header_size=10)
    heading(doc, "2.6 條件覆蓋測試用例", 2)
    body(doc, "針對複合判定 D3＝(C1：member_level≥1) 且 (C2：subtotal≥1000)，設計用例使每個原子條件的真、假各出現一次，條件覆蓋率達 100%（並同時滿足判定-條件組合覆蓋）。")
    caption(doc, "表B-3　D3 條件覆蓋測試用例")
    make_table(doc, ["用例", "items→subtotal", "member", "C1:≥1會員", "C2:≥1000", "D3 結果", "預期回傳"], [
        ["TC-W01", "[(600,2)]→1200", "2", "T", "T", "T（立減）", "980.0"],
        ["TC-W02", "[(300,1)]→300", "1", "T", "F", "F", "285.0"],
        ["TC-W05", "[(800,2)]→1600", "0", "F", "T", "F", "1600.0"],
        ["TC-W03", "[(100,1)]→100", "0", "F", "F", "F", "100.0"],
    ], widths=[1.7, 3.3, 1.3, 2, 2, 2.4, 2.1], body_size=9, header_size=9)

    # 三、模組二
    heading(doc, "三、模組二：商品價格冒泡排序（bubble_sort_by_price）", 1)
    heading(doc, "3.1 被測原始碼", 2)
    code_block(doc, CODE_SORT)
    heading(doc, "3.2 程式流程圖", 2)
    add_image(doc, os.path.join(BASE, "圖表", "圖B-2_商品排序冒泡流程圖.png"), width_cm=14)
    caption(doc, "圖B-2　bubble_sort_by_price 程式流程圖", above=False)
    heading(doc, "3.3 語句與判定覆蓋測試用例", 2)
    body(doc, "本模組含 4 個判定：DB1（外層 i<n-1）、DB2（內層 j<n-1-i）、DB3（相鄰價格比較）、DB4（本趟未交換則 break）。下列用例使全部語句執行一次、且各判定真假分支皆覆蓋。")
    caption(doc, "表B-4　語句／判定覆蓋測試用例")
    make_table(doc, ["用例", "輸入（名稱,價格）", "涵蓋重點", "DB1", "DB2", "DB3", "DB4", "預期輸出（價格序）"], [
        ["TC-S01", "[(A,30),(B,20),(C,10)]（反序）", "多次交換，走完全部趟次", "T/F", "T/F", "T/F", "F", "10,20,30"],
        ["TC-S02", "[(A,10),(B,20),(C,30)]（已序）", "首趟無交換→break 提前結束", "T", "T/F", "F", "T", "10,20,30"],
        ["TC-S03", "[(A,5)]（單一元素）", "外層迴圈零次，直接 return", "F", "—", "—", "—", "5"],
    ], widths=[1.6, 4.6, 4, 1.2, 1.2, 1.2, 1.2, 3], body_size=8.5, header_size=8.5)
    body(doc, "綜合 TC-S01～S03：語句 B1～B8 全部覆蓋（B6 由 S01、B7 break 由 S02），DB1～DB4 之真假分支皆覆蓋，語句與判定覆蓋率均達 100%。", size=11)
    heading(doc, "3.4 邊界值與迴圈覆蓋", 2)
    body(doc, "排序屬迴圈密集邏輯，另設計邊界與迴圈覆蓋用例（零次、一次、典型多次、相等元素），驗證邊界健壯性。")
    caption(doc, "表B-5　邊界與迴圈覆蓋測試用例")
    make_table(doc, ["用例", "輸入", "覆蓋類型", "預期輸出"], [
        ["TC-S04", "[]（空串列）", "迴圈執行 0 次（n=0）", "[]（不崩潰）"],
        ["TC-S05", "[(A,5)]（1 元素）", "外層迴圈 0 次", "[(A,5)]"],
        ["TC-S06", "[(A,20),(B,10)]（2 元素）", "迴圈最小有效次數，1 次交換", "10,20"],
        ["TC-S07", "[(A,10),(B,10),(C,5)]（含相等）", "DB3 取「等於」邊界（>為假，不交換）", "5,10,10（穩定）"],
        ["TC-S08", "[(A,30),(B,20),(C,10)]（完全反序）", "迴圈最多次數、最多交換", "10,20,30"],
    ], widths=[1.8, 5.4, 4.5, 3], body_size=9, header_size=9.5)

    # 四、覆蓋率匯總與結論
    heading(doc, "四、覆蓋率匯總與結論", 1)
    caption(doc, "表B-6　白盒測試覆蓋率匯總")
    make_table(doc, ["被測模組", "判定數", "語句覆蓋", "判定覆蓋", "條件覆蓋", "用例數"], [
        ["calc_order_amount", "4", "100%", "100%", "100%", "5（W01-W05）"],
        ["bubble_sort_by_price", "4", "100%", "100%", "—（無複合條件）", "8（S01-S08）"],
    ], widths=[5, 1.8, 2.2, 2.2, 2.6, 2.4], body_size=9.5, header_size=9.5)
    heading(doc, "4.1 結論", 2)
    body(doc, "（1）透過繪製程式流程圖釐清兩個核心模組的控制流程後，依語句、判定、條件三種覆蓋準則設計測試用例，兩模組之語句覆蓋與判定覆蓋率均達 100%；對含複合條件的判定 D3 另以條件覆蓋驗證，亦達 100%。")
    body(doc, "（2）白盒測試補足了黑盒測試難以觸及的內部分支：例如 calc_order_amount 中「會員且滿千」之複合條件、防負歸零分支，以及冒泡排序「本趟未交換即提前結束」之最佳化分支，均經由結構分析設計出對應用例予以覆蓋。")
    body(doc, "（3）建議：可進一步引入路徑覆蓋與條件組合覆蓋以提高強度，並以 coverage.py 等工具於 CI 流程中自動量測實際覆蓋率，使結構測試結果可持續追蹤。")
    body(doc, "本白盒測試與功能（黑盒）、API、效能測試相互補充，共同構成本次《軟體測試》大作業之完整測試體系。")

    out = os.path.join(BASE, "白盒測試報告.docx")
    doc.save(out)
    print("已產生:", out)


if __name__ == "__main__":
    build()
