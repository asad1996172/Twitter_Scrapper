from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import ast
import json
import time
from selenium.common.exceptions import TimeoutException
#browser = webdriver.Firefox()
chrome_options = webdriver.ChromeOptions()
executable_path = 'chromedriver.exe'
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(
    executable_path=executable_path, chrome_options=chrome_options)
browser.set_window_size(1366, 768)
browser_link = 'https://twitter.com/login'
user = ""
pwd = ""
browser.get(browser_link)
#assert "Login on Twitter" in browser.title
elem = browser.find_element_by_class_name("js-username-field")
elem.send_keys(user)
browser.implicitly_wait(1)
elem = browser.find_element_by_class_name("js-password-field")
elem.send_keys(pwd)
browser.implicitly_wait(1)
browser.find_element_by_class_name("EdgeButtom--medium").click()
for(path, dir, files) in os.walk("trends_tweets_dataset_political"):
    for name in dir:
        print("---------------------------------------------------")
        print("Starting for Username : ", name)
        new_dir = os.path.join(path, name)
        file = os.listdir(new_dir)
        # print(file)
        tweets = open(new_dir + "/" + file[1], "r")
        total_to_be_processed = len(tweets.readlines())
        print("Total Tweets : ", total_to_be_processed)
        tweets.close()
        tweets = open(new_dir + "/" + file[1], "r")
        retweets_file = open(new_dir + "/retweets.txt", 'r')
        total_done = len(retweets_file.readlines())
        retweets_file.close()
        retweets_file = open(new_dir + "/retweets.txt", 'a')
        print("Total Tweets Completed", total_done)
        line_no_for_tweets = 1
        for line in tweets:
            if (line_no_for_tweets > total_done):
                line_dict = ast.literal_eval(line)
                print("Processing Tweet : ", line_no_for_tweets,
                      "/", total_to_be_processed)
                # print("Line Dict Value :", line_dict)
                for key in line_dict.keys():
                    line_dict[key]["fullname"] = line_dict[key]["fullname"].decode(
                        "utf-8")
                    all_retweeters = {}
                    if int(line_dict[key]["retweets"]) > 0:
                        try:
                            file_path = os.path.join(new_dir, file[0])
                            # print(file_path)
                            # print("https://twitter.com/" +
                            #       str(line_dict[key]["user"]) + "/status/" + str(key))
                            browser.get("https://twitter.com/" +
                                        str(line_dict[key]["user"]) + "/status/" + str(key))
                            browser.find_element_by_class_name(
                                "request-retweeted-popup").click()
                            browser.implicitly_wait(2)
                            # total_retweeters = browser.find_element_by_id(
                            #     "activity-popup-dialog-header").text
                            # print(total_retweeters)

                            timeline = browser.find_element_by_xpath(
                                '//*[@id="activity-popup-dialog-body"]/div[4]/ol')
                            retweets = timeline.find_elements_by_css_selector(
                                'li.js-stream-item.stream-item.stream-item')

                            count = 1
                            for user in retweets:
                                one_retweeter = {}
                                info = user.find_element_by_css_selector(
                                    'div.stream-item-header')
                                user_profile_link = info.find_element_by_css_selector('a.account-group.js-user-profile-link').get_attribute(
                                    'href')

                                retweeted_by_name = info.find_element_by_css_selector(
                                    'strong.fullname').text
                                retweeted_by_username = info.find_element_by_css_selector(
                                    'span.username.u-dir.u-textTruncate').text
                                one_retweeter["profile_link"] = user_profile_link
                                one_retweeter["name"] = retweeted_by_name
                                one_retweeter["username"] = retweeted_by_username
                                # print(user_profile_link)
                                # print(retweeted_by_name)
                                # print(retweeted_by_username)
                                # print('')
                                all_retweeters[str(count)] = one_retweeter
                                count += 1
                            line_dict[key]["all_retweeters"] = all_retweeters
                            # print(line_dict)
                            retweets_file.write(json.dumps(line_dict))
                            retweets_file.write('\n')
                        except Exception as e:
                            line_dict[key]["all_retweeters"] = all_retweeters
                            # print(line_dict)
                            retweets_file.write(json.dumps(line_dict))
                            retweets_file.write('\n')
                            print(e)
                    else:
                        line_dict[key]["all_retweeters"] = all_retweeters
                        # print(line_dict)
                        retweets_file.write(json.dumps(line_dict))
                        retweets_file.write('\n')
                    time.sleep(2)
            line_no_for_tweets += 1
        tweets.close()
        retweets_file.close()
        print("---------------------------------------------------")
        print('')

browser.quit()
