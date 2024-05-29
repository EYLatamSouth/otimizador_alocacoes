from __future__ import annotations

import shutil
from datetime import datetime, timedelta
from pathlib import Path

import allocpro.config as cfg


def create_backup_folder() -> Path:
    """Create the `./Backup` folder if it doesn't exist.

    Returns
    -------
    Path
        The folder path where previous execution outputs will be moved to.
    """
    backup_folder = Path(cfg.BACKUP_FOLDER)
    backup_folder.mkdir(exist_ok=True, parents=True)
    return backup_folder


def create_timestamped_folder(backup_folder: str | Path) -> Path:
    # Create a timestamped folder inside Backup folder
    current_time = datetime.now().strftime("%Y-%m-%d %Hh_%Mm")
    timestamped_folder = Path(backup_folder).joinpath(current_time)
    timestamped_folder.mkdir(exist_ok=True, parents=True)
    return timestamped_folder


def move_files_to_backup(source_folder: str | Path, dest_folder: str | Path):
    """Move files from source folder to destination folder.

    Parameters
    ----------
    source_folder : str | Path
        The source folder path to move files from.
    dest_folder : str | Path
        The folder path to move files to.

    Notes
    -----
    This function moves files from every child directory of `source_folder`
    keeping the same underlying folder structure.
    """
    source_folder = Path(source_folder)
    dest_folder = Path(dest_folder)
    dest_folder.mkdir(exist_ok=True, parents=True)

    filenames = list(source_folder.glob("**/*"))

    if not source_folder.is_dir() or not filenames:
        return

    for filename in filenames:
        dest_filepath = dest_folder.joinpath(filename.relative_to(source_folder))
        dest_filepath.parent.mkdir(exist_ok=True, parents=True)
        try:
            shutil.move(filename, dest_filepath)
        except PermissionError as exc:
            print(f"PermissionError: {exc}. Skipping file: {filename}")
        except Exception as exc:
            print(f"Error: {exc}. Skipping file: {filename}")


def is_folder_not_empty(folder_path: Path | str) -> bool:
    folder_path = Path(folder_path)
    filenames = list(folder_path.glob("**/*"))
    return folder_path.is_dir() and filenames


def backup_staging_and_outputs():
    # Define source folders
    staging_folder = Path(cfg.STAGING_FOLDER)
    outputs_folder = Path(cfg.OUTPUTS_FOLDER)

    # Create Backup folder
    backup_folder = create_backup_folder()

    staging_not_empty = is_folder_not_empty(staging_folder)
    outputs_not_empty = is_folder_not_empty(outputs_folder)

    # If both folders are empty or don't exist, no need to create timestamped folder
    if not staging_not_empty and not outputs_not_empty:
        print("Both Staging and Outputs folders are empty or don't exist. No backup needed.")
        return

    # Create a timestamped folder inside Backup folder
    timestamped_folder = create_timestamped_folder(backup_folder)

    # Move files from Staging and Outputs to the respective folders in the timestamped folder
    if staging_not_empty:
        move_files_to_backup(staging_folder, timestamped_folder.joinpath(staging_folder.name))
    if outputs_not_empty:
        move_files_to_backup(outputs_folder, timestamped_folder.joinpath(outputs_folder.name))

    staging_folder.mkdir(exist_ok=True, parents=True)
    outputs_folder.mkdir(exist_ok=True, parents=True)

    print(f"Backup completed successfully at '{timestamped_folder}'")


def cleanup_old_backups(
    backup_folder: str | Path = cfg.BACKUP_FOLDER,
    days: int = cfg.BACKUP_FOLDERS_PERSISTENCE,
):
    """
    Remove folders in the backup directory that are older than a specified number of days.

    Parameters
    ----------
    backup_folder : str | Path, default='./Backups'
        The backup folder path to clean up.
    days : int, default=31
        The number of days to keep backups. Folders older than this will be deleted.
    """
    backup_folder = Path(backup_folder)
    cutoff_date = datetime.now() - timedelta(days=days)

    for folder in backup_folder.iterdir():
        if folder.is_dir():
            creation_time = datetime.fromtimestamp(folder.stat().st_ctime)
            if creation_time < cutoff_date:
                try:
                    shutil.rmtree(folder)
                    print(f"Deleted old backup folder: {folder}")
                except Exception as exc:
                    print(f"Error deleting folder {folder}: {exc}")


if __name__ == "__main__":
    # Run the backup process
    backup_staging_and_outputs()
    cleanup_old_backups()
