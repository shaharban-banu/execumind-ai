"""
Abstract base connector.

Every connector (CSV, MySQL, PostgreSQL, API, etc.)
must implement the load_tables() method.
"""

from abc import ABC,abstractmethod
from pandas import DataFrame

class BaseConnector(ABC):
    """Base class for all connectors"""

    @abstractmethod
    def load_tables(self):
        """load all configured tables"""
        raise NotImplementedError
    