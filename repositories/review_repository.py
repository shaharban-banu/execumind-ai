"""
Repository for review-related
database operations.
"""

import pandas as pd
from sqlalchemy import text

from database.database import engine
from utils.logger import logger

def get_reviews():
    """
    Retrieve review data from the reviews table.

    Returns:
        pd.DataFrame:
            DataFrame containing review_id,
            order_id,
            review_score,
            and review_comment_message.
    """

    query="""
    select review_id,order_id,review_score,review_comment_message
    from reviews"""
    df=pd.read_sql(text(query),engine)
    logger.info(f"{len(df)} reviews retrieved")
    return df