import logging
import os
from tqdm import tqdm
import paramiko
import common


class SFTPUpload:
    def __init__(
            self, host: str, username: str, port: int = 22, root_server_path: str = "",
            key_filename: str = "~/.ssh/id_rsa"
    ):
        self.host = host
        self.port = port
        self.username = username
        self.root_server_path = root_server_path
        self.key_filename = key_filename

    def do(self, input_file: str, output_filename: str, delete_after_upload: bool = False):
        with paramiko.SSHClient() as ssh:
            ssh.load_system_host_keys()

            ssh.connect(
                self.host, port=self.port, username=self.username, key_filename=os.path.expanduser(self.key_filename)
            )

            sftp = ssh.open_sftp()

            sftp.chdir(self.root_server_path)

            if output_filename in sftp.listdir(self.root_server_path):
                s = sftp.stat(self.root_server_path + "/" + output_filename)
                logging.warning(
                    f"File {self.root_server_path + '/' + output_filename} already exists on server. "
                    f"Assuming the upload is incomplete/corrupt. Overwriting file with size "
                    f"{common.file_size_format(s.st_size)} with new file with size "
                    f"{common.file_size_format(os.path.getsize(input_file))}"
                )

            with tqdm(total=os.path.getsize(input_file), unit="B", unit_scale=True, unit_divisor=1024) as pbar:
                sftp.put(
                    input_file, output_filename,
                    callback=lambda sent, size: self._callback(pbar, output_filename, sent, size)
                )

        if delete_after_upload:
            os.remove(input_file)

    def _callback(self, pbar, filename: str, sent: int, size: int):
        pbar.total = size
        pbar.update(sent - pbar.n)
        pbar.desc = f"Uploading {filename}"


if __name__ == "__main__":
    temp = SFTPUpload("u338984.your-storagebox.de", "u338984", root_server_path="/archive", port=22)
    temp.do("cli.py", "run.sh")
