# selenium 
  
  
from selenium import webdriver 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
  
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = False 

#testcase 1 -- check of blank input notification
browser1 = webdriver.Firefox(capabilities=cap,executable_path=r'C:\Users\LENOVO\Desktop\geckodriver.exe') 
browser1.get("http://localhost:5000/home")
browser1.find_element_by_name("login").click()
browser1.quit()

#testcase 2 -- check if login functionality is working properly
browser5 = webdriver.Firefox(capabilities=cap,executable_path=r'C:\Users\LENOVO\Desktop\geckodriver.exe') 
browser5.get("http://localhost:5000/home")
browser5.find_element_by_name("user").send_keys("admin")
browser5.find_element_by_name("password").send_keys("admin")
browser5.find_element_by_name("login").click()

#testcase 3 --  check if app is rendered as expected.
browser2 = webdriver.Firefox(capabilities=cap,executable_path=r'C:\Users\LENOVO\Desktop\geckodriver.exe') 
browser2.get("http://localhost:5000/")
#browser.quit()

#testcase 4  -- check if book search functionality is working properly
browser3 = webdriver.Firefox(capabilities=cap,executable_path=r'C:\Users\LENOVO\Desktop\geckodriver.exe') 
browser3.get("http://localhost:5000/")
browser3.find_element_by_name("searchBook").send_keys("to kill a mocking bird")
browser3.find_element_by_name("goBook").click()
#browser.quit()

#testcase 5 -- check is book checkin is working properly
browser4 = webdriver.Firefox(capabilities=cap,executable_path=r'C:\Users\LENOVO\Desktop\geckodriver.exe') 
browser4.get("http://localhost:5000/")
browser.find_element_by_name("search").send_keys("to kill a mocking bird")
browser.find_element_by_name("go").click()