from ast import literal_eval
import re
import pandas as pd

    
def clean_instagram_post_data(insta_df):
    '''
    clean instagram datafram
    '''
    insta_df['date']= pd.to_datetime(insta_df['taken_at'], unit = 's')
    
    insta_df['people_tagged '] = insta_df['people_tagged '].apply(literal_eval)
    insta_df['commenters'] = insta_df['commenters'].apply(literal_eval)
    insta_df['comments'] = insta_df['comments'].apply(literal_eval)
    insta_df['hashtags'] = insta_df['hashtags'].apply(literal_eval)
    insta_df['num_people_tagged'] = insta_df['people_tagged '].apply(length)
    insta_df['year'] = pd.DatetimeIndex( insta_df['date']).year
    insta_df['month'] = pd.DatetimeIndex( insta_df['date']).month
    insta_df['day'] = pd.DatetimeIndex( insta_df['date']).day
    insta_df['hour'] = pd.DatetimeIndex( insta_df['date']).hour
    insta_df['DOW'] = pd.DatetimeIndex( insta_df['date']).dayofweek
    insta_df['date']= insta_df['day']+ 100 * insta_df['month'] + 10000 * insta_df['year']
    insta_df['num_posts']= 1
    insta_df = pd.get_dummies(insta_df, columns=["DOW"],drop_first=True)
    return insta_df

def clean_order_data(df):
    df['total'] = df['total'].apply(remove_dollar_signs)
    df['order_num'] = df['order_num'].apply(remove_hashtag)
    for column in ['items', 'order_num','total']:
        df[column] = df[column].apply(literal_eval)
    df['number_of_items'] = df['items'].apply(len)
    df['time_of_sale'] = df['sale_time'].apply(extract_time)
    df['month'] = df['sale_time'].apply(extract_month)
    df['year'] = df['sale_time'].apply(extract_year)
    return df







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