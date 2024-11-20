def has_verified_metrics(df):
    return  df.loc[(df['qod_score'] >= 0.8) & (df['pol_score'] > 0)]
