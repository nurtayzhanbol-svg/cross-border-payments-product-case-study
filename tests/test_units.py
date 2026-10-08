import numpy as np
import pandas as pd

from rpw.harmonise import access_digital, parse_date, payout_group, provider_type_group, to_numeric
from rpw.providers import build_provider_map


def test_to_numeric_flags_semantic_strings_but_not_blanks():
    vals, failed = to_numeric(pd.Series([1, "2.5", "", " 3 ", "N/A", None], dtype=object))
    assert vals.iloc[1] == 2.5 and vals.iloc[3] == 3.0
    assert np.isnan(vals.iloc[2]) and np.isnan(vals.iloc[4])
    assert failed.tolist() == [False, False, False, False, True, False]


def test_parse_date_handles_text_and_datetimes():
    out = parse_date(pd.Series(["24/Jan/2011", pd.Timestamp("2025-02-03"), "", "bad"], dtype=object))
    assert out.iloc[0] == pd.Timestamp("2011-01-24")
    assert out.iloc[1] == pd.Timestamp("2025-02-03")
    assert out.iloc[2:].isna().all()


def test_provider_map_folds_case_space_and_aliases():
    m = build_provider_map(pd.Series(["Azimo", "azimo", "Azimo", "Transferwise", "Wise", "Western  Union"]))
    d = dict(zip(m.firm_raw, m.firm))
    assert d["azimo"] == "Azimo"
    assert d["Transferwise"] == "Wise"
    assert d["Western  Union"] == "Western Union"
    assert set(m.firm_raw) == {"Azimo", "azimo", "Transferwise", "Wise", "Western  Union"}


def test_category_groupings():
    assert payout_group("Cash") == "cash"
    assert payout_group("Cash, Bank Account") == "multiple"
    assert payout_group("") is np.nan or pd.isna(payout_group(""))
    assert access_digital("Not available") == (np.nan, np.nan) or pd.isna(access_digital("Not available")[0])
    assert access_digital("Internet") == (True, True)
    assert access_digital("Agent,Internet") == (True, False)
    assert provider_type_group("Bank / Money Transfer Operator") == "Mixed / multiple types"
    assert provider_type_group("Money Transfer Operator") == "Money transfer operator"
