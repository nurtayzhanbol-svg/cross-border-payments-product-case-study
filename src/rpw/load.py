"""Load the raw workbook without modifying it and verify its integrity."""
import hashlib

import pandas as pd

from . import config


def sha256(path=config.RAW_WORKBOOK):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_raw(path=config.RAW_WORKBOOK):
    digest = sha256(path)
    if digest != config.RAW_SHA256:
        raise ValueError(f"Raw workbook hash mismatch: {digest}")
    return digest


def read_sheet(sheet, path=config.RAW_WORKBOOK):
    """Read a data sheet as raw cell values (cached formula results), no NA inference.

    `keep_default_na=False` keeps literal strings such as `N/A` and `..` intact.
    Unlabeled helper columns (POST AQ–AU) are dropped here and documented in docs/pipeline.md.
    """
    df = pd.read_excel(path, sheet_name=sheet, dtype=object, keep_default_na=False, na_filter=False,
                       engine="openpyxl")
    return df.loc[:, [c for c in df.columns if not str(c).startswith("Unnamed")]]


def load_raw(use_cache=True):
    """Return {"PRE": df, "POST": df}. Caches a pickle in data/interim keyed by the raw hash."""
    digest = verify_raw()
    cache = config.CACHE_DIR / f"raw_{digest[:12]}.pkl"
    if use_cache and cache.exists():
        return pd.read_pickle(cache)
    sheets = {"PRE": read_sheet(config.SHEET_PRE), "POST": read_sheet(config.SHEET_POST)}
    for name, df in sheets.items():
        if len(df) != config.EXPECTED_ROWS[name]:
            raise ValueError(f"{name}: expected {config.EXPECTED_ROWS[name]} rows, got {len(df)}")
    config.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    pd.to_pickle(sheets, cache)
    return sheets
