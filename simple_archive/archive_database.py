import json
import os
import datetime
import typing

from config import BackupInfo


class ArchiveDatabase:
    def __init__(self, database_dir: str):
        self.database_dir = database_dir

    def create_archive_log(self, archive_name: str):
        os.makedirs(self.database_dir, exist_ok=True)
        os.makedirs(os.path.join(self.database_dir, archive_name), exist_ok=True)

    def create_file_path_in_archive_log(self, archive_name: str, file_name: str):
        return os.path.join(self.database_dir, archive_name, file_name)

    def exists_archive_log(self, archive_name: str):
        return os.path.exists(os.path.join(self.database_dir, archive_name))

    def is_finished(self, archive_name: str):
        return os.path.exists(os.path.join(self.database_dir, archive_name, "info.json"))

    def finish(self, archive_name, backup_info: BackupInfo):
        with open(os.path.join(self.database_dir, archive_name, "info.json"), "w") as f:
            f.write(backup_info.to_json())

    def get_all_archives(self):
        return os.listdir(self.database_dir)

    def read_backup_info(self, archive_name: str) -> typing.Optional[BackupInfo]:
        info_file = self.create_file_path_in_archive_log(archive_name, "info.json")
        if not os.path.exists(info_file):
            return None

        with open(info_file, "r") as f:
            return BackupInfo.from_json(json.load(f))
