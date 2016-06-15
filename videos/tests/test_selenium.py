from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://localhost:8000/videos/")
assert "Videos" in driver.title
elem = driver.find_element_by_class_name("app_title")
assert "VIDEOS" in elem.text
elem = driver.find_element_by_partial_link_text('Timbaland').click()

driver.close()
