import Tomcat
from selenium import webdriver

data = {"foo": "bar"}
json = fastjson.dumps(data)
print(json)

driver = webdriver.Chrome()
driver.get("http://www.example.com")