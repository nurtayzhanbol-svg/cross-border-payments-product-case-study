"""Schema harmonisation and type conversion. One output row per input row, always."""
import re

import numpy as np
import pandas as pd

from . import config
from .providers import build_provider_map

INCOME_MAP = {
    "High income: OECD": "High income",
    "High income: nonOECD": "High income",
    "Lower income": "Low income",
}
SPEED_MAP = {"less than one hour": "Less than one hour", "Next Day": "Next day", "N/A": np.nan}
DIGITAL_TOKENS = ("on-line", "internet", "mobile phone", "on mobile phone")


def _blank_to_nan(s):
    return s.map(lambda v: np.nan if (isinstance(v, str) and v.strip() == "") else v)


def to_numeric(s):
    """Coerce to float. Returns (values, parse_failed) where parse_failed marks non-blank values
    that could not be parsed (e.g. semantic strings)."""
    s2 = _blank_to_nan(s).map(lambda v: v.strip() if isinstance(v, str) else v)
    out = pd.to_numeric(s2, errors="coerce").astype(float)
    return out, s2.notna() & out.isna()


def parse_date(s):
    def one(v):
        if isinstance(v, pd.Timestamp) or hasattr(v, "year"):
            return pd.Timestamp(v)
        if isinstance(v, str) and v.strip():
            return pd.to_datetime(v.strip(), format="%d/%b/%Y", errors="coerce")
        return pd.NaT
    return pd.to_datetime(s.map(one))


def split_tokens(v):
    if not isinstance(v, str) or not v.strip():
        return []
    return [t.strip().lower() for t in v.split(",") if t.strip()]


def payout_group(v):
    toks = split_tokens(v)
    if not toks:
        return np.nan
    groups = set()
    for t in toks:
        if "cash" in t:
            groups.add("cash")
        elif "account" in t:
            groups.add("bank account")
        elif "mobile" in t:
            groups.add("mobile wallet")
        elif "home" in t:
            groups.add("home delivery")
        elif "atm" in t:
            groups.add("atm")
        elif "card" in t:
            groups.add("card")
        else:
            groups.add("other")
    return groups.pop() if len(groups) == 1 else "multiple"


def access_digital(v):
    toks = split_tokens(v)
    if not toks or toks == ["not available"]:
        return np.nan, np.nan
    dig = [any(d in t for d in DIGITAL_TOKENS) for t in toks]
    return any(dig), all(dig)


def provider_type_group(v):
    s = clean = " ".join(str(v).split()).lower()
    if "/" in clean:
        return "Mixed / multiple types"
    return {
        "bank": "Bank",
        "money transfer operator": "Money transfer operator",
        "post office": "Post office",
        "mobile operator": "Mobile operator",
        "non-bank fi": "Non-bank financial institution",
        "credit union": "Credit union",
    }.get(s, "Other")


def harmonise_sheet(df, sheet):
    rename = dict(config.COMMON_RENAME)
    rename.update(config.PRE_ONLY_RENAME if sheet == "PRE" else config.POST_ONLY_RENAME)
    missing = set(rename) - set(df.columns)
    if missing:
        raise ValueError(f"{sheet}: missing columns {sorted(missing)}")
    out = df[list(rename)].rename(columns=rename).copy()
    out.insert(0, "sheet", sheet)
    out.insert(1, "source_row", np.arange(2, len(df) + 2))
    return out


def harmonise(raw):
    frames = [harmonise_sheet(raw["PRE"], "PRE"), harmonise_sheet(raw["POST"], "POST")]
    df = pd.concat(frames, ignore_index=True, sort=False)
    df["record_id"] = df["record_id"].astype(str).str.strip()
    df["record_key"] = df["sheet"] + ":" + df["period"] + ":" + df["record_id"]

    p = df["period"].str.extract(r"^(\d{4})_(\d)Q$")
    df["year"] = p[0].astype(int)
    df["quarter"] = p[1].astype(int)
    df["period_start"] = pd.to_datetime(dict(year=df["year"], month=3 * (df["quarter"] - 1) + 1, day=1))

    for col in config.NUMERIC_FIELDS:
        df[col], df[f"{col}__parse_failed"] = to_numeric(df[col])
    for col in [c for c in df.columns if df[c].dtype == object]:
        df[col] = df[col].map(lambda v: v.strip() if isinstance(v, str) else v)
    df["collection_date"] = parse_date(df["date_raw"])
    df["date_raw"] = df["date_raw"].astype(str)

    df["transparent_norm"] = df["transparent_raw"].str.lower()
    df["speed"] = df["speed_raw"].replace(SPEED_MAP)
    df["firm_type"] = df["firm_type_raw"].str.replace("Post Office", "Post office", regex=False)
    df["provider_type"] = df["firm_type"].map(provider_type_group)
    for side in ("source", "destination"):
        df[f"{side}_income_harmonised"] = df[f"{side}_income"].replace(INCOME_MAP)
    df["corridor_key"] = df["source_code"] + df["destination_code"]

    pmap = build_provider_map(df["firm_raw"])
    df["firm"] = df["firm_raw"].map(pmap.set_index("firm_raw")["firm"])

    df["payout_method_group"] = np.where(df["sheet"] == "PRE", df["pickup_method_pre"].map(payout_group),
                                         df["pickup_method_post"].map(payout_group))
    acc = np.where(df["sheet"] == "PRE", df["sending_location_pre"], df["access_point_post"])
    dig = [access_digital(v) for v in acc]
    df["access_has_digital"] = pd.array([d[0] for d in dig], dtype="boolean")
    df["access_digital_only"] = pd.array([d[1] for d in dig], dtype="boolean")

    notes = df[["note1_pre", "standard_note_post", "note2"]].fillna("").astype(str).agg(" | ".join, axis=1)
    df["note_text"] = notes.str.strip(" |")
    return df, pmap


NOT_TRANSPARENT_RE = re.compile(r"not\s+transparent|non[- ]?transparent", re.I)
DISCLAIMER_RE = re.compile(r"does\s+not\s+necessarily\s+mean", re.I)
