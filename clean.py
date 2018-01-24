def make_categories(df, column_name):
        """ input: df and column to be turned into categories
            output: updated dataframe with dummies added and original column dropped
        """
        df = pd.concat([df, pd.get_dummies(df[column_name], prefix=column_name+'_')], axis=1)
        df = df.drop(labels=[column_name], axis=1)
        return df
    
    
def clean_data(insta_df):
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