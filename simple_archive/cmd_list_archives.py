from datetime import datetime
import os
from config import ListArchivesConfig
from simple_archive.archive_database import ArchiveDatabase

from rich.console import Console
from rich.table import Table

from simple_archive.common import file_size_format


class ListArchives:
    def __init__(self, config: ListArchivesConfig):
        self.config = config
        self.db = ArchiveDatabase(self.config.database_dir)

    def do(self):
        table = Table(title="Archives")
        table.add_column("Archive Date")
        table.add_column("Name", no_wrap=True)
        table.add_column("Duration")
        table.add_column("Compressed Size")
        table.add_column("Ratio")

        all_archives = self.db.get_all_archives()
        all_archives.sort()

        for archive in all_archives:
            if os.path.isfile(archive) or archive.startswith(".") or archive.startswith("_"):
                continue

            bi = self.db.read_backup_info(archive)
            duration_s = bi.time_end - bi.time_start
            if duration_s > 3600:
                pp_duration = "%.02fh" % (duration_s / 60.0 / 60.0)
            else:
                pp_duration = "%.02fm" % (duration_s / 60.0)

            table.add_row(
                datetime.fromtimestamp(bi.time_start).strftime('%Y-%m-%d %H:%M:%S'),
                archive,
                pp_duration,
                file_size_format(bi.compressed_file_size),
                "%.02f" % (bi.compressed_file_size / bi.original_file_size)
            )

        console = Console()
        console.print(table)
