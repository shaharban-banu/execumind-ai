"""
Load transformed datasets into SQLite.
"""
from utils.logger import logger
from typing import Dict
import pandas as pd
from sqlalchemy.orm import Session

class DataLoader:
    table_order=[
            "customers",
            "products",
            "sellers",
            "orders",
            "payments",
            "order_items",
            "reviews",
            "geolocation",
            "category_translation",
        ]
    def __init__(self,session:Session,datasets:Dict[str,pd.DataFrame]):
        self.datasets=datasets
        self.session=session
    def load(self):
        logger.info("Starting data loading...")
       
        loaded_tables = set()
        try:

            #
            # Load dependency tables first
            #
            for table_name in self.table_order:
                if table_name not in self.datasets:
                    continue

                self._load_table(table_name,self.datasets[table_name],)
                loaded_tables.add(table_name)

            #
            # Load any remaining canonical tables
            #
            remaining_tables =[table for table in self.datasets if table not in loaded_tables]

            for table_name in remaining_tables:
                self._load_table(table_name,self.datasets[table_name],)

            self.session.commit()

            logger.info("Data loading completed successfully.")

        except Exception:

            self.session.rollback()
            logger.exception("Data loading failed.")
            raise

    def _load_table(self,table_name: str,dataframe: pd.DataFrame,replace_existing:bool=True,) :
        """
        Load a single DataFrame into SQLite.
        """

        logger.info("Loading table '%s' (%d rows)",table_name,len(dataframe),)

        dataframe.to_sql(
            name=table_name,
            con=self.session.bind,
            if_exists="replace" if replace_existing else 'append',
            index=False,
            
        )

        logger.info("Loaded '%s'",table_name,)

# from database.database import engine

# def load_customers(df):
#     df.to_sql("customers",engine,if_exists="replace",index=False)
#     print("customer loaded.")

# def load_orders(df):
#     df.to_sql("orders",engine,if_exists="replace",index=False)
#     print("orders loaded.")

# def load_products(df):
#     df.to_sql("products",engine,if_exists="replace",index=False)
#     print("products loaded.")

# def load_reviews(df):
#     df.to_sql("reviews",engine,if_exists="replace",index=False)
#     print("reviews loaded.")

# def load_sellers(df):
#     df.to_sql("sellers",engine,if_exists="replace",index=False)
#     print("sellers loaded.")

# def load_payments(df):
#     df.to_sql("payments",engine,if_exists="replace",index=False)
#     print("payments loaded.")

# def load_order_items(df):
#     df.to_sql("order_items",engine,if_exists="replace",index=False)
#     print("order_items loaded.")

# def load_geolocation(df):
#     df.to_sql("geolocation",engine,if_exists="replace",index=False)
#     print("geolocation loaded.")

# def load_category(df):
#     df.to_sql("category_translation",engine,if_exists="replace",index=False)
#     print("product category translation added")
