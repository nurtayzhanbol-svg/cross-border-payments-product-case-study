"""Provider-name normalisation. Raw names are never overwritten."""
import pandas as pd

from .config import PROVIDER_ALIASES


def clean_name(value):
    return " ".join(str(value).split())


def provider_key(value):
    key = clean_name(value).casefold()
    return PROVIDER_ALIASES.get(key, key).casefold()


def build_provider_map(firm_raw: pd.Series) -> pd.DataFrame:
    """Map each raw firm string to a canonical display name.

    Rule: fold case and whitespace, apply explicit aliases, then use the alias target or the most
    frequent cleaned spelling within the key (ties broken alphabetically).
    """
    counts = firm_raw.map(clean_name).value_counts().rename_axis("firm_clean").reset_index(name="rows")
    counts["firm_key"] = counts["firm_clean"].map(provider_key)
    alias_targets = {v.casefold(): v for v in PROVIDER_ALIASES.values()}
    canon = (counts.sort_values(["firm_key", "rows", "firm_clean"], ascending=[True, False, True])
             .groupby("firm_key")["firm_clean"].first())
    canon.update(pd.Series(alias_targets).reindex(canon.index).dropna())
    raw = pd.DataFrame({"firm_raw": firm_raw.drop_duplicates().values})
    raw["firm_clean"] = raw["firm_raw"].map(clean_name)
    raw["firm_key"] = raw["firm_clean"].map(provider_key)
    raw["firm"] = raw["firm_key"].map(canon)
    raw["firm_changed"] = raw["firm"] != raw["firm_raw"]
    variants = raw.groupby("firm_key")["firm_raw"].transform("nunique")
    raw["n_raw_variants"] = variants
    return raw.sort_values(["firm", "firm_raw"]).reset_index(drop=True)
