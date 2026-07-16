"""
Forecast Data Loader.

Provides historical time series used for
forecast model training.
"""

import calendar
import pandas as pd

from database.database import engine


RAW_QUERIES = {
    "revenue": """
        SELECT
            o.order_date,
            p.payment_value
        FROM orders o
        JOIN payments p
            ON o.order_id = p.order_id
        WHERE o.order_date IS NOT NULL
    """,

    "orders": """
        SELECT
            order_date
        FROM orders
        WHERE order_date IS NOT NULL
    """,

    "customers": """
        SELECT
            o.order_date,
            c.customer_master_id
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE o.order_date IS NOT NULL
    """,

    "aov": """
        SELECT
            o.order_date,
            p.payment_value
        FROM orders o
        JOIN payments p
            ON o.order_id = p.order_id
        WHERE o.order_date IS NOT NULL
    """,
}


def remove_incomplete_last_month(df):
    while not df.empty:

        latest = df["order_date"].max()

        days = calendar.monthrange(
            latest.year,
            latest.month,
        )[1]

        if latest.day == days:
            break

        print(
            f"Removing incomplete month: "
            f"{latest.strftime('%Y-%m')}"
        )

        period = latest.to_period("M")

        df = df[
            df["order_date"].dt.to_period("M") != period
        ]

    return df

def load_time_series(metric: str) -> pd.DataFrame:
    """
    Load historical time series for Prophet.
    """

    if metric not in RAW_QUERIES:
        raise ValueError(f"Unknown metric: {metric}")

    df = pd.read_sql(RAW_QUERIES[metric], engine)

    print(df)
    print(df.shape)
    

    df["order_date"] = pd.to_datetime(df["order_date"])

    df = remove_incomplete_last_month(df)

    # --------------------------------------------------
    # Aggregate monthly
    # --------------------------------------------------

    if metric == "revenue":

        ts = (
            df.groupby(
                pd.Grouper(
                    key="order_date",
                    freq="MS",
                )
            )["payment_value"]
            .sum()
            .reset_index(name='y')
        )

    elif metric == "orders":

        ts = (
            df.groupby(
                pd.Grouper(
                    key="order_date",
                    freq="MS",
                )
            )
            .size()
            .reset_index(name="y")
        )

    elif metric == "customers":

        ts = (
            df.groupby(
                pd.Grouper(
                    key="order_date",
                    freq="MS",
                )
            )["customer_master_id"]
            .nunique()
            .reset_index(name="y")
        )

    elif metric == "aov":

        ts = (
            df.groupby(
                pd.Grouper(
                    key="order_date",
                    freq="MS",
                )
            )["payment_value"]
            .mean()
            .reset_index(name='y')
        )

    ts.rename(columns={"order_date": "ds"}, inplace=True)

    ts = ts.sort_values("ds").reset_index(drop=True)

    # -------------------------------------------------
    # Ensure every month exists
    # -------------------------------------------------

    full_months = pd.date_range(
        start=ts["ds"].min(),
        end=ts["ds"].max(),
        freq="MS",
    )

    ts = (
        ts.set_index("ds")
          .reindex(full_months)
          .rename_axis("ds")
          .reset_index()
    )

    if metric == "aov":
        ts["y"] = ts["y"].ffill().bfill()
    else:
        ts["y"] = ts["y"].fillna(0)

    return ts

    return ts