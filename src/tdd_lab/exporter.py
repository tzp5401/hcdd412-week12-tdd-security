"""Legacy report exporter -- INTENTIONALLY INSECURE."""
import subprocess


def archive_report(filename: str) -> int:
    """Zips a report file without using a shell."""
    return subprocess.call(["zip", "-q", "archive.zip", "--", filename])
