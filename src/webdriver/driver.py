from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json, time

class Post:
    def __init__(self):
        self.title  = '' 
        self.author = ''
        self.date   = '' 
        self.body   = ''

    # show prints the post to stdout.
    def show(self):
        print(f'{self.author}: {self.title} ({self.date})\n    {self.body}\n\n')

class Currents:
    def __init__(self, creds_file='creds.json', chill_time=3):
        self.URL = 'https://currents.google.com/u/1/communities/112231973545069490014?hl=en'
        self.chill_time = chill_time

        self.logged_in = False

        self.creds_file = creds_file
        self.username, self.password = self.load_creds()
    
        self.driver = webdriver.Firefox()

    def load_creds(self):
        with open(self.creds_file) as f:
            creds = json.load(f)
            return (creds['username'], creds['password'])

    def wait_for(self, name, callback):
        pass

    def login(self):
        self.driver.get(self.URL)

        # Enter the username
        self.driver.find_element_by_name('identifier').send_keys(self.username)

        # Click the username continue box
        self.driver.find_element_by_xpath("//*[@id='identifierNext']/div").click()

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'password'))
            )
            
            # Type the password
            self.driver.find_element_by_name('password').send_keys(self.password)

            # print(self.driver.find_element_by_xpath("//*[@id='passwordNext']/div").get_attribute('innerHTML')) # for debug

            # Click the nexxt button
            time.sleep(self.chill_time)
            login_button = self.driver.find_element_by_xpath("//*[@id='passwordNext']/div")
            login_button.click()

            '''
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='passwordNext']/div"))
            ).click()
            '''

            self.logged_in = True

            time.sleep(3) # To give time for the posts to load

        except TimeoutException as e:
            print(e)
    
    def fetch_all(self):
        if not self.logged_in:
            print('not logged in')
            return False

        posts_container = self.driver.find_element_by_xpath(
            "//div[@class='H68wj jxKp7'][@role='list']"
        )

        posts = posts_container.find_elements_by_tag_name('c-wiz')
        authors = posts_container.find_elements_by_xpath("//a[@class='f2PA1b HonOSe']")
        all_posts = []

        for i in range(1, len(posts) - 1):
            post = posts[i]

            post_data = Post()

            # Get the post title
            try:
                post_date.title = post.find_element_by_class_name('xelT1').get_attribute('innerHTML')
            except Exception:
                post_data.title = '(No title)'

            # Get the post body
            post_data.body = post.find_element_by_class_name('jVjeQd').get_attribute('innerHTML')

            # Get the post author
            post_data.author = authors[i].get_attribute('innerHTML')

            # Get the post date
            post_data.date = post.find_element_by_xpath("//div[@class='ZUmA7e']/span").get_attribute('innerHTML')
            all_posts.append(post_data)

            # Click the view post button and make it go into a new tab, grab the url.
            # then close the tab

        return all_posts

    def fetch_new(self):
        pass

scraper = Currents()
scraper.login()

posts = scraper.fetch_all()
for post in posts:
    post.show()

