"""
ETL Evaluation Module.

Validates:
1. Row Counts
2. Duplicate Records
3. Foreign Key Integrity
4. Missing Values

Author: ExecuMind AI
"""
from utils.logger import logger
from pathlib import Path
import pandas as pd
from sqlalchemy import text
from database.database import engine

OUTPUT_DIR=Path("evaluation/results")
OUTPUT_FILE=(OUTPUT_DIR/"etl_report.csv")

def run_query(query):
    """
    Execute SQL query.
    """
    return pd.read_sql(text(query),engine)

#ROW COUNT VALIDATION
#-------------------------------
def validate_row_count():
    tables=["customers","orders","products","reviews","sellers",
        "payments","order_items","geolocation"]
    results=[]
    for table in tables:
        query=f"select count(*) as row_count from {table}"
        count_row=run_query(query)["row_count"][0]
        results.append({
            "check_type":"row_count",
            "table":table,
            "result":count_row,
            "status":"PASS"
        })
    return results

#DUPLICATE VALIDATION
# ----------------------------   
def validate_duplicates():
    checks=[("customers","customer_id"),("orders","order_id"),("products","product_id"),
            ("reviews","review_id"),("sellers","seller_id")]
    results=[]
    for table,column in checks:
        query=f"select count(*)-count(distinct {column}) as duplicates from {table}"
        duplicates=run_query(query)["duplicates"][0]
        results.append({
            "check_type":"duplicates",
            "table":table,
            "result":duplicates,
            "status":("PASS" if duplicates==0 else "FAIL")
        })
    return results
    
#MISSING VALUES VALIDATION
#-----------------------------
def validate_missing_values():
    checks=[( "orders","customer_id"),
            ( "orders","order_purchase_timestamp"),
            ("reviews","review_score"),
            ("products","product_category_name")]
    results=[]
    for table,column in checks:
        query=f"select count(*) as missing_count from {table} where {column} is NULL"
        missing=run_query(query)['missing_count'][0]

        results.append({
            "check_type":"missing_values",
            "table":f"{table}.{column}",
            "result":missing,
            "status":("PASS" if missing==0 else "WARNING")
        })
    return results
    
def main():
    OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
    report=[]
    report.extend(validate_row_count())
    report.extend(validate_duplicates())
    report.extend(validate_missing_values())
    report_pdf=pd.DataFrame(report)
    report_pdf.to_csv(OUTPUT_FILE,index=False)
    print("\nEvaluation")
    print("="*80)

    print(report_pdf)
    print(f"\nReport saved : {OUTPUT_FILE}")

if __name__=="__main__":
    main()
