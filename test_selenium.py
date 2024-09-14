import unittest
from selenium import webdriver


class SeleniumTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()  # or another driver

    def test_add_user(self):
        driver = self.driver
        driver.get('http://localhost:5000/add_user')
        # Add test logic
        pass



    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
