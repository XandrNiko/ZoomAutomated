import time
from get_chrome_driver import GetChromeDriver
from selenium import webdriver
from selenium.webdriver.common.by import By

INTERVAL = 3.0
NUMBER = 0

def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    get_driver = GetChromeDriver()
    get_driver.install()
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://zoom.us/join")
    driver.implicitly_wait(10)
    return driver


def join_to_session(meet_code, pass_code, user_name, driver: webdriver.Chrome):
    input_element = driver.find_element(by=By.XPATH, value="//input[@id='join-confno']")
    input_element.send_keys(meet_code)

    submit_element = driver.find_element(by=By.XPATH, value="//a[@id='btnSubmit']")
    submit_element.click()

    submit_element = driver.find_element(by=By.ID, value="onetrust-accept-btn-handler")
    submit_element.click()

    submit_element = driver.find_element(by=By.XPATH, value="//*[@id='zoom-ui-frame']/div[2]/div/div[2]/h3[1]/a")
    submit_element.click()

    submit_element = driver.find_element(by=By.XPATH, value="//*[@id='zoom-ui-frame']/div[2]/div/div[2]/h3[2]/span/a")
    submit_element.click()

    input_element = driver.find_element(by=By.XPATH, value="//*[@id='inputname']")
    input_element.send_keys(user_name)

    submit_element = driver.find_element(by=By.XPATH, value="//*[@id='joinBtn']")
    submit_element.click()

    input_element = driver.find_element(by=By.XPATH, value="//*[@id='inputpasscode']")
    input_element.send_keys(pass_code)

    submit_element = driver.find_element(by=By.XPATH, value="//*[@id='joinBtn']")
    submit_element.click()


def get_count_users(driver: webdriver.Chrome):
    span_element = driver.find_element(by=By.XPATH, value="//*[@id='foot-bar']/div[2]/div[1]/button/div/span")
    return span_element.text


def is_session_stopped(driver: webdriver.Chrome):
    try:
        driver.find_element(by=By.XPATH, value="/html/body/div[12]/div/div")
    except Exception as e:
        return False
    else:
        return True


def set_timeout(interval):
    start_time = time.time()
    while time.time() - start_time < interval:
        pass


def wait_connection(driver: webdriver.Chrome):
    is_form_ready = False
    is_connected = False
    while not is_connected:
        set_timeout(INTERVAL)
        try:
            driver.find_element(by=By.XPATH, value="//*[@id='root']/div/div[3]/div/div[1]/div/div[3]/button")
        except Exception as e:
            if is_form_ready:
                is_connected = True
                print("Connected")
        else:
            is_form_ready = True
            is_connected = False
            print("Not connected")
    return is_connected


def wait_disconnect(driver: webdriver.Chrome):
    is_working = True
    max_users = get_count_users(driver)
    while is_working:
        set_timeout(INTERVAL)
        is_working = not is_session_stopped(driver)# or int(max_users) / 100 * 90 >= int(get_count_users(driver))


def start(meet_code, pass_code, user_name):
    print("Start")
    driver = get_driver()
    print("Join to session.")
    join_to_session(meet_code, pass_code, user_name, driver)
    print("Wait connection.")
    wait_connection(driver)
    print("Wait disconnect.")
    wait_disconnect(driver)
    print("Stop session")
    driver.quit()
    print("End")


def main():
    meet_code = "418 754 7973"
    pass_code = "9XBXZM"
    user_name = "User 1"

    start(meet_code, pass_code, user_name)
    start(meet_code, pass_code, user_name)


if __name__ == '__main__':
    main()