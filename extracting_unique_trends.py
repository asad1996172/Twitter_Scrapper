import pickle
from dateutil.parser import parse
    

def is_date(string):
    try:
        parse(string)
        return True
    except ValueError:
        return False

def get_trends():
    all_trends = []
    trends = open("trends.txt")
    trends = trends.readlines()
    curr_date = ""

    for i in range(len(trends)):
        line = trends[i].strip('\n')
        if is_date(line):
            curr_date = line
            continue
        elif '\\' in line:
            continue
        elif 'b' in line:
            try:
                line = line.split('b')[1][2:-1]
                if line != '':
                    if line[0]!='#':
                        line = '#' + line
                    if len(line) > 3:
                        all_trends.append(line)
            except:
                c=1

    all_trends = list((set(all_trends)))
    print("Total Unique Trends : " ,len(all_trends))
    with open('all_trends.pkl', 'wb') as f:
        pickle.dump(all_trends, f)

get_trends()
# with open('all_trends.pkl', 'rb') as f:
#     profiles = pickle.load(f)
#     print(profiles)