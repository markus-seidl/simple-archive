import logging

import argparse
import datetime
import os

from config import ArchiveConfig, DecompressConfig
from cmd_archive import Archive
from cmd_decompress import Decompress

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO, datefmt='%I:%M:%S')


def do():
    parser = argparse.ArgumentParser(prog="simple_archive")
    parser.add_argument("--database", help="Database directory", default="./db")
    subparsers = parser.add_subparsers(help="commands", dest="command")

    archive = subparsers.add_parser("archive")
    archive.add_argument("--source", help="Source directory", required=True)
    archive.add_argument("--sftp-host", required=True)
    archive.add_argument("--sftp-user", required=True)
    archive.add_argument("--sftp-root-path", default="/archive")
    archive.add_argument(
        "--password-file", help="Password for file encryption in plain text as file", default="./password.age"
    )
    archive.add_argument("--tempdir", help="Store tar output", default="./temp")
    archive.add_argument(
        "--exclude", help="tar exclude option", default=None, required=False, action='append', nargs='+'
    )

    decompress = subparsers.add_parser("decompress")
    decompress.add_argument("--archive-file", help="File to decrypt and decompress", required=True)
    decompress.add_argument("--dest", help="Dest directory", required=True)
    decompress.add_argument("--password-file", help="Password in plain text as file", default="./password.age")

    args = parser.parse_args()

    if args.command == 'archive':
        do_archive(args)
    elif args.command == "decompress":
        do_decompress(args)
    else:
        parser.print_help()


def do_archive(args):
    config = ArchiveConfig(
        source_dir=args.source,
        database_dir=args.database,
        password_file=args.password_file,
        temp_dir=args.tempdir,
        excludes=args.exclude,
        sftp_host=args.sftp_host,
        sftp_user=args.sftp_user,
        sftp_root_path=args.sftp_root_path
    )

    Archive(config).do()


def do_decompress(args):
    config = DecompressConfig(
        archive_file=args.archive_file,
        dest=args.dest,
        password_file=args.password_file
    )

    Decompress(config).do()


if __name__ == '__main__':
    do()
