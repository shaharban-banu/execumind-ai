"""
scanner.py

Scans uploaded datasets and loads supported files into memory.
Supported formats:
- CSV
- Excel (.xlsx, .xls)
- JSON

This module does not perform any analysis or transformation.
"""
from __future__ import annotations
from pathlib import Path
from utils.logger import logger
import pandas as pd
from ingestion.models.dataset import DatasetMetadata
from ingestion.models.tables import TableMetadata

class DatasetScanner:
    """
    Scans a dataset directory or file and creates DatasetMetadata.
    """

    SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".json"}

    def scan(self, path: str) -> DatasetMetadata:
        """
        Scan a dataset file or directory.

        Loads all supported dataset files into memory and constructs
        a DatasetMetadata object containing the discovered tables.

        Args:
            path: Path to a dataset file or directory.

        Returns:
            DatasetMetadata representing the scanned dataset.

        Raises:
            FileNotFoundError: If the supplied path does not exist.
            ValueError: If no supported files are found or an
                unsupported file type is encountered.
            RuntimeError: If dataset scanning fails.
        """
        dataset_path = Path(path)

        if not dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")

        logger.info("Starting dataset scan: %s", dataset_path)

        try:

            if dataset_path.is_dir():
                tables = self._scan_directory(dataset_path)
                file_type = "directory"
            else:
                tables = [self._scan_file(dataset_path)]
                file_type = dataset_path.suffix.lower().replace(".", "")

            dataset = DatasetMetadata(
                dataset_name=dataset_path.stem,
                source_path=str(dataset_path),
                file_type=file_type,
                tables=tables,
            )

            logger.info(
                "Dataset scan completed. Loaded %d table(s).",
                len(dataset.tables),
            )

            return dataset
        except Exception as exc:
            logger.exception(
                "Dataset scan failed: %s",
                exc,
            )
            raise RuntimeError(
                "Failed to scan dataset."
            ) from exc

    def _scan_directory(self, directory: Path) -> list[TableMetadata]:
        """
        Scan all supported dataset files in a directory.

        Args:
            directory: Directory containing dataset files.

        Returns:
            List of discovered table metadata objects.

        Raises:
            ValueError: If the directory contains no supported files.
        """
        tables = []

        for file in sorted(directory.iterdir()):
            if file.is_file() and file.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                logger.info("Loading %s", file.name)
                tables.append(self._scan_file(file))

        if not tables:
            raise ValueError("No supported dataset files found.")

        return tables

    def _scan_file(self, file_path: Path) -> TableMetadata:
        """
        Scan a single dataset file.

        Reads the file into a DataFrame and creates the initial
        table metadata.

        Args:
            file_path: Dataset file to load.

        Returns:
            Table metadata containing the loaded DataFrame.

        Raises:
            ValueError: If the file type is unsupported.
        """
        suffix = file_path.suffix.lower()

        if suffix == ".csv":
            dataframe = self._read_csv(file_path)

        elif suffix in {".xlsx", ".xls"}:
            dataframe = self._read_excel(file_path)

        elif suffix == ".json":
            dataframe = self._read_json(file_path)

        else:
            raise ValueError(f"Unsupported file type: {suffix}")

        return self._create_table_metadata(
            table_name=file_path.stem,
            dataframe=dataframe,
        )

    @staticmethod
    def _read_csv(path: Path) -> pd.DataFrame:
        """
        Read a CSV file.
        """
        return pd.read_csv(path)

    @staticmethod
    def _read_excel(path: Path) -> pd.DataFrame:
        """
        Read an Excel file.
        """
        return pd.read_excel(path)

    @staticmethod
    def _read_json(path: Path) -> pd.DataFrame:
        """
        Read a JSON file.
        """
        return pd.read_json(path)

    @staticmethod
    def _create_table_metadata(
        table_name: str,
        dataframe: pd.DataFrame,
    ) -> TableMetadata:
        """
        Create initial table metadata from a DataFrame.

        Args:
            table_name: Name of the dataset table.
            dataframe: Loaded dataset.

        Returns:
            TableMetadata instance.
        """
        return TableMetadata(
            table_name=table_name,
            row_count=len(dataframe),
            dataframe=dataframe,
        )