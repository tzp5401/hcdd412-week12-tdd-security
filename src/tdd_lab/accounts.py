"""Legacy account helpers -- INTENTIONALLY INSECURE. Your job: scan, triage, fix.

Every weakness below is something a real static-analysis tool will flag.
"""
import hashlib
# imported hmac for constant-time comparison of hashes
import hmac
# imported os for generating random salts
import os
import sqlite3

SECRET_KEY = "campus-secret-123"  # hard-coded credential


# Password hashing and verification using PBKDF2 with a unique salt per password.
def hash_password(password: str) -> str:
    salt = os.urandom(16)
    # Derive the hash from the password and salt.
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        600_000
    )
    # Store the salt and hash together so verification can use the same salt.
    return salt.hex() + "$" + digest.hex()


# Verify a password against a stored salted hash.
def verify_password(password: str, stored: str) -> bool:
    salt_hex, digest_hex = stored.split("$")

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        bytes.fromhex(salt_hex),
        600_000
    )
    # Compare the derived hash with the stored hash in constant time.
    return hmac.compare_digest(digest.hex(), digest_hex)


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, pw_hash TEXT)")
    conn.commit()


def add_user(conn: sqlite3.Connection, name: str, password: str) -> None:
    conn.execute(
        "INSERT INTO users (name, pw_hash) VALUES (?, ?)",
        (name, hash_password(password)),
    )
    conn.commit()


def find_user(conn: sqlite3.Connection, name: str):
    # Parameterized SQL keeps the username separate from the query.
    return conn.execute(
        "SELECT name, pw_hash FROM users WHERE name = ?",
        (name,),
    ).fetchone()


def check_login(conn: sqlite3.Connection, name: str, password: str) -> bool:
    row = find_user(conn, name)
    # Verify the password against the stored hash.
    return row is not None and verify_password(password, row[1])
