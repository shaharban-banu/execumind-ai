import pandas as  pd

def extract_csv(file_path):
    """Generic csv extractor"""
    return pd.read_csv(file_path)