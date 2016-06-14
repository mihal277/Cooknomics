from selenium import webdriver

driver = webdriver.Firefox()
# wait = WebDriverWait(driver, 3)
driver.get("http://localhost:8000/partners/")
assert "Partners" in driver.title
elem = driver.find_element_by_class_name("app_title")
assert "PARTNERS" in elem.text
driver.close()
