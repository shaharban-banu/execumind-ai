import pandas as pd

def standardise_column_names(df):
    df.columns=df.columns.str.strip().str.lower()
    return df

def convert_date_column(df,date_columns):
    for col in date_columns:
        if col in df.columns:
            df[col]=pd.to_datetime(df[col],errors='coerce')
    return df



def handle_missing_values(df,rules):
    for column,fill_value in rules.items():
        if column in df.columns:
            df[column]=df[column].fillna(fill_value)
    return df