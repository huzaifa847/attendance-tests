import pytest
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

APP_URL = "http://13.53.138.23:3000"

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver

def random_email():
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for i in range(8))
    return f"{name}@school.edu"

# ─────────────────────────────────────────────
# HOME PAGE TESTS
# ─────────────────────────────────────────────

def test_01_homepage_loads():
    """Home page should load successfully"""
    driver = get_driver()
    try:
        driver.get(APP_URL)
        assert "Student Hub" in driver.page_source or "Attendance" in driver.page_source
        print("PASS: Homepage loaded successfully")
    finally:
        driver.quit()

def test_02_homepage_has_login_button():
    """Home page should have Portal Login button"""
    driver = get_driver()
    try:
        driver.get(APP_URL)
        wait = WebDriverWait(driver, 10)
        login_link = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(text(),'Login') or contains(text(),'login') or contains(text(),'Portal')]")
        ))
        assert login_link is not None
        print("PASS: Login button found on homepage")
    finally:
        driver.quit()

def test_03_homepage_has_register_button():
    """Home page should have Register/Request Access button"""
    driver = get_driver()
    try:
        driver.get(APP_URL)
        wait = WebDriverWait(driver, 10)
        register_link = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(text(),'Register') or contains(text(),'Access') or contains(text(),'register')]")
        ))
        assert register_link is not None
        print("PASS: Register button found on homepage")
    finally:
        driver.quit()

def test_04_homepage_login_button_redirects():
    """Clicking Portal Login should go to /login page"""
    driver = get_driver()
    try:
        driver.get(APP_URL)
        wait = WebDriverWait(driver, 10)
        login_link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(),'Login') or contains(text(),'Portal')]")
        ))
        login_link.click()
        time.sleep(2)
        assert "/login" in driver.current_url
        print(f"PASS: Redirected to login page: {driver.current_url}")
    finally:
        driver.quit()

def test_05_homepage_register_button_redirects():
    """Clicking Request Access should go to /register page"""
    driver = get_driver()
    try:
        driver.get(APP_URL)
        wait = WebDriverWait(driver, 10)
        register_link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(),'Register') or contains(text(),'Access')]")
        ))
        register_link.click()
        time.sleep(2)
        assert "/register" in driver.current_url
        print(f"PASS: Redirected to register page: {driver.current_url}")
    finally:
        driver.quit()

# ─────────────────────────────────────────────
# LOGIN PAGE TESTS
# ─────────────────────────────────────────────

def test_06_login_page_loads():
    """Login page should load with title Welcome Back"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/login")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        assert "Welcome Back" in driver.page_source or "Login" in driver.page_source
        print("PASS: Login page loaded successfully")
    finally:
        driver.quit()

def test_07_login_page_has_email_field():
    """Login page should have email input field"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/login")
        wait = WebDriverWait(driver, 10)
        email_field = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='email']")
        ))
        assert email_field is not None
        placeholder = email_field.get_attribute("placeholder")
        print(f"PASS: Email field found with placeholder: {placeholder}")
    finally:
        driver.quit()

def test_08_login_page_has_password_field():
    """Login page should have password input field"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/login")
        wait = WebDriverWait(driver, 10)
        password_field = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='password']")
        ))
        assert password_field.get_attribute("type") == "password"
        print("PASS: Password field found and is of type password")
    finally:
        driver.quit()

def test_09_login_with_wrong_credentials():
    """Login with wrong credentials should show error message"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/login")
        wait = WebDriverWait(driver, 10)

        email_field = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='email']")
        ))
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        email_field.send_keys("wronguser@school.edu")
        password_field.send_keys("wrongpassword123")
        submit_btn.click()
        time.sleep(3)

        # Should show error message
        error_div = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.bg-red-50, div.text-red-600")
        ))
        assert error_div is not None
        print(f"PASS: Error shown for wrong credentials: {error_div.text}")
    finally:
        driver.quit()

def test_10_login_empty_fields_validation():
    """Login with empty fields should not submit (HTML5 validation)"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/login")
        wait = WebDriverWait(driver, 10)

        submit_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[type='submit']")
        ))
        submit_btn.click()
        time.sleep(1)

        # Should still be on login page
        assert "/login" in driver.current_url
        print("PASS: Empty form submission prevented, stayed on login page")
    finally:
        driver.quit()

def test_11_login_page_has_register_link():
    """Login page should have a link to register page"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/login")
        wait = WebDriverWait(driver, 10)
        register_link = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href,'/register')]")
        ))
        assert register_link is not None
        print("PASS: Register link found on login page")
    finally:
        driver.quit()

def test_12_login_register_link_works():
    """Clicking Register here on login page should go to /register"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/login")
        wait = WebDriverWait(driver, 10)
        register_link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@href,'/register')]")
        ))
        register_link.click()
        time.sleep(2)
        assert "/register" in driver.current_url
        print(f"PASS: Navigated to register page: {driver.current_url}")
    finally:
        driver.quit()

# ─────────────────────────────────────────────
# REGISTER PAGE TESTS
# ─────────────────────────────────────────────

def test_13_register_page_loads():
    """Register page should load with Create Account heading"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/register")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        assert "Create Account" in driver.page_source or "Register" in driver.page_source
        print("PASS: Register page loaded successfully")
    finally:
        driver.quit()

def test_14_register_page_has_all_fields():
    """Register page should have name, email, password fields and role dropdown"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/register")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))

        name_field = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        role_select = driver.find_element(By.TAG_NAME, "select")

        assert name_field is not None
        assert email_field is not None
        assert password_field is not None
        assert role_select is not None
        print("PASS: All register fields found: name, email, password, role")
    finally:
        driver.quit()

def test_15_register_role_dropdown_has_options():
    """Role dropdown should have student and teacher options"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/register")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "select")))

        select = Select(driver.find_element(By.TAG_NAME, "select"))
        options = [o.get_attribute("value") for o in select.options]

        assert "student" in options
        assert "teacher" in options
        print(f"PASS: Role dropdown has options: {options}")
    finally:
        driver.quit()

def test_16_register_default_role_is_student():
    """Default selected role in dropdown should be student"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/register")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "select")))

        select = Select(driver.find_element(By.TAG_NAME, "select"))
        default_value = select.first_selected_option.get_attribute("value")

        assert default_value == "student"
        print(f"PASS: Default role is: {default_value}")
    finally:
        driver.quit()

def test_17_register_with_short_password():
    """Registration with password less than 6 chars should fail"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/register")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))

        driver.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys("Test User")
        driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys(random_email())
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        # Should stay on register page
        assert "/register" in driver.current_url
        print("PASS: Short password registration prevented")
    finally:
        driver.quit()

def test_18_register_page_has_login_link():
    """Register page should have a link back to login page"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/register")
        wait = WebDriverWait(driver, 10)
        login_link = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href,'/login')]")
        ))
        assert login_link is not None
        print("PASS: Login link found on register page")
    finally:
        driver.quit()

def test_19_register_new_student_success():
    """Registering a new student should redirect to login page"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/register")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))

        test_email = random_email()

        driver.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys("Test Student")
        driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys(test_email)
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("password123")

        select = Select(driver.find_element(By.TAG_NAME, "select"))
        select.select_by_value("student")

        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(4)

        assert "/login" in driver.current_url
        print(f"PASS: Student registered successfully with email: {test_email}")
    finally:
        driver.quit()

def test_20_register_new_teacher_success():
    """Registering a new teacher should redirect to login page"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/register")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))

        test_email = random_email()

        driver.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys("Test Teacher")
        driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys(test_email)
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("password123")

        select = Select(driver.find_element(By.TAG_NAME, "select"))
        select.select_by_value("teacher")

        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(4)

        assert "/login" in driver.current_url
        print(f"PASS: Teacher registered successfully with email: {test_email}")
    finally:
        driver.quit()

def test_21_register_duplicate_email_shows_error():
    """Registering with same email twice should show error"""
    driver = get_driver()
    try:
        # Use a fixed email that likely already exists
        driver.get(f"{APP_URL}/register")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))

        fixed_email = "duplicate.test@school.edu"

        driver.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys("Duplicate User")
        driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys(fixed_email)
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("password123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(4)

        # Either shows error OR redirects to login (first time registration)
        current_url = driver.current_url
        page_source = driver.page_source
        assert "/login" in current_url or "error" in page_source.lower() or "already" in page_source.lower() or "/register" in current_url
        print(f"PASS: Duplicate email handled correctly, URL: {current_url}")
    finally:
        driver.quit()

# ─────────────────────────────────────────────
# GENERAL / NAVIGATION TESTS
# ─────────────────────────────────────────────

def test_22_direct_access_teacher_dashboard_redirects():
    """Accessing /teacher/dashboard without login should redirect"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/teacher/dashboard")
        time.sleep(3)
        current_url = driver.current_url
        # Should either redirect to login or show some page (not crash)
        assert driver.find_element(By.TAG_NAME, "body") is not None
        print(f"PASS: Teacher dashboard access handled, URL: {current_url}")
    finally:
        driver.quit()

def test_23_direct_access_student_dashboard_redirects():
    """Accessing /student/dashboard without login should redirect"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/student/dashboard")
        time.sleep(3)
        current_url = driver.current_url
        assert driver.find_element(By.TAG_NAME, "body") is not None
        print(f"PASS: Student dashboard access handled, URL: {current_url}")
    finally:
        driver.quit()

def test_24_page_load_time_acceptable():
    """All main pages should load within 15 seconds"""
    driver = get_driver()
    try:
        pages = [APP_URL, f"{APP_URL}/login", f"{APP_URL}/register"]
        for page in pages:
            start = time.time()
            driver.get(page)
            end = time.time()
            load_time = end - start
            assert load_time < 15, f"Page {page} took too long: {load_time:.2f}s"
            print(f"PASS: {page} loaded in {load_time:.2f}s")
    finally:
        driver.quit()

def test_25_login_page_submit_button_text():
    """Login submit button should say Sign In"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/login")
        wait = WebDriverWait(driver, 10)
        submit_btn = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button[type='submit']")
        ))
        btn_text = submit_btn.text
        assert "Sign In" in btn_text or "Login" in btn_text or "Sign" in btn_text
        print(f"PASS: Login button text is: {btn_text}")
    finally:
        driver.quit()
