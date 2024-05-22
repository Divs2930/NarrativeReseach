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

def get_tweets_and_profile(username):
    username=str(username)
    print(username,NITTER_URL)
    """
    This will scrape the tweets for a given user based on the username provided.

    :param username: username of the tweet handle
    :return:
    """
    x=NITTER_URL+'/'+username
    print(x)
    chrome_driver.get(x)

    time.sleep(5)
    # list to store tweets data
    final = []

    # locate the profile details
    profile_elements = chrome_driver.find_element(By.CLASS_NAME,"profile-statlist").find_elements(By.XPATH, ".//li")

    # emtpy dict to store profile data
    profile = {}

    try:
        # add #post in the dict
        profile['posts'] =  profile_elements[0].find_element(By.XPATH, "//li[contains(@class,'posts')]").text.split('\n')[
            -1].replace(',', '')
    except:
        profile['posts']=''
    
    try:
        # add #following in the dict
        profile['following'] = profile_elements[0].find_element(By.XPATH, "//li[contains(@class,'following')]").text.split('\n')[-1].replace(',', '')
    except:
        profile['following'] = ''
    
    try:
        # add #followers in the dict
        profile['followers']=profile_elements[0].find_element(By.XPATH, "//li[contains(@class,'followers')]").text.split('\n')[-1].replace(',', '')
    except:
        profile['followers']=''
    
    try:
        # add #likes in the dict
        profile['likes'] = profile_elements[0].find_element(By.XPATH, "//li[contains(@class,'likes')]").text.split('\n')[
            -1].replace(',', '')
    except:
        profile['likes']=''
    
    try:
        # add joined date in the dict
        profile['joined'] = chrome_driver.find_element(By.CLASS_NAME,'profile-joindate').find_element(By.XPATH,".//span[contains(@title, 'M')]").get_attribute('title')
    except:
        profile['joined']=''
    
    try:
        # add #total_media in the dict
        profile['total_media']=chrome_driver.find_element(By.CLASS_NAME,'photo-rail-header').text
    except:
        profile['total_media']=''
    
    try:
        # add bio in the dict
        profile['bio']=chrome_driver.find_element(By.CLASS_NAME,'profile-bio').text,
    except:
        profile['bio'] = ''
    
    try:
        # add location in the dict
        profile['location'] = chrome_driver.find_element(By.CLASS_NAME,'profile-location').text
    except:
        profile['location'] = ''    
    
    profile['profile_handle'] = username    
    profile['profile'] = chrome_driver.find_element(By.CLASS_NAME,'profile-card-fullname').get_attribute('title')

    tweets_texts = []
    tweet_links = []
    
    tweets = chrome_driver.find_elements(By.CSS_SELECTOR, 'div.timeline-item')

    # check to exit if no tweets are loaded on the homepage of the profile
    if not tweets:
        return
    
    count=0

    flag = True
    while flag:
        # get the tweet elemets
        tweets_from_tag = [item for item in chrome_driver.find_elements(By.CSS_SELECTOR, 'div.timeline-item') if item.get_attribute('class').strip() == 'timeline-item']
        # get the link elements
        links_from_tag = chrome_driver.find_elements(By.CSS_SELECTOR, 'a.tweet-link')
        tweets_texts.extend(tweets_from_tag)
        tweet_links.extend(links_from_tag)

        try:
            for tweets_, links in tqdm(zip(tweets_from_tag, links_from_tag)):
                if count>=500:
                    flag=False
                    break
                else:
                    
                    
                    
                    print(f'in loop {count} ---------------------------------')
                    
                count+=1
                try:
                    details = {}
                    try:
                        images_list = []
                        image_links = []
                        list_of_images = tweets_.find_elements(By.CLASS_NAME, 'gallery-row')
                        for row in list_of_images:
                            images_list.extend([i for i in row.find_elements(By.CSS_SELECTOR, 'a.still-image')])
                        for img in images_list:
                            image_links.append(img.get_attribute('href'))
                        details['images'] = image_links
                    except NoSuchElementException:
                        details['images'] = []
                    # try:
                    #     videos_list = []
                    #     videos_links = []
                    #     list_of_videos = tweets_.find_elements(By.CLASS_NAME, 'gallery-video')
                    #     for row in list_of_videos:
                    #         if row:
                    #             details['videos'] = True
                    # except NoSuchElementException:
                    #     details['videos'] = []    

                    details['retweet_of'] = ''
                    details['handle_original_tweet'] = ''
                    details['handle_original_tweet_name'] = ''
                    details['handle_original_tweet_user'] = ''

                    try:
                        tweets_.find_element(By.CLASS_NAME, 'retweet-header')
                        details['type_of_tweet'] = 'retweet'
                        details['user'] = ' '.join(
                            tweets_.find_element(By.CLASS_NAME, 'retweet-header').text.split()[:-1])
                        details['retweet_of'] = tweets_.find_element(By.CLASS_NAME, 'retweet-header').text
                        details['handle_original_tweet_name'] = tweets_.find_element(By.CLASS_NAME, 'fullname').text
                        details['handle_original_tweet_user'] = tweets_.find_element(By.CLASS_NAME, 'username').text
                    except NoSuchElementException:

                        details['type_of_tweet'] = 'tweet'
                        try:
                            tweets_.find_element(By.CSS_SELECTOR, 'a.quote-link')
                            details['type_of_tweet'] = 'quote'
                            details['quote_original_text'] = tweets_.find_element(By.CLASS_NAME,'quote-text').text
                            details['handle_original_tweet_name'] = tweets_.find_element(By.CSS_SELECTOR,
                                                                                        'div.quote').find_element(
                                By.CSS_SELECTOR, 'a.fullname').get_attribute('text')
                            details['handle_original_tweet_user'] = tweets_.find_element(By.CSS_SELECTOR,
                                                                                        'div.quote').find_element(
                                By.CSS_SELECTOR, 'a.username').get_attribute('text')
                        except NoSuchElementException:
                            details['type_of_tweet'] = 'tweet'
                        details['retweet_of'] = ''
                        details['handle_original_tweet'] = ''
                        details['handle_original_tweet_name'] = ''

                    if 'timeline-item thread' in tweets_.get_attribute('class'):
                        details['type_of_tweet'] = 'thread' 
                    details['time_elapsed'] = tweets_.find_element(By.CLASS_NAME, 'tweet-date').find_element(
                        By.CSS_SELECTOR, 'a').get_attribute('title')
                    stats = tweets_.find_elements(By.CSS_SELECTOR, 'span.tweet-stat')
                    details['comments_on_tweet'] = stats[0].text
                    details['retweets_on_tweet'] = stats[1].text
                    details['quote_on_tweet'] = stats[2].text
                    details['likes_on_tweet'] = stats[3].text
                    details['text'] = tweets_.find_element(By.CLASS_NAME,'tweet-content').text
                    details['link'] = tweets_.find_element(By.CLASS_NAME,'tweet-link').get_attribute('href')
                    details['profile'] = profile['profile']
                    details['profile_handle'] = profile['profile_handle']
                    details['posts'] = profile['posts']
                    details['likes']=profile['likes']
                    details['followers']=profile['followers']
                    details['following']=profile['following']
                    # details['bio'] = profile['bio']
                    # details['joined'] = profile['joined']
                    # details['location'] = profile['location']
                    # details['total_media'] = profile['total_media']
                    details['user'] = tweets_.find_element(By.CLASS_NAME,'fullname-and-username').find_element(By.CLASS_NAME,'fullname').text
                    details['username'] = tweets_.find_element(By.CLASS_NAME,'fullname-and-username').find_element(By.CLASS_NAME,'username').text

                    # try:
                    #     details['views_on_video'] = stats[4].text
                    # except:
                    #     details['views_on_video'] = []
                    final.append(details)
                    

                except NoSuchElementException:
                    continue
            try:
                # find the show more button
                show_more_tags = chrome_driver.find_elements(By.CSS_SELECTOR, 'div.show-more')
                flag_2 = True
                for show_more_tag in show_more_tags:
                    # get the show more button and click on it
                    if show_more_tag.get_attribute('class').strip() == 'show-more':
                        show_more_tag.click()
                        time.sleep(10)
                        flag_2 = False
                # if flaf_2 is found true that means the we are not getting the show more button and now we can end the scrapping
                if flag_2:
                    flag = False
            except Exception as e:
                print(e)
                flag = False
        
        except Exception as e:
            chrome_driver.close_window()
    
    return final

if __name__ == '__main__':

    user_list = ['RajeshAgrawal']
    for user in user_list:
        
        if os.path.exists(f'TWEETS/'):
            pass
        else:
            os.mkdir(f'TWEETS/')
        
        final = get_tweets_and_profile(user)
        
        user_tweets = pd.DataFrame(final)
        user_tweets.to_csv(f'./TWEETS/New_{user}.csv',index = False)