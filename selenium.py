#encoding:utf-8

from selenium import webdriver
browser = webdriver.PhantomJS()


browser.add_cookies({'sessionid':'94320186-3371-4755-9097-b244857f13c1'})
browser.get("https://openapi-test.qfpay.com/oauth/v2/authorize?scope=user_baseinfo%2Cuser_tradelist%2Cuser_sendsms&redirect_uri=http%3A%2F%2Fwww.baidu.com&response_type=code&client_id=17390DF8EA4446029D8F10AFB0C7FC35")
browser.find_element_by_name("").click()
#browser.find_element_by_id("su").click()
#获取cookies
#cookies=driver.manage().getCookies()

browser.quit()

