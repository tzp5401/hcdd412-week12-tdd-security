"""Legacy data importer using safer data-only alternatives."""
# imported ast and json for safer data-only alternatives.
import ast
import json


def load_session(blob: bytes):
    # Load JSON data instead of deserializing untrusted bytes.
    return json.loads(blob)


def compute_discount(expression: str):
    # Evaluate Python literals without executing arbitrary code.
    return ast.literal_eval(expression)
