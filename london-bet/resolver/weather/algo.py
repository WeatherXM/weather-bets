def has_verified_data(df):   
    return true

def has_verified_metrics(df):
    # verified_loc = row['pol_score'] == 1
    # verified_data_quality = row['qod_score'] >= 0.8
    return df.loc[(df['qod_score'] >= 0.8) & (df['pol_score'] == 1)]
    #return (verified_loc and verified_data_quality)

