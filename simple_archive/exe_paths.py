import sys

if sys.platform == "linux":
    TAR = "/usr/bin/tar"
    ZSTD = "/usr/bin/zstd"
    SHA256SUM = "/usr/bin/sha256sum"
    AGE = "/usr/bin/age"
    MD5SUM = "/usr/bin/md5sum"
    UNZIP = "/usr/bin/unzip"
    Z7 = "/usr/bin/7z"
    SHA256SUM = "/usr/bin/sha256sum"
elif sys.platform == "darwin":
    TAR = "/opt/homebrew/bin/gtar"
    ZSTD = "/opt/homebrew/bin/zstd"
    SHA256SUM = "/opt/homebrew/bin/sha256sumß"
    AGE = "/opt/homebrew/bin/age"
    MD5SUM = "/opt/homebrew/bin/md5sum"
    UNZIP = "/usr/bin/unzip"
    Z7 = "/opt/homebrew/bin/7zz"
    SHA256SUM = "/opt/homebrew/bin/sha256sum"
