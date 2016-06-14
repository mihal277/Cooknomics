from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://localhost:8000/recipes/")
assert "Recipes" in driver.title
elem = driver.find_element_by_class_name("app_title")
assert "RECIPES" in elem.text
elem = driver.find_element_by_id("search-button")
assert "Wyszukaj" in elem.text
elem = driver.find_element_by_link_text('Banan').click()

driver.close()
