# Twitter_Scrapper
Twitter Profile and Trend wise Tweets Scrapper

Fast Internet is recommended as it helps loading JS faster.

Following are the 4 steps of the code.

______________________________________    STEP - 1    ____________________________________________________

Run get_trends.py to get all the trends on daily basis. It saves all these trends in "trends.txt" file.
It has two arguments i.e
1) Start Date ( should be greater than 2015-04-01 )
2) End Date ( should be less than current date )

Format Of the date is ==> yy-mm-dd ==> e.g 2017-12-10

For example :

              filename      start_date end_date
       -----------------------------------
       python get_trends.py 2017-01-01 2017-12-10

____________________________________________________________________________________________________________

______________________________________    STEP - 2    ______________________________________________________

Run extracting_unique_trends.py to get all the unique trends present in the trends.txt file. It reads all the
trends from the "trends.txt" file and then makes a pickle file "all_trends.pkl" containing a list of unique
trends.

For example :

              filename
       ---------------------
       python extracting_unique_trends.py
____________________________________________________________________________________________________________

______________________________________    STEP - 3    ______________________________________________________

Run scrape_profile_links.py to get list of profiles with respect to trends. It creates a folder named "dataset"
and the creates subfolder for every trend. In each of these subfolders there is a file named 'profiles_list.pkl'
which is a pickle file containing a list of profile links belonging to respective trend.

If code is interrupted, it carries on from where it left provided that "all_trends.pkl" doesn't change.

Following is its one and only argument:
1) Number of profile links per trend

This is because of the fact that many trends have thousands of profiles so we need a limit.

For example:

              filename                profiles per trend
       -------------------------------------------------
       python scrape_profile_links.py 600
____________________________________________________________________________________________________________

______________________________________    STEP - 4    ______________________________________________________

Run scrape_profiles.py to get the whole profile data of profiles. It opens up the respective trend subfolder
and reads the pickle file . then it downloads tweets for the past year ( given as an argument ) and save the
profile as a dictionary as a pickle in the folder by the name of that profile. Following python code is used
to read these profiles

with open('filename.pickle', 'rb') as handle:
    b = pickle.load(handle)

If interrupted , the code carries on from the remaining profiles.

Following is the only argument for this.
1) Year till the profile is to scraped. ( '2016' means tweets from 'Dec 30 2016' onwards )

For example:

              filename           till year
       -------------------------------------------------
       python scrape_profiles.py 2016
____________________________________________________________________________________________________________

Step 3 and Step 4 can run side by side to fasten things.
Run Step 3 and when one trend is complete you can run Step 4 to donwload all the profiles of completed trend.


____________________________________________________________________________________________________________

______________________________________    Independent Step    ______________________________________________________

Run trends_tweets_scrapper.py to get the tweets data for a particular trend. Data is stored in folder
trends_tweets_dataset .It opens up the respective trend subfolder
and creates the pickle file . This pickle file contains all the tweets regarding the respective trend.

Following is its one and only argument:
1) Number of Tweets per trend

This is because of the fact that many trends have thousands of tweets so we need a limit.

For example:

              filename                tweets per trend
       -------------------------------------------------
       python trends_tweets_scrapper.py 600
