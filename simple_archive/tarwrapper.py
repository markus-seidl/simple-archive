import subprocess
import logging
import threading
import os
import time

from base_wrapper import Wrapper
from exe_paths import TAR
from common import file_size_format, report_performance_bytes

COMPRESS_TAR_BACKUP_FULL_CMD = \
    '{cmd} cv {excludes} ' \
    '--label="{backup_name}" ' \
    ' -f {output_file} ' \
    ' {source} > {tar_log_file} 2>&1 '

LIST_CMD = '{cmd} tvf {tar_file}'


class TarWrapper(Wrapper):
    def __init__(self):
        super().__init__()

    def compress_directory(
            self, directory: str, backup_name: str, output_file: str, tar_log_file: str, excludes: [str] = None
    ):
        exclude_cmd = ""
        if excludes:
            for exclude in excludes:
                exclude_cmd += f' --exclude "{exclude[0]}"'

        cmd = COMPRESS_TAR_BACKUP_FULL_CMD.format(
            cmd=TAR,
            excludes="",
            backup_name=backup_name,
            output_file=output_file,
            source=directory,
            tar_log_file=tar_log_file
        )
        logging.debug(f"Running command: {cmd}")
        p = subprocess.Popen(cmd, shell=True)

        start_piping = time.time()
        last_report_time = start_piping

        while True:
            bytes_written = -1
            if os.path.exists(output_file):
                bytes_written = os.path.getsize(output_file)

            if time.time() - last_report_time >= 1 and bytes_written > 0:
                last_report_time = time.time()
                logging.info(f"Tar written {file_size_format(bytes_written)}")

            time.sleep(0.1)

            if p.poll() is not None:
                break

        output_stdout, output_stderr = p.communicate()

        if p.returncode != 0:
            raise OSError(output_stderr)

        bytes_written = os.path.getsize(output_file)
        logging.info("Tar done with " + report_performance_bytes(start_piping, bytes_written))

    def write_contents_to(self, tar_file: str, output_file: str):
        """
        Gets the contents of the tar archive
        """
        tar_cmd = LIST_CMD.format(
            cmd=TAR,
            tar_file=tar_file
        )
        logging.debug(f"tar list cmd: {tar_cmd}")

        list_process = subprocess.Popen(tar_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        s_out, s_err = list_process.communicate()

        lines = s_out.decode("UTF-8").split(os.linesep)

        with open(output_file, "w") as f:
            for line in lines:
                f.write(line + os.linesep)
