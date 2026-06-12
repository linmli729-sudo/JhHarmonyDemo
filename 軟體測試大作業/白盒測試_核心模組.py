# -*- coding: utf-8 -*-
"""白盒測試對象：核心邏輯模組（供白盒測試與覆蓋率分析使用）。

模組一 calc_order_amount：購物車訂單金額計算
  規則：小計 = Σ(單價×數量)
        會員折扣：VIP(2)→0.90、會員(1)→0.95、普通(0)→1.0
        滿額立減：會員(等級≥1) 且 小計≥1000 → 再減 100
        優惠券：total -= coupon
        防負：total<0 → total=0
模組二 bubble_sort_by_price：商品依價格升序排序（冒泡排序，含提前結束旗標）
"""


def calc_order_amount(items, member_level, coupon=0):
    """items: [(price, qty), ...]；member_level: 0/1/2；coupon: 優惠券面額。"""
    subtotal = 0
    for price, qty in items:                 # S3 迴圈累加
        subtotal += price * qty
    if member_level == 2:                    # D1
        discount = 0.90                      # S5
    elif member_level == 1:                  # D2
        discount = 0.95                      # S7
    else:
        discount = 1.0                       # S8
    total = subtotal * discount              # S9
    if member_level >= 1 and subtotal >= 1000:   # D3（複合條件 C1 且 C2）
        total -= 100                         # S11
    total -= coupon                          # S12
    if total < 0:                            # D4
        total = 0                            # S14
    return round(total, 2)                   # S15


def bubble_sort_by_price(products):
    """products: [(name, price), ...]，回傳依 price 升序排序後的新串列。"""
    arr = list(products)
    n = len(arr)
    for i in range(n - 1):                   # 外層迴圈
        swapped = False
        for j in range(n - 1 - i):           # 內層迴圈
            if arr[j][1] > arr[j + 1][1]:    # 比較相鄰兩商品價格
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:                      # 本趟未交換 → 已有序，提前結束
            break
    return arr


if __name__ == "__main__":
    # 對應報告中的語句/判定/條件覆蓋測試用例（可直接執行驗證）
    print("calc_order_amount 範例：")
    print(" TC-W01:", calc_order_amount([(600, 2)], 2, 0), "（期望 980.0）")
    print(" TC-W02:", calc_order_amount([(300, 1)], 1, 0), "（期望 285.0）")
    print(" TC-W03:", calc_order_amount([(100, 1)], 0, 0), "（期望 100.0）")
    print(" TC-W04:", calc_order_amount([(50, 1)], 1, 80), "（期望 0）")
    print(" TC-W05:", calc_order_amount([(800, 2)], 0, 0), "（期望 1600.0，C1=F,C2=T）")
    print("bubble_sort_by_price 範例：")
    print(" 反序:", bubble_sort_by_price([("A", 30), ("B", 20), ("C", 10)]))
    print(" 已序:", bubble_sort_by_price([("A", 10), ("B", 20), ("C", 30)]))
    print(" 單一:", bubble_sort_by_price([("A", 5)]))
