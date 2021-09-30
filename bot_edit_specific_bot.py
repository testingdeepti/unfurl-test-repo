import unittest
import os,sys,inspect
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import traceback
from selenium.webdriver.chrome.options import Options
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
parent_parentdir=os.path.dirname(parentdir)
sys.path.insert(0,parent_parentdir)
parent_parent_parentdir=os.path.dirname(parent_parentdir)
sys.path.insert(0,parent_parent_parentdir)
sys.path.insert(0,'../..')
from Commons import config_reg as cfg
from Commons.login import login
from Commons.delete_account import delete
from Commons.wait_and_click import wait_and_click
from Commons.Utils import Utils

opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
opts.add_argument("--start-maximized")
opts.add_argument('--headless')

class bot_edit_specific_bot(unittest.TestCase):
    '''
    Precondition: Should have altleat 1 bot modified activity in account for a specific bot
    Test case description: filter specific bot activity
    '''
    def setUp(self):
        try:
            self.utils = Utils()
            self.driver=webdriver.Chrome(options=opts)
            login(self.driver,cfg.activity['email'],cfg.activity['password'])
        except Exception as ee:
            self.utils.take_screen_shot(driver=self.driver, filename='bot_edit_specific_bot_setup_fail')
            print(ee)
            raise

    def test_bot_edit_specific_bot(self):
        try:
            #Make sure this app is available and has 9 or greater activities to it
            app_name="Google Sheets - New Row (Recommended)"
            edit_activity_count=1

            element_xpath="//a[contains(text(),'Activity')]"
            wait_and_click(self.driver,By.XPATH,element_xpath)

            element_xpath="//aio-btn-group-dropdown[1]//span[@class='caret']"
            wait_and_click(self.driver,By.XPATH,element_xpath)

            element_xpath="(//aio-btn-group-dropdown)[1]//span[contains(text(),'Bot Edit')]"
            wait_and_click(self.driver,By.XPATH,element_xpath)

            element_xpath="(//aio-btn-group-dropdown)[3]//span[@class='caret']"
            wait_and_click(self.driver,By.XPATH,element_xpath)

            element_xpath="(//aio-btn-group-dropdown)[3]//span[contains(text(),'"+app_name+"')]"
            wait_and_click(self.driver,By.XPATH,element_xpath)

            element=WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='title-msg-wrapper']")))

            all_activity_count=self.driver.find_elements_by_xpath("//div[@class='title-msg-wrapper']")

            self.assertGreaterEqual(len(all_activity_count),edit_activity_count,"All bot edit activities not rendered")
        except Exception as ee:
            self.utils.take_screen_shot(driver=self.driver, filename='bot_edit_specific_bot_test_fail')
            print(ee)
            raise

    def tearDown(self):
        # close the browser window
        self.driver.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2)