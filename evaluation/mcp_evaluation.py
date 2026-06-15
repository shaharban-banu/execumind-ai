"""
MCP Tool Evaluation.
"""

import pandas as pd

from mcp.tools.query_db import query_db
from mcp.tools.search_docs import search_docs
from mcp.tools.check_delivery_issues import (check_delivery_issues)
from mcp.tools.check_delivery_issues_by_state import (check_delivery_issues_by_state)

results = []

#query_db
#--------------------------
try:
    query_db("select count(*) as total_orders from orders")
    results.append(["query_db_valid","PASS"])
except Exception:
    results.append(["query_db_valid","FAIL"])

try:
    query_db("select * from xyz")
    results.append(["query_db_invalid","FAIL"])
except Exception:
    results.append(["query_db_invalid","PASS"])

try:
    docs=search_docs("delivery issues")
    if (len(docs["business_docs"])>0 and len(docs['reviews'])>0):
        results.append(["search_docs","PASS"])
    else:
        results.append(["search_docs","FAIL"])
except Exception:
    results.append(["search_docs","FAIL"])

#delivery issues
#-------------------------------------
try:
    metrics=check_delivery_issues()
    if (metrics["late_orders"]<=metrics["total_delivered_orders"]):
        results.append(["delivery_metrics","PASS"])
    else:
        results.append(["delivery_metrics","FAIL"])
except Exception:
    results.append(["delivery_metrics","FAIL"])

#STATE DELIVERY ISSUES
#-----------------------------------------
try:
    state_results=check_delivery_issues_by_state(top_n=5)
    if len(state_results)==5:
        results.append(["state_analysis","PASS"])
    else:
        results.append(["state_analysis","FAIL"])
except Exception:
    results.append(["state_analysis","FAIL"])

#-----------------------------
report=pd.DataFrame(results,columns=["test_case","status"])
report.to_csv("evaluation/results/mcp_report.csv",index=False)

print("\nMCP EVALUATION")
print("="*50)

print(report)
success_rate = round(((report["status"]== "PASS").sum()/len(report))* 100,2)
print(f"Success Rate :{success_rate}%")