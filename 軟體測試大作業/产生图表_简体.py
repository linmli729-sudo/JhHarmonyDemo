# -*- coding: utf-8 -*-
"""产生报告图4-1(各模块执行结果柱状图)与图4-2(缺陷类型分布饼图) —— 简体中文版。
数字为合理示意值，总案例数=205；可依实际执行结果调整 DATA 后重跑。
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "图表_简体")
os.makedirs(OUT, exist_ok=True)

FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
font_manager.fontManager.addfont(FONT_PATH)
cn = font_manager.FontProperties(fname=FONT_PATH)
plt.rcParams["font.family"] = cn.get_name()
plt.rcParams["axes.unicode_minus"] = False

# ── 图4-1：各模块执行结果柱状图（通过/失败/阻塞）──
DATA = [
    ("用户注册", 27, 2, 1),
    ("用户登录", 25, 2, 1),
    ("商品搜索", 23, 2, 0),
    ("商品浏览详情", 24, 1, 0),
    ("购物车", 24, 1, 1),
    ("结账与下单", 23, 2, 1),
    ("联系我们", 21, 1, 0),
    ("订阅与其他", 22, 1, 0),
]
modules = [d[0] for d in DATA]
passed = [d[1] for d in DATA]
failed = [d[2] for d in DATA]
blocked = [d[3] for d in DATA]
total = sum(passed) + sum(failed) + sum(blocked)

fig, ax = plt.subplots(figsize=(11, 6))
x = range(len(modules))
b1 = ax.bar(x, passed, color="#4CAF50", label="通过")
b2 = ax.bar(x, failed, bottom=passed, color="#E53935", label="失败")
bottom2 = [p + f for p, f in zip(passed, failed)]
b3 = ax.bar(x, blocked, bottom=bottom2, color="#FB8C00", label="阻塞")
ax.set_xticks(list(x))
ax.set_xticklabels(modules, fontproperties=cn, rotation=15)
ax.set_ylabel("案例数", fontproperties=cn, fontsize=12)
ax.set_title("图4-1  各模块测试案例执行结果（共 %d 条）" % total, fontproperties=cn, fontsize=15, pad=14)
ax.legend(prop=cn, loc="upper right")
for i in x:
    tot = passed[i] + failed[i] + blocked[i]
    ax.text(i, tot + 0.3, str(tot), ha="center", fontproperties=cn, fontsize=10)
ax.set_ylim(0, max(passed[i] + failed[i] + blocked[i] for i in x) + 3)
plt.tight_layout()
p1 = os.path.join(OUT, "图4-1_各模块执行结果柱状图.png")
plt.savefig(p1, dpi=150)
plt.close()

tp, tf, tb = sum(passed), sum(failed), sum(blocked)
print("总计：通过 %d、失败 %d、阻塞 %d、合计 %d、通过率 %.1f%%" % (tp, tf, tb, total, tp / total * 100))

# ── 图4-2：缺陷类型分布饼图 ──
DEFECTS = [
    ("输入验证", 3),
    ("安全性(注入/XSS)", 2),
    ("功能逻辑", 1),
    ("界面/UI 显示", 1),
    ("兼容性", 1),
]
labels = [d[0] for d in DEFECTS]
sizes = [d[1] for d in DEFECTS]
colors = ["#42A5F5", "#EF5350", "#66BB6A", "#FFCA28", "#AB47BC"]
explode = [0.05] + [0] * (len(sizes) - 1)

fig, ax = plt.subplots(figsize=(8, 7))
wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, autopct=lambda p: "%d 个\n(%.0f%%)" % (round(p * sum(sizes) / 100), p),
    colors=colors, explode=explode, startangle=90,
    textprops={"fontproperties": cn, "fontsize": 11},
)
for t in autotexts:
    t.set_fontproperties(cn)
    t.set_fontsize(10)
ax.set_title("图4-2  缺陷类型分布（共 %d 个）" % sum(sizes), fontproperties=cn, fontsize=15, pad=14)
ax.axis("equal")
plt.tight_layout()
p2 = os.path.join(OUT, "图4-2_缺陷类型分布饼图.png")
plt.savefig(p2, dpi=150)
plt.close()

print("已产生:")
print(" -", p1)
print(" -", p2)
