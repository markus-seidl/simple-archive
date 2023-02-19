import os
import logging
import subprocess
from exe_paths import UNZIP, Z7

ZIP_LIST_CMD = '{cmd} -l {zip_file}'
Z7LIST_CMD = '{cmd} l {zip_file}'
SHA256SUM_CMD = '{cmd} {file}'


def get_zip_file_contents(zip_file: str, output_file: str):
    """
    Gets the contents of the tar archive
    """
    cmd = ZIP_LIST_CMD.format(
        cmd=UNZIP,
        zip_file=zip_file
    )
    logging.debug(f"zip list cmd: {cmd}")

    list_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s_out, s_err = list_process.communicate()

    lines = s_out.decode("UTF-8").split(os.linesep)

    with open(output_file, "w") as f:
        for line in lines:
            f.write(line + os.linesep)


def get_7zip_file_contents(zip_file: str, output_file: str):
    """
    Gets the contents of the tar archive
    """
    cmd = Z7LIST_CMD.format(
        cmd=Z7,
        zip_file=zip_file
    )
    logging.debug(f"7zip list cmd: {cmd}")

    list_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s_out, s_err = list_process.communicate()

    lines = s_out.decode("UTF-8").split(os.linesep)

    with open(output_file, "w") as f:
        for line in lines:
            f.write(line + os.linesep)


def sha256_sum(file: str) -> str:
    """
    Returns the sha256 sum of the file
    """
    cmd = SHA256SUM_CMD.format(
        cmd="sha256sum",
        file=file
    )
    logging.debug(f"sha256sum cmd: {cmd}")

    list_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s_out, s_err = list_process.communicate()

    return s_out.decode("UTF-8").split(" ")[0]
