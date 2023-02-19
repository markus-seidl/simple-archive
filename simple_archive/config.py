from dataclasses import dataclass


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
