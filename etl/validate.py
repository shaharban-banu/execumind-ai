def dataset_shape(df):
    return df.shape

def check_duplicates(df):
    return df.duplicated().sum()

def check_missing_values(df):
    return df.isnull().sum()

def validate_primary_key(df,primary_key):
    if primary_key is None:
        return "No primary key defined"
    return df[primary_key].duplicated().sum()

def get_dtypes(df):
    return df.dtypes