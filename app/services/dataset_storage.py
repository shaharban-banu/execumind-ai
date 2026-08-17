from pathlib import Path


BASE_DIR = Path("data/users")


def get_dataset_version_dir(
    user_id: int,
    dataset_name: str,
    version_number: int,
) -> Path:
    """
    Return the storage directory for a specific dataset version.

    The directory is organized by user, dataset, and version
    to prevent files belonging to different users or versions
    from being mixed.

    Args:
        user_id: ID of the dataset owner.
        dataset_name: Logical name of the dataset.
        version_number: Version number of the dataset.

    Returns:
        Path to the dataset version directory.
    """

    return (
        BASE_DIR
        / str(user_id)
        / "datasets"
        / dataset_name
        / f"v{version_number}"
    )


def create_dataset_version_dir(
    user_id: int,
    dataset_name: str,
    version_number: int,
) -> Path:
    """
    Create and return the storage directory for a dataset version.

    The directory is created recursively if it does not already exist.

    Args:
        user_id: ID of the dataset owner.
        dataset_name: Logical name of the dataset.
        version_number: Version number of the dataset.

    Returns:
        Path to the created dataset version directory.
    """

    directory = get_dataset_version_dir(
        user_id,
        dataset_name,
        version_number,
    )

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory