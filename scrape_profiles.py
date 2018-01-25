import sys
from selenium import webdriver
import pickle
from selenium.common.exceptions import TimeoutException
from os import walk
import time
import datetime

chrome_options = webdriver.ChromeOptions()
executable_path = 'chromedriver.exe'
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(executable_path=executable_path,chrome_options=chrome_options)
browser.set_window_size(1300, 768)

def get_profile(browser_link,till_year,path):
    browser.get(browser_link)
    count = 1
    whole_profile = {}
    # print(browser_link)
    # Profile Picture Link
    profile_picture_link = browser.find_element_by_xpath('//*[@id="page-container"]/div[1]/div/div[1]/div[2]/div[1]/div/a/img').get_attribute('src')
    # print(profile_picture_link)
    whole_profile["profile_pic_link"] = profile_picture_link
    list_of_details = browser.find_element_by_xpath('//*[@id="page-container"]/div[1]/div/div[2]/div/div/div[2]/div/div/ul')
    details = list_of_details.find_elements_by_tag_name('li')
    # Profile Details
    profile_details = {}
    try:
        for detail in details[:-3]:
            spans = detail.find_elements_by_tag_name('span')
            if (spans[0].text!='') and (spans[2].text!=''):
                profile_details[spans[0].text] = spans[2].text
    except:
        for detail in details[:-4]:
            spans = detail.find_elements_by_tag_name('span')
            if (spans[0].text!='') and (spans[2].text!=''):
                profile_details[spans[0].text] = spans[2].text
    # print(profile_details)

    whole_profile["profile_details"] = profile_details
    # Profile Desccription
    description = browser.find_element_by_xpath('//*[@id="page-container"]/div[2]/div/div/div[1]/div/div/div/div[1]/p').text
    # print(description)
    whole_profile["profile_description"] = description
    # Profile Created Date
    date_joined = browser.find_element_by_xpath('//*[@id="page-container"]/div[2]/div/div/div[1]/div/div/div/div[1]/div[3]/span[2]').text
    # print(date_joined)
    whole_profile["date_joined"] = date_joined
    # Get Timeline
    whole_timeline = {}
    tweet_count = 0
    end_of_page_checker = 0

    browser_link_temp = "https://twitter.com/search?l=&q=from%3A" + \
        browser_link.split(
            '/')[-1] + "%20since%3A2017-01-01%20until%3A" + datetime.datetime.today().strftime('%Y-%m-%d') + "&src=typd&lang=en"
    browser.get(browser_link_temp)

    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        # while (browser.execute_script("if (document.body.scrollHeight == document.body.scrollTop + window.innerHeight) { return false; } else { return true; }")):
        #     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        timeline = browser.find_element_by_xpath('//*[@id="stream-items-id"]')
        tweets = timeline.find_elements_by_css_selector('li.js-stream-item.stream-item.stream-item')
        # print("Tweet_count",tweet_count)
        # print("Tweets_found ",len(tweets))
        # if tweet_count == len(tweets):
        #     end_of_page_checker+=1
        # else:
        #     end_of_page_checker = 0
        # if end_of_page_checker == 40:
        #     break
        last_date = ""
        for tweet in tweets[tweet_count:]:
            try:
                whole_tweet = {}
                context = tweet.find_element_by_css_selector('div.context').text
                if "Retweeted" in context:
                    context = "Retweet"
                else:
                    context = "Tweet"
                # print(context)
                whole_tweet["context"] = context
                top_info = tweet.find_element_by_css_selector('div.stream-item-header')
                tweeted_by_name = top_info.find_element_by_css_selector('strong.fullname.show-popup-with-id.u-textTruncate').text
                tweeted_by_username = top_info.find_element_by_css_selector('span.username.u-dir').text
                date = top_info.find_element_by_css_selector('span._timestamp.js-short-timestamp').text
                last_date = date
                # print(date)
                # print(tweeted_by_name)
                # print(tweeted_by_username)

                whole_tweet["date"] = date
                whole_tweet["tweeted_by_name"] = tweeted_by_name
                whole_tweet["tweeted_by_username"] = tweeted_by_username

                desc = tweet.find_element_by_css_selector('div.js-tweet-text-container').text
                # print(desc)
                whole_tweet["description"] = desc
                try:
                    tweet_content_link = tweet.find_element_by_xpath("//a[@class='QuoteTweet-link js-nav']").get_attribute(
                        'href')
                except:
                    try:
                        tweet_content_link = tweet.find_elements_by_tag_name('img')
                        tweet_content_link = tweet_content_link[1].get_attribute('src')
                    except:
                        tweet_content_link = ""
                # print(tweet_content_link)
                whole_tweet["tweet_content_link"] = tweet_content_link
                footer = tweet.find_element_by_css_selector('div.stream-item-footer').text
                footer = footer.split('\n')
                if (footer[1] == 'Reply') or (footer[1] == 'Retweet') or (footer[1] == 'Like'):
                    footer.insert(1, '0')
                if (footer[3] == 'Reply') or (footer[3] == 'Retweet') or (footer[3] == 'Like'):
                    footer.insert(3, '0')
                if len(footer) == 5:
                    footer.insert(5, '0')

                replies = footer[1]
                retweets = footer[3]
                likes = footer[5]
                whole_tweet["replies"] = replies
                whole_tweet["retweets"] = retweets
                whole_tweet["likes"] = likes
                # print(tweet_count)
                whole_timeline[str(tweet_count)] = whole_tweet
                tweet_count += 1

                if (till_year in date) and (context == "Tweet"):
                    whole_profile["timeline"] = whole_timeline
                    filename = browser_link.split('/')[-1]
                    with open(path + '/' + filename + '.pickle', 'wb') as handle:
                        pickle.dump(whole_profile, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    return
            except Exception as e: print(e)

        print(str(browser_link) + " ====> Tweets Scraped : " + str(tweet_count) + " ====> Done Till : " + str(last_date))
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True


    whole_profile["timeline"] = whole_timeline
    filename = browser_link.split('/')[-1]
    with open(path + '/' +filename + '.pickle', 'wb') as handle:
        pickle.dump(whole_profile, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Load data (deserialize)
    # with open('filename.pickle', 'rb') as handle:
    #     unserialized_data = pickle.load(handle)

def main(arguments):

    if len(arguments)!=2:
        print("Invalid Number of Arguments !!! ")
        return

    trends = []
    for (dirpath, dirnames, filenames) in walk('dataset'):
        trends.extend(dirnames)
        break
    test = []
    for i in range(len(trends)):
        trend = trends[i]
        with open('dataset/' + trend +'/profiles_list.pkl', 'rb') as f:
            profile_links = pickle.load(f)

        already_done = []
        for (dirpath, dirnames, filenames) in walk('dataset/' + trend):
            already_done.extend(filenames)
            break
        # print(already_done)
        for j in range(len(profile_links)):
            profile_link =  profile_links[j]
            if str(profile_link.split('/')[-1] + '.pickle') not in already_done:
                print(str("Processing " + str(i) + " Trend " + str(j) + " Profile "))
                print(profile_link)
                # profile_link = "https://twitter.com/ImranKhanPTI"
                get_profile(profile_link,arguments[1],'dataset/' + trend)

                print(str("Completed " + str(i) + " Trend " + str(j) + " Profile "))
                print("")


for i in range(0, 1):
        while True:
            try:
                main(sys.argv)
            except TimeoutException as ex:
                print("Exception has been thrown. " + str(ex))
                browser.close()
                browser = webdriver.Chrome(
                    executable_path=executable_path, chrome_options=chrome_options)
                browser.set_window_size(1300, 768)      
                continue
            break
