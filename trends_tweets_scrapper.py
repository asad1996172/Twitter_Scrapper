import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import os
import datetime
import time
from selenium.common.exceptions import TimeoutException

chrome_options = webdriver.ChromeOptions()
executable_path = 'chromedriver.exe'
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(
    executable_path=executable_path, chrome_options=chrome_options)
browser.set_window_size(1300, 768)
browser_link = 'https://twitter.com/gamingexprncia'
browser.get(browser_link)


def main(arguments):
# def main():

    if len(arguments)!=2:
        print("Invalid Number of Arguments !!! ")
        return

    try:
        val = int(arguments[1])
    except ValueError:
        print("Argumnet is not an int !!!")
        return

    if not os.path.exists('trends_tweets_dataset'):
        os.makedirs('trends_tweets_dataset')

    trends = []
    try:
        for (dirpath, dirnames, filenames) in os.walk('trends_tweets_dataset'):
            trends.extend(dirnames)
            break
        test = []
        for trend in trends:
            test.append(int(trend.split('_')[0]))
        highest = max(test)
    except:
        highest = 0

    with open('all_trends.pkl', 'rb') as f:
        trends = pickle.load(f)

    print("Total trends : " + str(len(trends)))

    print("Remaining trends : " + str(len(trends) - highest))

    for i in range(highest+1,len(trends)):
        trend = trends[i]

        appstr = "since:2017-01-01 until:" + \
            datetime.datetime.today().strftime('%Y-%m-%d')
        print("Starting Trend : ", trend)
        search_trend = browser.find_element_by_id("search-query")
        search_trend.clear()
        search_trend.send_keys(trend + " " + appstr)
        print(trend + " " + appstr)
        search_trend.send_keys(Keys.ENTER)
        search_trend.submit()
        end_of_page_checker = 0
        tweet_count = 0
        trends_tweets = {}
        try:
            lenOfPage = browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            match = False
            while (match == False):
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
                # print(tweet_count)
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
                            tweet_content_link = tweet.find_element_by_xpath(
                                "//a[@class='QuoteTweet-link js-nav']").get_attribute(
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
                        trends_tweets[str(tweet_count)] = whole_tweet
                        tweet_count += 1

                        if (tweet_count >= int(arguments[1])):
                            if not os.path.exists('trends_tweets_dataset/' + str(i) + "_" + trend[1:]):
                                os.makedirs('trends_tweets_dataset/' + str(i) + "_" + trend[1:])
                            with open('trends_tweets_dataset/' + str(i) + "_" + trend[1:] + '/tweets_list.pkl', 'wb') as f:
                                pickle.dump(trends_tweets, f, protocol=pickle.HIGHEST_PROTOCOL)
                            print("\nTrend " + str(i) + " completed : " + str(tweet_count) + " Tweets")
                            break
                    except Exception as e: print(e)

                print(str(trend) + " ====> Tweets Scraped : " + str(tweet_count) + " ====> Done Till : " + str(
                    last_date))
                lastCount = lenOfPage
                time.sleep(3)
                lenOfPage = browser.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount == lenOfPage:
                    match = True
                    if not os.path.exists('trends_tweets_dataset/' + str(i) + "_" + trend[1:]):
                        os.makedirs('trends_tweets_dataset/' + str(i) + "_" + trend[1:])
                    with open('trends_tweets_dataset/' + str(i) + "_" + trend[1:] + '/tweets_list.pkl', 'wb') as f:
                        pickle.dump(trends_tweets, f, protocol=pickle.HIGHEST_PROTOCOL)
                    print("\nTrend " + str(i) + " completed : " + str(tweet_count) + " Tweets")

                if tweet_count>=int(arguments[1]):
                    break
            # print(trends_tweets)
        except Exception as e: print(e)


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
                browser_link = 'https://twitter.com/gamingexprncia'
                browser.get(browser_link)
                continue
            break
