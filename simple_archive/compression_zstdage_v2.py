import logging
import os
import subprocess
import time
import re
import tqdm

from config import ArchiveConfig
from common import file_size_format, report_performance_bytes_ratio

from exe_paths import ZSTD, AGE, SHA256SUM, MD5SUM
from compression import Compression


class ZstdAgeV2(Compression):
    """
    This class compresses and encrypts a file in one go.
    Additionally, a hash is also computed.
    """

    def __init__(self, config: ArchiveConfig):
        super().__init__()
        self.all_bytes_read = 0
        self.all_bytes_written = 0
        self.config = config

    def do(self, input_file: str, output_file: str) -> str:
        original_size = os.path.getsize(input_file)
        self.all_bytes_read += original_size

        if os.path.exists(output_file):
            os.remove(output_file)

        zstd_process = subprocess.Popen(
            [ZSTD, "-15", "-T0", input_file, "--stdout"], stdout=subprocess.PIPE
        )
        output_process = subprocess.Popen(
            [AGE, "-e", "-i", self.config.password_file, "-o", output_file], stdin=zstd_process.stdout
        )

        start_piping = time.time()

        with tqdm.tqdm(total=original_size, unit="B", unit_scale=True, unit_divisor=1024) as pbar:
            while True:
                bytes_written = -1
                if os.path.exists(output_file):
                    bytes_written = os.path.getsize(output_file)

                pbar.update(bytes_written - pbar.n)
                pbar.desc = f"Compressing/Encrypting"

                time.sleep(0.1)

                if output_process.poll() is not None:
                    break

            pbar.update(pbar.total - pbar.n)  # make sure we reach 100%, user confusion otherwise

            output_stdout, output_stderr = output_process.communicate()

            if output_process.returncode != 0:
                raise OSError(output_stderr)

        bytes_written = os.path.getsize(output_file)
        logging.info(
            "Compression/Encryption done with " +
            report_performance_bytes_ratio(start_piping, original_size, bytes_written)
        )
        self.all_bytes_written += bytes_written

        os.remove(input_file)

    def overall_compression_ratio(self) -> float:
        return self.all_bytes_read / float(self.all_bytes_written)
