import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class TestAttendanceSystem:
    
    def setup_method(self):
        # Setup for Chrome (Headless mode for Jenkins/Ubuntu)
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless') # Uncomment for Jenkins
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "http://localhost:3000"

    def teardown_method(self):
        self.driver.quit()

    # --- CATEGORY 1: NAVIGATION ---
    def test_01_home_page_load(self):
        self.driver.get(self.base_url)
        assert "Student Hub" in self.driver.page_source

    def test_02_nav_to_login(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.LINK_TEXT, "Portal Login").click()
        assert "/login" in self.driver.current_url

    def test_03_nav_to_register(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.LINK_TEXT, "Request Access").click()
        assert "/register" in self.driver.current_url

    # --- CATEGORY 2: REGISTRATION ---
    def test_04_successful_student_registration(self):
        self.driver.get(f"{self.base_url}/register")
        self.driver.find_element(By.PLACEHOLDER_TEXT, "John Doe").send_keys("Test Student")
        self.driver.find_element(By.NAME, "email").send_keys(f"std_{int(time.time())}@school.edu")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        # Select Role
        role_dropdown = Select(self.driver.find_element(By.TAG_NAME, "select"))
        role_dropdown.select_by_value("student")
        
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.wait.until(EC.url_contains("/login"))
        assert "/login" in self.driver.current_url

    def test_05_teacher_role_assignment(self):
        self.driver.get(f"{self.base_url}/register")
        role_dropdown = Select(self.driver.find_element(By.TAG_NAME, "select"))
        role_dropdown.select_by_value("teacher")
        assert role_dropdown.first_selected_option.text == "Teacher"

    def test_06_password_length_error(self):
        self.driver.get(f"{self.base_url}/register")
        self.driver.find_element(By.NAME, "password").send_keys("123") # Too short
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        error = self.driver.find_element(By.CLASS_NAME, "bg-red-50")
        assert error.is_displayed()

    def test_07_empty_fields_validation(self):
        self.driver.get(f"{self.base_url}/register")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        # Verify browser stopped the click (HTML5 validation)
        assert "/register" in self.driver.current_url

    # --- CATEGORY 3: LOGIN ---
    def test_08_invalid_login_error(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.NAME, "email").send_keys("wrong@user.com")
        self.driver.find_element(By.NAME, "password").send_keys("wrongpass")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        error_msg = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "bg-red-50")))
        assert "Login failed" in error_msg.text

    def test_09_login_loading_state(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.NAME, "email").send_keys("test@test.com")
        self.driver.find_element(By.NAME, "password").send_keys("password")
        btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        btn.click()
        # Immediately check text
        assert "Signing in..." in btn.text

    def test_10_redirect_teacher_dashboard(self):
        # NOTE: Requires an existing teacher account in DB
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.NAME, "email").send_keys("teacher@school.edu")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        # Verify 404 or Page Content (Since file was missing in your logs)
        self.wait.until(EC.url_contains("/teacher/dashboard"))
        assert "/teacher/dashboard" in self.driver.current_url

    def test_11_redirect_student_dashboard(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.NAME, "email").send_keys("student@school.edu")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.wait.until(EC.url_contains("/student/dashboard"))

    # --- CATEGORY 4: UX & REDIRECTS ---
    def test_12_register_to_login_link(self):
        self.driver.get(f"{self.base_url}/register")
        self.driver.find_element(By.LINK_TEXT, "Sign in here").click()
        assert "/login" in self.driver.current_url

    def test_13_login_to_register_link(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.LINK_TEXT, "Register here").click()
        assert "/register" in self.driver.current_url

    def test_14_email_input_type(self):
        self.driver.get(f"{self.base_url}/login")
        email_input = self.driver.find_element(By.NAME, "email")
        assert email_input.get_attribute("type") == "email"

    def test_15_dark_mode_class_check(self):
        self.driver.get(self.base_url)
        main_container = self.driver.find_element(By.TAG_NAME, "main")
        # Check if the dark mode class exists in Tailwind
        assert "dark:bg-slate-900" in main_container.get_attribute("class")
