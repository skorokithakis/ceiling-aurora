#!/usr/bin/env python3
"""Build the compact star catalogue used by the ceiling visualization."""

import csv
import gzip
import io
import sys
from pathlib import Path
from urllib.request import urlopen


SOURCE_URL = (
    "https://raw.githubusercontent.com/astronexus/HYG-Database/main/"
    "hyg/CURRENT/hygdata_v41.csv"
)
MAGNITUDE_LIMIT = 6.0
OUTPUT_PATH = Path(__file__).with_name("stars.js")


def format_number(value: float, decimals: int) -> str:
    """Keep the requested precision without storing insignificant zeroes."""
    return f"{value:.{decimals}f}".rstrip("0").rstrip(".")


def download_catalogue() -> io.TextIOWrapper:
    with urlopen(SOURCE_URL) as response:
        data = response.read()

    # Current HYG v4.1 is plain CSV; retain gzip support for a future catalogue
    # release without relying on the URL extension.
    if data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    return io.TextIOWrapper(io.BytesIO(data), encoding="utf-8", newline="")


def make_stars() -> list[tuple[float, float, float]]:
    with download_catalogue() as catalogue:
        reader = csv.DictReader(catalogue)
        stars = [
            (float(row["ra"]), float(row["dec"]), magnitude)
            for row in reader
            if (magnitude := float(row["mag"])) <= MAGNITUDE_LIMIT
            and row.get("proper", "").strip().lower() not in {"sun", "sol"}
        ]
    return stars


def render(stars: list[tuple[float, float, float]]) -> str:
    records = ",\n".join(
        "  ["
        f"{format_number(ra, 3)},"
        f"{format_number(dec, 3)},"
        f"{format_number(magnitude, 2)}"
        "]"
        for ra, dec, magnitude in stars
    )
    return f"const STARS = [\n{records}\n];\n"


def main() -> None:
    stars = make_stars()
    output = render(stars)
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(output, encoding="utf-8")
    else:
        OUTPUT_PATH.write_text(output, encoding="utf-8")
    print(f"Wrote {len(stars)} stars", file=sys.stderr)


if __name__ == "__main__":
    main()
