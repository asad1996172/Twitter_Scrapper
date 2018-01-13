import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import os
import time
from selenium.common.exceptions import TimeoutException

def main(arguments):

    if len(arguments) != 2:
        print("Invalid Number of Arguments !!! ")
        return

    try:
        val = int(arguments[1])
    except ValueError:
        print("Argumnet is not an int !!!")
        return

    if not os.path.exists('dataset'):
        os.makedirs('dataset')

    chrome_options = webdriver.ChromeOptions()
    executable_path = 'chromedriver.exe'
    chrome_options.add_argument("--headless")
    

    for i in range(0, 1):
        while True:
            try:
                browser = webdriver.Chrome(
                    executable_path=executable_path, chrome_options=chrome_options)
                browser.set_window_size(1300, 768)
                browser_link = 'https://twitter.com/gamingexprncia'
                browser.get(browser_link)
                trends = []
                try:
                    for (dirpath, dirnames, filenames) in os.walk('dataset'):
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

                for i in range(highest + 1, len(trends)):
                    trend = trends[i]
                    profiles_list = []
                    profiles_count = 0
                    search_trend = browser.find_element_by_id("search-query")
                    search_trend.clear()
                    search_trend.send_keys(trend)
                    search_trend.send_keys(Keys.ENTER)
                    search_trend.submit()
                    end_of_page_checker = 0
                    while True:
                        browser.find_element_by_tag_name('body').send_keys(Keys.END)
                        html_list = browser.find_element_by_id("stream-items-id")
                        profiles = html_list.find_elements_by_xpath(
                            "//a[@class='account-group js-account-group js-action-profile js-user-profile-link js-nav']")
                        time.sleep(2)
                        print("Trend " + str(i) + " Reached : " +
                            str(len(set(profiles_list))) + " Profiles")
                        # print("profiles_count",profiles_count)
                        # print("profiles_found ",len(profiles))
                        if profiles_count == len(profiles):
                            end_of_page_checker += 1
                        else:
                            end_of_page_checker = 0
                        if end_of_page_checker == 10:
                            if not os.path.exists('dataset/' + str(i) + "_" + trend[1:]):
                                os.makedirs('dataset/' + str(i) + "_" + trend[1:])
                            with open('dataset/' + str(i) + "_" + trend[1:] + '/profiles_list.pkl', 'wb') as f:
                                pickle.dump(list(set(profiles_list)), f)
                            print("\nTrend " + str(i) + " completed : " +
                                str(len(set(profiles_list))) + " Profiles")
                            print("")
                            break

                        for profile in profiles[profiles_count:]:
                            profile_link = profile.get_attribute("href")
                            # print(profile_link)
                            # print(profiles_count)
                            profiles_count += 1
                            profiles_list.append(profile_link)
                        if len(set(profiles_list)) > int(arguments[1]):
                            if not os.path.exists('dataset/' + str(i) + "_" + trend[1:]):
                                os.makedirs('dataset/' + str(i) + "_" + trend[1:])
                            with open('dataset/' + str(i) + "_" + trend[1:] + '/profiles_list.pkl', 'wb') as f:
                                pickle.dump(list(set(profiles_list)), f)
                            print("\nTrend " + str(i) + " completed : " +
                                str(len(set(profiles_list))) + " Profiles")
                            print("")
                            break

            except TimeoutException as ex:
                print("Exception has been thrown. " + str(ex))
                browser.close()
                continue
            break

    

main(sys.argv)
