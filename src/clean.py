from ast import literal_eval
import re
import pandas as pd

 
def clean_fresh_instagram_post_data(insta_df):
    '''
    clean instagram dataframe right after scraping
    '''
    insta_df['date']= pd.to_datetime(insta_df['taken_at'], unit = 's')
    insta_df['num_people_tagged'] = insta_df['people_tagged'].apply(length)
    insta_df['year'] = pd.DatetimeIndex( insta_df['date']).year
    insta_df['month'] = pd.DatetimeIndex( insta_df['date']).month
    insta_df['day'] = pd.DatetimeIndex( insta_df['date']).day
    insta_df['hour'] = pd.DatetimeIndex( insta_df['date']).hour
    insta_df['DOW'] = pd.DatetimeIndex( insta_df['date']).dayofweek
    insta_df['date_num']= insta_df['day']+ 100 * insta_df['month'] + 10000 * insta_df['year']
    insta_df['num_posts']= 1
    insta_df = pd.get_dummies(insta_df, columns=["DOW"],drop_first=False)
    return insta_df   


def clean_instagram_post_data(insta_df):
    '''
    clean instagram dataframe that was stored as csv
    '''
    insta_df['date']= pd.to_datetime(insta_df['taken_at'], unit = 's')
    if 'people_tagged ' in insta_df.columns:
        insta_df['people_tagged'] = insta_df['people_tagged ']
        insta_df.drop(['people_tagged '], axis=1, inplace=True)    
    for col in ['people_tagged', 'commenters', 'comments', 'hashtags']:
        insta_df[col] = insta_df[col].apply(literal_eval)
    insta_df['num_people_tagged'] = insta_df['people_tagged'].apply(length)
    insta_df['year'] = pd.DatetimeIndex( insta_df['date']).year
    insta_df['month'] = pd.DatetimeIndex( insta_df['date']).month
    insta_df['day'] = pd.DatetimeIndex( insta_df['date']).day
    insta_df['hour'] = pd.DatetimeIndex( insta_df['date']).hour
    insta_df['DOW'] = pd.DatetimeIndex( insta_df['date']).dayofweek
    insta_df['date_num']= insta_df['day']+ 100 * insta_df['month'] + 10000 * insta_df['year']
    insta_df['num_posts']= 1
    insta_df = pd.get_dummies(insta_df, columns=["DOW"],drop_first=False)
    return insta_df

def add_rep_booleans(serious_reps, df):
    for rep in serious_reps:
        df[rep] = df.apply(lambda x: is_tagged(rep, x.people_tagged), axis=1)
    return df
    
    
    
def clean_order_data(df):
    '''
    clean order data that has been stored as csv
    '''
    df['total'] = df['total'].apply(remove_dollar_signs)
    df['order_num'] = df['order_num'].apply(remove_hashtag)
    for column in ['items', 'order_num','total']:
        df[column] = df[column].apply(literal_eval)
    df['number_of_items'] = df['items'].apply(len)
    df['time_of_sale'] = df['sale_time'].apply(extract_time)
    df['month'] = df['sale_time'].apply(extract_month)
    df['year'] = df['sale_time'].apply(extract_year)
    return df


def clean_traffic_data(df):
  
    df['date'] = pd.to_datetime(df['Unnamed: 0'])
    df.drop('Unnamed: 0', inplace=True, axis=1)
    df['percent_Insta'] = df['Instagram'] / df['total']
    #df= df.set_index('')
    return df 

def make_best_of_day(insta_df):
    '''
    turns instagram post df into a df with a row for each unique day where there was a post
    '''
    insta_df_sorted = insta_df[['date_num','number_of_likes', 'DOW_1','DOW_2','DOW_3','DOW_4','DOW_5','DOW_6', 'num_people_tagged']].groupby(by=['date_num','number_of_likes']).max().reset_index()
    daily_post_count = insta_df[['date_num','num_posts']].groupby(by=['date_num']).count()
    best_of_day = insta_df_sorted.drop_duplicates(subset=['date_num'], keep='last')
    best_of_day.set_index('date_num', inplace=True)
    best_of_and_count = pd.concat([best_of_day,daily_post_count], axis=1,)
    return best_of_and_count


def is_tagged(person, ppl_tagged):
    if person in ppl_tagged:
        return True
    else:
        return False

def extract_year(time):
    match = re.search('\d\d\d\d', time)
    year = match.group()
    return int(year)

def extract_month(time):
    match = re.search('\w\w\w+?\s', time)
    month = match.group()
    return month.strip()
    
def extract_time(time):
    match = re.search('\d+?\:\d\d\wm', time)
    time = match.group()
    if len(time) == 6:
        refined_time = int(time[0])
    elif len(time) == 7:
        refined_time = int(time[:2])
    if time[-2:] == 'pm' and refined_time != 12:
        refined_time += 12
    refined_time += float(time[-4:-2])/60
    return round(refined_time,2)

def length(thing):
    return len(thing)

def remove_hashtag(thing):
    return re.sub('\#', '', thing)

def remove_dollar_signs(thing):
    return re.sub('\$', '', thing)

def make_categories(df, column_name):
    """ input: df and column to be turned into categories
            output: updated dataframe with dummies added and original column dropped
        """
    df = pd.concat([df, pd.get_dummies(df[column_name], prefix=column_name+'_')], axis=1)
    df = df.drop(labels=[column_name], axis=1)
    return df