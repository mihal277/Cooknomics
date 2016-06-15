from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://localhost:8000/news/")
assert "News" in driver.title
elem = driver.find_element_by_class_name("app_title")
assert "NEWS" in elem.text
elem = driver.find_element_by_class_name("filter-option")
assert "Sortuj po:" in elem.text

driver.close()
