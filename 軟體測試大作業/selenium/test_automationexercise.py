# -*- coding: utf-8 -*-
"""Automation Exercise 瀏覽器功能自動化測試（Selenium 4 + pytest）。

對應報告 3.1 功能模組的可自動化關鍵流程：註冊、登入、搜尋、購物車、聯絡我們、訂閱。
每個測試結束會自動截圖到 screenshots/，可直接放進報告。

執行：
    pip install -r requirements.txt
    pytest -v                      # 有頭(看得到瀏覽器)
    HEADLESS=1 pytest -v           # 無頭(CI/伺服器)
備註：Selenium 4.6+ 內建 Selenium Manager 會自動下載對應的 chromedriver，免額外安裝。
"""
import os
import time
import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://automationexercise.com"
SHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
os.makedirs(SHOT_DIR, exist_ok=True)


def shot(driver, name):
    ts = datetime.datetime.now().strftime("%H%M%S")
    path = os.path.join(SHOT_DIR, f"{name}_{ts}.png")
    driver.save_screenshot(path)
    print(f"[screenshot] {path}")
    return path


@pytest.fixture()
def driver():
    opts = Options()
    if os.environ.get("HEADLESS") == "1":
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1366,900")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-notifications")
    d = webdriver.Chrome(options=opts)
    d.implicitly_wait(8)
    yield d
    d.quit()


def wait(driver, locator, timeout=15):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))


def click(driver, locator, timeout=15):
    el = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    try:
        el.click()
    except Exception:
        driver.execute_script("arguments[0].click();", el)
    return el


def unique_email():
    return f"qa_{int(time.time()*1000)}@example.com"


# ── TC: 註冊新帳號（含登入驗證 + 刪除帳號清理） ──
def test_register_new_user(driver):
    email = unique_email()
    name = "QA Tester"
    driver.get(BASE_URL + "/login")
    wait(driver, (By.CSS_SELECTOR, "[data-qa='signup-name']")).send_keys(name)
    driver.find_element(By.CSS_SELECTOR, "[data-qa='signup-email']").send_keys(email)
    click(driver, (By.CSS_SELECTOR, "[data-qa='signup-button']"))

    wait(driver, (By.ID, "id_gender1")).click()
    driver.find_element(By.ID, "password").send_keys("Test@12345")
    from selenium.webdriver.support.ui import Select
    Select(driver.find_element(By.ID, "days")).select_by_value("10")
    Select(driver.find_element(By.ID, "months")).select_by_value("5")
    Select(driver.find_element(By.ID, "years")).select_by_value("1995")
    driver.find_element(By.ID, "first_name").send_keys("QA")
    driver.find_element(By.ID, "last_name").send_keys("Tester")
    driver.find_element(By.ID, "address1").send_keys("123 Test Street")
    Select(driver.find_element(By.ID, "country")).select_by_visible_text("United States")
    driver.find_element(By.ID, "state").send_keys("California")
    driver.find_element(By.ID, "city").send_keys("Los Angeles")
    driver.find_element(By.ID, "zipcode").send_keys("12345")
    driver.find_element(By.ID, "mobile_number").send_keys("1234567890")
    click(driver, (By.CSS_SELECTOR, "[data-qa='create-account']"))

    msg = wait(driver, (By.CSS_SELECTOR, "[data-qa='account-created'], h2.title")).text
    shot(driver, "TC_register_account_created")
    assert "Account Created" in msg or "ACCOUNT CREATED" in msg.upper()

    click(driver, (By.CSS_SELECTOR, "[data-qa='continue-button']"))
    assert "Logged in as" in driver.find_element(By.TAG_NAME, "body").text

    # 清理：刪除帳號
    click(driver, (By.LINK_TEXT, "Delete Account"))
    wait(driver, (By.CSS_SELECTOR, "[data-qa='account-deleted'], h2.title"))
    shot(driver, "TC_register_account_deleted")


# ── TC-031: 有效登入 / TC-032: 無效登入 ──
def test_login_invalid(driver):
    driver.get(BASE_URL + "/login")
    wait(driver, (By.CSS_SELECTOR, "[data-qa='login-email']")).send_keys("nobody_unknown_999@example.com")
    driver.find_element(By.CSS_SELECTOR, "[data-qa='login-password']").send_keys("wrongpassword")
    click(driver, (By.CSS_SELECTOR, "[data-qa='login-button']"))
    err = wait(driver, (By.CSS_SELECTOR, "form[action='/login'] p")).text
    shot(driver, "TC032_login_invalid")
    assert "incorrect" in err.lower()


# ── TC-059: 搜尋商品 ──
def test_search_product(driver):
    driver.get(BASE_URL + "/products")
    wait(driver, (By.ID, "search_product")).send_keys("top")
    click(driver, (By.ID, "submit_search"))
    title = wait(driver, (By.XPATH, "//h2[contains(.,'Searched Products')]")).text
    products = driver.find_elements(By.CSS_SELECTOR, ".features_items .product-image-wrapper")
    shot(driver, "TC059_search_top")
    assert "Searched Products" in title
    assert len(products) > 0


# ── TC-109: 加入購物車 ──
def test_add_to_cart(driver):
    driver.get(BASE_URL + "/products")
    first = wait(driver, (By.CSS_SELECTOR, ".features_items .product-image-wrapper"))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first)
    add_btn = first.find_element(By.CSS_SELECTOR, "a.add-to-cart")
    driver.execute_script("arguments[0].click();", add_btn)
    click(driver, (By.XPATH, "//u[contains(.,'View Cart')] | //a[contains(.,'View Cart')]"))
    rows = wait(driver, (By.CSS_SELECTOR, "#cart_info_table tbody tr"))
    shot(driver, "TC109_add_to_cart")
    assert rows is not None


# ── TC-161: 聯絡我們表單 ──
def test_contact_us(driver):
    driver.get(BASE_URL + "/contact_us")
    wait(driver, (By.CSS_SELECTOR, "[data-qa='name']")).send_keys("QA Tester")
    driver.find_element(By.CSS_SELECTOR, "[data-qa='email']").send_keys(unique_email())
    driver.find_element(By.CSS_SELECTOR, "[data-qa='subject']").send_keys("Test Subject")
    driver.find_element(By.CSS_SELECTOR, "[data-qa='message']").send_keys("This is an automated test message.")
    click(driver, (By.CSS_SELECTOR, "[data-qa='submit-button']"))
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
    except Exception:
        pass
    success = wait(driver, (By.CSS_SELECTOR, ".status.alert.alert-success, .contact-form .status")).text
    shot(driver, "TC161_contact_us")
    assert "success" in success.lower() or "submitted" in success.lower()


# ── TC-183: 頁尾電子報訂閱 ──
def test_subscription(driver):
    driver.get(BASE_URL)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait(driver, (By.ID, "susbscribe_email")).send_keys(unique_email())
    click(driver, (By.ID, "subscribe"))
    msg = wait(driver, (By.CSS_SELECTOR, "#success-subscribe .alert-success, .alert-success")).text
    shot(driver, "TC183_subscription")
    assert "subscribed" in msg.lower()
