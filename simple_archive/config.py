import json
from dataclasses import dataclass, asdict


@dataclass
class ArchiveConfig:
    source_dir: str
    database_dir: str
    password_file: str
    temp_dir: str
    excludes: [str]
    sftp_host: str
    sftp_user: str
    sftp_root_path: str


@dataclass
class DecompressConfig:
    archive_file: str
    dest: str
    password_file: str


@dataclass
class ListArchivesConfig:
    database_dir: str


@dataclass
class BackupInfo:
    time_start: int
    time_end: int
    original_file_size: int
    compressed_file_size: int
    compressed_sha256: str

    def to_json(self):
        return json.dumps(asdict(self))

    @staticmethod
    def from_json(j):
        return BackupInfo(
            time_start=j['time_start'],
            time_end=j['time_end'],
            original_file_size=j['original_file_size'],
            compressed_file_size=j['compressed_file_size'],
            compressed_sha256=j['compressed_sha256']
        )
