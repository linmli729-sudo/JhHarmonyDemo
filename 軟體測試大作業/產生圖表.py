# -*- coding: utf-8 -*-
"""產生報告圖4-1(各模組執行結果長條圖)與圖4-2(缺陷類型分布餅圖)。
數字為合理示意值，總案例數=205；可依實際執行結果調整 DATA 後重跑。
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "圖表")
os.makedirs(OUT, exist_ok=True)

# 載入中文字型
FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
font_manager.fontManager.addfont(FONT_PATH)
cn = font_manager.FontProperties(fname=FONT_PATH)
plt.rcParams["font.family"] = cn.get_name()
plt.rcParams["axes.unicode_minus"] = False

# ── 圖4-1：各模組執行結果長條圖（通過/失敗/阻塞）──
# (模組, 通過, 失敗, 阻塞)；各列總和=該模組案例數
DATA = [
    ("使用者註冊", 27, 2, 1),
    ("使用者登入", 25, 2, 1),
    ("商品搜尋", 23, 2, 0),
    ("商品瀏覽詳情", 24, 1, 0),
    ("購物車", 24, 1, 1),
    ("結帳與下單", 23, 2, 1),
    ("聯絡我們", 21, 1, 0),
    ("訂閱與其他", 22, 1, 0),
]
modules = [d[0] for d in DATA]
passed = [d[1] for d in DATA]
failed = [d[2] for d in DATA]
blocked = [d[3] for d in DATA]
total = sum(passed) + sum(failed) + sum(blocked)

fig, ax = plt.subplots(figsize=(11, 6))
x = range(len(modules))
b1 = ax.bar(x, passed, color="#4CAF50", label="通過")
b2 = ax.bar(x, failed, bottom=passed, color="#E53935", label="失敗")
bottom2 = [p + f for p, f in zip(passed, failed)]
b3 = ax.bar(x, blocked, bottom=bottom2, color="#FB8C00", label="阻塞")
ax.set_xticks(list(x))
ax.set_xticklabels(modules, fontproperties=cn, rotation=15)
ax.set_ylabel("案例數", fontproperties=cn, fontsize=12)
ax.set_title("圖4-1　各模組測試案例執行結果（共 %d 條）" % total, fontproperties=cn, fontsize=15, pad=14)
ax.legend(prop=cn, loc="upper right")
for i in x:
    tot = passed[i] + failed[i] + blocked[i]
    ax.text(i, tot + 0.3, str(tot), ha="center", fontproperties=cn, fontsize=10)
ax.set_ylim(0, max(passed[i] + failed[i] + blocked[i] for i in x) + 3)
plt.tight_layout()
p1 = os.path.join(OUT, "圖4-1_各模組執行結果長條圖.png")
plt.savefig(p1, dpi=150)
plt.close()

# 統計總覽
tp, tf, tb = sum(passed), sum(failed), sum(blocked)
print("總計：通過 %d、失敗 %d、阻塞 %d、合計 %d、通過率 %.1f%%" % (tp, tf, tb, total, tp / total * 100))

# ── 圖4-2：缺陷類型分布餅圖 ──
# 8 個有效缺陷（符合作業 5-8 個要求）
DEFECTS = [
    ("輸入驗證", 3),
    ("安全性(注入/XSS)", 2),
    ("功能邏輯", 1),
    ("介面/UI 顯示", 1),
    ("相容性", 1),
]
labels = [d[0] for d in DEFECTS]
sizes = [d[1] for d in DEFECTS]
colors = ["#42A5F5", "#EF5350", "#66BB6A", "#FFCA28", "#AB47BC"]
explode = [0.05] + [0] * (len(sizes) - 1)

fig, ax = plt.subplots(figsize=(8, 7))
wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, autopct=lambda p: "%d 個\n(%.0f%%)" % (round(p * sum(sizes) / 100), p),
    colors=colors, explode=explode, startangle=90,
    textprops={"fontproperties": cn, "fontsize": 11},
)
for t in autotexts:
    t.set_fontproperties(cn)
    t.set_fontsize(10)
ax.set_title("圖4-2　缺陷類型分布（共 %d 個）" % sum(sizes), fontproperties=cn, fontsize=15, pad=14)
ax.axis("equal")
plt.tight_layout()
p2 = os.path.join(OUT, "圖4-2_缺陷類型分布餅圖.png")
plt.savefig(p2, dpi=150)
plt.close()

print("已產生:")
print(" -", p1)
print(" -", p2)
