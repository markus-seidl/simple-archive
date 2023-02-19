import os
import time

from config import ArchiveConfig, BackupInfo
from archive_database import ArchiveDatabase
from compression_zstdage_v2 import ZstdAgeV2
from sftp import SFTPUpload
import logging
import util
from tarwrapper import TarWrapper
import threading


def get_single_file(directory: str):
    """
    Returns the single file in the directory
    """
    files = os.listdir(directory)
    valid_files = []
    for file in files:
        if not file.startswith(".") and not file.startswith("_") and os.path.isfile(os.path.join(directory, file)):
            valid_files.append(file)

    if len(valid_files) == 1:
        file_path = os.path.join(directory, valid_files[0])
        if os.path.isfile(file_path):
            return file_path
    return None


class Archive:
    def __init__(self, config: ArchiveConfig):
        self.config = config
        self.tar = TarWrapper()
        self.db = ArchiveDatabase(self.config.database_dir)
        self.compress = ZstdAgeV2(config)
        self.upload = SFTPUpload(config.sftp_host, config.sftp_user, root_server_path=config.sftp_root_path)
        self.last_sha256 = None

    def do(self):
        # get all directories in config.source
        directories = os.listdir(self.config.source_dir)
        directories.sort()

        for directory in directories:
            if os.path.isfile(directory) or directory.startswith(".") or directory.startswith("_"):
                continue
            if self.db.exists_archive_log(directory) and self.db.is_finished(directory):
                logging.info(f"Archive log for {directory} already exists. Skipping.")
                continue

            self.db.create_archive_log(directory)
            archive_time_start = int(time.time())
            logging.info("*" * 80)
            logging.info(f"Archiving directory {directory}")
            input_directory = os.path.join(self.config.source_dir, directory)

            # If there is only one file in the directory, we want to create an index of this file
            self.handle_single_file_contents(input_directory, directory)

            # TAR
            tar_output_file = os.path.join(self.config.temp_dir, directory + ".tar")

            tar_log = self.db.create_file_path_in_archive_log(directory, "tar.log")
            self.tar.compress_directory(input_directory, directory, tar_output_file, tar_log, self.config.excludes)
            self.tar.write_contents_to(
                tar_output_file, self.db.create_file_path_in_archive_log(directory, "tar_contents.txt")
            )

            # Compression
            c_output_file = tar_output_file + ".zst.age"
            tar_file_size = os.path.getsize(tar_output_file)
            self.compress.do(tar_output_file, c_output_file)

            compressed_file_size = os.path.getsize(c_output_file)

            # SHA256 in background
            sha256_future = self.sha256_sum_async(
                c_output_file, self.db.create_file_path_in_archive_log(directory, "sha256_archive.txt")
            )

            # Upload file and delete scratch file
            self.upload.do(c_output_file, os.path.basename(c_output_file))

            # Wait for SHA256 to finish
            if sha256_future.is_alive():
                logging.info("Waiting for SHA256 to finish...")
            sha256_future.join()

            # Delete scratch file
            os.remove(c_output_file)

            backup_info = BackupInfo(
                time_start=archive_time_start,
                time_end=int(time.time()),
                original_file_size=tar_file_size,
                compressed_file_size=compressed_file_size,
                compressed_sha256=self.last_sha256,
            )
            self.last_sha256 = None
            self.db.finish(directory, backup_info)
            logging.info(f"Finished archiving {directory}")

    def sha256_sum_async(self, input_file: str, output_file: str) -> threading.Thread:
        download_thread = threading.Thread(
            target=self.calculate_and_save_sha256, name="Downloader", args=[input_file]
        )
        download_thread.start()
        return download_thread

    def calculate_and_save_sha256(self, input_file: str):
        self.last_sha256 = util.sha256_sum(input_file)

    def handle_single_file_contents(self, src_directory: str, archive_name: str):
        """
        If there is only one file in the directory, we want to create an index of this file if it is a known format
        """
        file = get_single_file(src_directory)
        if file is None:
            return

        out_index_file = "sub_archive_content.txt"
        if file.endswith(".tar"):
            self.tar.write_contents_to(file, self.db.create_file_path_in_archive_log(archive_name, out_index_file))
        elif file.endswith(".zip"):
            util.get_zip_file_contents(file, self.db.create_file_path_in_archive_log(archive_name, out_index_file))
        elif file.endswith(".7z"):
            util.get_7zip_file_contents(file, self.db.create_file_path_in_archive_log(archive_name, out_index_file))
