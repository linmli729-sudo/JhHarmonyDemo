# -*- coding: utf-8 -*-
"""產生白盒測試程式流程圖：
圖B-1 calc_order_amount（購物車金額計算）流程圖
圖B-2 bubble_sort_by_price（商品冒泡排序）流程圖
以 matplotlib 手繪流程圖元件（起止/處理/判定 + 連接箭頭）。
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
from matplotlib import font_manager

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "圖表")
os.makedirs(OUT, exist_ok=True)

FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
font_manager.fontManager.addfont(FONT_PATH)
cn = font_manager.FontProperties(fname=FONT_PATH)
plt.rcParams["font.family"] = cn.get_name()
plt.rcParams["axes.unicode_minus"] = False

EDGE = "#37474F"
C_TERM = ("#C8E6C9", "#2E7D32")   # 起止
C_PROC = ("#BBDEFB", "#1565C0")   # 處理
C_DEC = ("#FFE0B2", "#E65100")    # 判定

PW, PH = 3.4, 0.95   # process size
DW, DH = 3.6, 1.5    # decision size
TW, TH = 2.4, 0.9    # terminal size


def terminal(ax, x, y, text):
    p = FancyBboxPatch((x - TW / 2, y - TH / 2), TW, TH,
                       boxstyle="round,pad=0.02,rounding_size=0.45",
                       fc=C_TERM[0], ec=C_TERM[1], lw=1.6, zorder=2)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontproperties=cn, fontsize=11, zorder=3)


def process(ax, x, y, text):
    p = FancyBboxPatch((x - PW / 2, y - PH / 2), PW, PH,
                       boxstyle="round,pad=0.02,rounding_size=0.06",
                       fc=C_PROC[0], ec=C_PROC[1], lw=1.6, zorder=2)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontproperties=cn, fontsize=10.5, zorder=3)


def decision(ax, x, y, text):
    pts = [(x, y + DH / 2), (x + DW / 2, y), (x, y - DH / 2), (x - DW / 2, y)]
    ax.add_patch(Polygon(pts, closed=True, fc=C_DEC[0], ec=C_DEC[1], lw=1.6, zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontproperties=cn, fontsize=10, zorder=3)


def path(ax, pts, label="", lx=None, ly=None):
    """折線連接，末端加箭頭。"""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs[:-1], ys[:-1], color=EDGE, lw=1.4, zorder=1)
    ax.annotate("", xy=pts[-1], xytext=pts[-2],
                arrowprops=dict(arrowstyle="-|>", lw=1.4, color=EDGE), zorder=1)
    if label:
        if lx is None:
            lx = (pts[0][0] + pts[1][0]) / 2 + 0.18
        if ly is None:
            ly = (pts[0][1] + pts[1][1]) / 2
        ax.text(lx, ly, label, fontproperties=cn, fontsize=9.5, color="#B71C1C", zorder=4)


# ───────────────────────── 圖B-1：calc_order_amount ─────────────────────────
def chart_calc():
    fig, ax = plt.subplots(figsize=(10.5, 17))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 18)
    ax.axis("off")
    cx, rx = 3.4, 8.2

    terminal(ax, cx, 17.2, "開始")
    process(ax, cx, 15.8, "subtotal = 0")
    process(ax, cx, 14.4, "走訪 items：\nsubtotal += 單價×數量")
    decision(ax, cx, 12.6, "member_level\n== 2 ?")
    process(ax, rx, 12.6, "discount = 0.90")
    decision(ax, cx, 10.6, "member_level\n== 1 ?")
    process(ax, rx, 10.6, "discount = 0.95")
    process(ax, cx, 9.0, "discount = 1.0")
    process(ax, cx, 7.5, "total =\nsubtotal × discount")
    decision(ax, cx, 5.7, "member_level≥1\n且 subtotal≥1000 ?")
    process(ax, rx, 5.7, "total -= 100")
    process(ax, cx, 4.1, "total -= coupon")
    decision(ax, cx, 2.6, "total < 0 ?")
    process(ax, rx, 2.6, "total = 0")
    process(ax, cx, 1.1, "return round(total,2)")
    terminal(ax, cx, 0.2, "結束")

    # 主幹
    path(ax, [(cx, 16.75), (cx, 16.3)])           # 開始→subtotal=0
    path(ax, [(cx, 15.33), (cx, 14.9)])           # →累加
    path(ax, [(cx, 13.93), (cx, 13.35)])          # →D1
    path(ax, [(cx, 11.85), (cx, 11.35)], "否")    # D1 no→D2
    path(ax, [(cx, 9.85), (cx, 9.48)], "否")      # D2 no→discount=1.0
    path(ax, [(cx, 8.53), (cx, 8.0)])             # discount=1.0→total
    path(ax, [(cx, 7.02), (cx, 6.45)])            # total→D3
    path(ax, [(cx, 4.95), (cx, 4.58)], "否")      # D3 no→coupon
    path(ax, [(cx, 3.63), (cx, 3.35)])            # coupon→D4
    path(ax, [(cx, 1.85), (cx, 1.58)], "否")      # D4 no→return
    path(ax, [(cx, 0.63), (cx, 0.65)])            # return→結束

    # 右側分支
    path(ax, [(cx + DW / 2, 12.6), (rx - PW / 2, 12.6)], "是")          # D1 yes→0.90
    path(ax, [(cx + DW / 2, 10.6), (rx - PW / 2, 10.6)], "是")          # D2 yes→0.95
    path(ax, [(rx, 12.13), (rx, 7.5), (cx + PW / 2, 7.5)])              # 0.90→total
    path(ax, [(rx, 10.13), (rx - 0.9, 10.13), (rx - 0.9, 7.5), (cx + PW / 2 + 0.0, 7.5)])  # 0.95→total
    path(ax, [(cx + DW / 2, 5.7), (rx - PW / 2, 5.7)], "是")            # D3 yes→-100
    path(ax, [(rx, 5.23), (rx, 4.1), (cx + PW / 2, 4.1)])               # -100→coupon
    path(ax, [(cx + DW / 2, 2.6), (rx - PW / 2, 2.6)], "是")            # D4 yes→total=0
    path(ax, [(rx, 2.13), (rx, 1.1), (cx + PW / 2, 1.1)])              # total=0→return

    ax.set_title("圖B-1　calc_order_amount（購物車訂單金額計算）程式流程圖",
                 fontproperties=cn, fontsize=14, pad=12)
    plt.tight_layout()
    p = os.path.join(OUT, "圖B-1_購物車金額計算流程圖.png")
    plt.savefig(p, dpi=150, bbox_inches="tight")
    plt.close()
    return p


# ───────────────────────── 圖B-2：bubble_sort_by_price ─────────────────────────
def chart_sort():
    fig, ax = plt.subplots(figsize=(12, 15))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 16)
    ax.axis("off")
    cx, rx = 3.6, 8.2

    terminal(ax, cx, 15.2, "開始")
    process(ax, cx, 13.9, "arr = list(products)\nn = len(arr)")
    process(ax, cx, 12.6, "i = 0")
    decision(ax, cx, 11.0, "i < n-1 ?")
    process(ax, cx, 9.3, "swapped = False\nj = 0")
    decision(ax, cx, 7.6, "j < n-1-i ?")
    decision(ax, cx, 5.6, "arr[j].price >\narr[j+1].price ?")
    process(ax, rx, 5.6, "交換 arr[j],arr[j+1]\nswapped = True")
    process(ax, cx, 3.9, "j = j + 1")
    decision(ax, rx, 9.4, "not swapped ?")
    process(ax, rx, 7.0, "i = i + 1")
    process(ax, rx, 11.0, "return arr")
    terminal(ax, 11.0, 11.0, "結束")

    # 主幹（外/內迴圈本體）
    path(ax, [(cx, 14.75), (cx, 14.4)])               # 開始→init
    path(ax, [(cx, 13.43), (cx, 13.1)])               # init→i=0
    path(ax, [(cx, 12.13), (cx, 11.75)])              # i=0→D_outer
    path(ax, [(cx, 10.25), (cx, 9.78)], "是")         # outer yes→swapped=False
    path(ax, [(cx, 8.83), (cx, 8.35)])                # →D_inner
    path(ax, [(cx, 6.85), (cx, 6.35)], "是")          # inner yes→compare
    path(ax, [(cx, 4.85), (cx, 4.38)], "否")          # compare no→j++
    # 比較為真：交換
    path(ax, [(cx + DW / 2, 5.6), (rx - PW / 2, 5.6)], "是")           # compare yes→swap
    path(ax, [(rx, 5.13), (rx, 3.9), (cx + PW / 2, 3.9)])              # swap→j++
    # j++ 回到內層判定（左側回邊）
    path(ax, [(cx - PW / 2, 3.9), (1.2, 3.9), (1.2, 7.6), (cx - DW / 2, 7.6)])

    # 外層 no → return arr → 結束
    path(ax, [(cx + DW / 2, 11.0), (rx - PW / 2, 11.0)], "否")
    path(ax, [(rx + PW / 2, 11.0), (11.0 - TW / 2, 11.0)])

    # 內層 no → not swapped?
    path(ax, [(cx + DW / 2, 7.6), (rx, 7.6), (rx, 8.65)], "否")
    # not swapped 為真（已有序）→ break → return arr
    path(ax, [(rx, 10.15), (rx, 10.53)], "是")
    # not swapped 為否 → i = i+1
    path(ax, [(rx, 8.65), (rx, 7.5)], "否")
    # i++ 回到外層判定（右側回邊）
    path(ax, [(rx - PW / 2, 7.0), (5.9, 7.0), (5.9, 11.0), (cx + DW / 2, 11.0)])

    ax.set_title("圖B-2　bubble_sort_by_price（商品冒泡排序）程式流程圖",
                 fontproperties=cn, fontsize=14, pad=12)
    plt.tight_layout()
    p = os.path.join(OUT, "圖B-2_商品排序冒泡流程圖.png")
    plt.savefig(p, dpi=150, bbox_inches="tight")
    plt.close()
    return p


if __name__ == "__main__":
    p1 = chart_calc()
    p2 = chart_sort()
    print("已產生:")
    print(" -", p1)
    print(" -", p2)
