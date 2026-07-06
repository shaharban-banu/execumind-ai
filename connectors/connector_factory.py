"""
Connector Factory.

Returns the correct connector based on the dataset configuration.
"""
from config.settings import CONNECTOR
from connectors.csv_connector import CSVConnector

def get_connector():
    """
    Return the configured connector.

    Returns
    -------
    BaseConnector
    """
    if CONNECTOR.lower()=="csv":
        return CSVConnector()
    raise ValueError(f"unsupported connector : {CONNECTOR}")