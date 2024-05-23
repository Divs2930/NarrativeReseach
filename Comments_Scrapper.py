import time
import os
from tqdm import tqdm
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
# from chrome_driver import ChromeDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
# from config import DRIVER_PATH, NITTER_URL
options = Options()
options.headless = True  # Run Chrome in headless mode (no GUI)
NITTER_URL='https://nitter.poast.org/'
chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

chrome_driver.get(url=NITTER_URL)

try:
    # locate the setting button on nitter website and click it
    settings_button = chrome_driver.find_element(By.CSS_SELECTOR, 'a.icon-cog')
    settings_button.click()

    infinite_scroll_checkbox = chrome_driver.find_elements(By.XPATH,'/html/body/div/div/fieldset/form[1]/div/label[1]/span')[0]
    # infinite scroll selected or not
    if not infinite_scroll_checkbox.is_selected():
        # a.click()
        video_check = chrome_driver.find_element(By.XPATH, '/html/body/div/div/fieldset/form[1]/div/label[9]/span')
        if not video_check.is_selected():
            video_check.click()
        
        pinned_tweets = chrome_driver.find_element(By.XPATH, "/html/body/div[1]/div/fieldset/form[1]/div/label[6]")
        if not pinned_tweets.is_selected():
            pinned_tweets.click()

        tweet_replies = chrome_driver.find_element(By.XPATH, "/html/body/div[1]/div/fieldset/form[1]/div/label[7]")
        if not tweet_replies.is_selected():
            tweet_replies.click()
        
        enable_mp4 = chrome_driver.find_element(By.XPATH, "/html/body/div/div/fieldset/form[1]/div/label[9]/span")
        if not enable_mp4.is_selected():
            enable_mp4.click()
        
        enable_hls = chrome_driver.find_element(By.XPATH, "/html/body/div/div/fieldset/form[1]/div/label[10]/span")
        if not enable_hls.is_selected():
            enable_hls.click()
    
    save_button = chrome_driver.find_element(By.XPATH, '/html/body/div/div/fieldset/form[1]/button')
    save_button.click()

except (NoSuchElementException, ElementClickInterceptedException):
    print("ERORR OCCURED")
    time.sleep(2)

def scrape_comments(tweet_url: str):
    comments = []
    print(tweet_url)
    chrome_driver.get(tweet_url)
    count = 0
    last_height = 0

    for _ in range(50):
        
        chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        try:
            chrome_driver.find_element(By.CLASS_NAME, 'tweet-content media-body')
            print("Timeline break")
            return comments
        except:
            print("not yet")
        try:
            css_selector = "show-more"
            elements = chrome_driver.find_element(By.CLASS_NAME, css_selector)
            target_element = None
            for element in elements:
                if len(element.get_attribute("class").split()) == 1:
                    target_element = element
                    break
            if target_element:
                target_element.click()
                print("clicked")
                continue
        except:
            new_height = chrome_driver.execute_script("return document.body.scrollHeight")
            if(last_height == new_height):
                count+=1
            else:
                count = 0
                last_height = new_height
            if(count > 5):
                break
            print(count)

    replies = chrome_driver.find_elements(By.CLASS_NAME, "reply")
        
    for reply in replies:
        try:
            tweet_stats = [stat.text for stat in reply.find_element(
                By.CSS_SELECTOR, "div.tweet-stats").find_elements(By.CSS_SELECTOR, "span.tweet-stat")]
        except NoSuchElementException:
            continue
        try:
            attachments = [attachment.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                            for attachment in
                            reply.find_element(
                                By.CSS_SELECTOR, "div.attachments").find_elements(
                                By.CSS_SELECTOR, "div.attachment")
                            ] if "attachments" in reply.get_attribute('innerHTML') else []
        except NoSuchElementException:
            attachments = []

        comments.append({
            'datetime': reply.find_element(By.CSS_SELECTOR, "span.tweet-date a").get_attribute("title"),
            'url': reply.find_element(By.CSS_SELECTOR, "a").get_attribute("href"),
            'username': reply.find_element(By.CSS_SELECTOR, "a.tweet-avatar").get_attribute("href"),
            'tweet_content': reply.find_element(By.CSS_SELECTOR, "div.tweet-content.media-body").text,
            'attachments': attachments,
            'comments': tweet_stats[0],
            'retweets': tweet_stats[1],
            'quotes': tweet_stats[2],
            'likes': tweet_stats[3],
            'original_url': tweet_url,
        })
    
    return comments


if __name__ == '__main__':
    # read the tweet scrapped file to scraper comments for each of the tweet
    path = './TWEETS/final_rajesh.csv'
    save_dir_name = path.split("/")[-1].split(".")[0]
    user_df = pd.read_csv(path)
    data = user_df['link'].to_list()

    ids = [item.split("/")[-1].split("#")[0] for item in data]
    
    if os.path.exists(save_dir_name):
        pass
    else:
        os.mkdir(save_dir_name)
    
    # ids_already_scraped_list = [item.split(".")[0] for item in os.listdir('arvind_kejriwal_comments/')]
    print(len(data))
    for idx, link in enumerate(data):
        # if ids[idx] in ids_already_scraped_list:
        # #     continue
        # comments = scrape_comments(link)
        # chrome_driver.close()
        print(idx)
        # pd.DataFrame(comments).to_csv(f'r{idx}/ajesh_agrawal_comments.csv',index = False)
    
  