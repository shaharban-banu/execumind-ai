"""
Forecast Data Loader.

Provides historical time series used for
forecast model training.
"""

import calendar
import pandas as pd

from database.database import engine
from utils.logger import logger

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
            customer_created_date,
            customer_master_id
        FROM customers
        WHERE customer_created_date IS NOT NULL
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


def remove_incomplete_last_month(df,date_column: str,):
    """
    Remove the most recent month if it contains incomplete data.

    Forecast models require complete historical periods for accurate
    training. This function removes the latest month until the final
    remaining month is complete.

    Args:
        df: DataFrame containing an ``order_date`` column.

    Returns:
        Filtered DataFrame containing only complete months.
    """
    while not df.empty:

        latest = df[date_column].max()

        days = calendar.monthrange(
            latest.year,
            latest.month,
        )[1]

        if latest.day == days:
            break

        logger.info(
            "Removing incomplete month: %s",
            latest.strftime("%Y-%m"),
        )

        period = latest.to_period("M")

        df = df[
            df[date_column].dt.to_period("M") != period
        ]

    return df

def load_time_series(metric: str) -> pd.DataFrame:
    """
    Load historical time series for Prophet.

    Reads raw transactional data from the database, aggregates it into
    monthly values, removes incomplete months, fills missing periods,
    and returns a Prophet-compatible DataFrame.

    Args:
        metric: Forecast metric. Supported values are
            "revenue", "orders", "customers", and "aov".

    Returns:
        DataFrame with columns:
            ds: Monthly timestamp.
            y: Aggregated metric value.

    Raises:
        ValueError: If an unsupported metric is requested.
        RuntimeError: If data loading or preprocessing fails.
    """
    logger.info("Loading time series for metric '%s'.", metric)

    if metric not in RAW_QUERIES:
        raise ValueError(f"Unknown metric: {metric}")
    
    try:
        df = pd.read_sql(RAW_QUERIES[metric], engine)

        logger.debug("Loaded %d rows for metric '%s'.", len(df), metric)
        

        if metric == "customers":

            df["customer_created_date"] = pd.to_datetime(
                df["customer_created_date"]
            )

            df = remove_incomplete_last_month(
                df,
                date_column="customer_created_date",
            )

        else:

            df["order_date"] = pd.to_datetime(
                df["order_date"]
            )

            df = remove_incomplete_last_month(
                df,
                date_column="order_date",
            )

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
                .reset_index(name="y")
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

            df["customer_created_date"] = pd.to_datetime(
                df["customer_created_date"]
            )

            df = remove_incomplete_last_month(
                df,
                date_column="customer_created_date",
            )
           
            ts = (
                df.groupby(
                    pd.Grouper(
                        key="customer_created_date",
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
                .reset_index(name="y")
            )

        if metric == "customers":
            ts.rename(
                columns={
                    "customer_created_date": "ds"
                },
                inplace=True,
            )
        else:
            ts.rename(
                columns={
                    "order_date": "ds"
                },
                inplace=True,
            )

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
    except Exception as exc:
        logger.exception(
            "Failed to load time series for '%s': %s",
            metric,
            exc,
        )
        raise RuntimeError(
            f"Unable to load time series for '{metric}'."
        ) from exc
