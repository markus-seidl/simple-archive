import os
import datetime


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
        return os.path.exists(os.path.join(self.database_dir, archive_name, "done"))

    def finish(self, directory):
        with open(os.path.join(self.database_dir, directory, "done"), "w") as f:
            f.write(str(datetime.datetime.now()))
