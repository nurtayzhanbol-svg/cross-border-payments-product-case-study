from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_WORKBOOK = ROOT / "data" / "raw" / "rpw_dataset_2011_2025_q3.xlsx"
RAW_SHA256 = "f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8"
PROCESSED_DIR = ROOT / "data" / "processed"
CACHE_DIR = ROOT / "data" / "interim"

SHEET_PRE = "Dataset (up to Q1 2016)"
SHEET_POST = "Dataset (from Q2 2016)"
EXPECTED_ROWS = {"PRE": 49_491, "POST": 204_469}

AMOUNTS = {"cc1": 200, "cc2": 500}
COST_TOLERANCE_PP = 0.01
EXTREME_TOTAL_COST_PCT = 50.0
SDG_TARGET_PCT = 3.0
G20_TARGET_PCT = 5.0

COMMON_RENAME = {
    "id": "record_id",
    "period": "period",
    "source_code": "source_code",
    "source_name": "source_name",
    "source_region": "source_region",
    "source_income": "source_income",
    "source_lending": "source_lending",
    "source_G8G20": "source_g8g20",
    "destination_code": "destination_code",
    "destination_name": "destination_name",
    "destination_region": "destination_region",
    "destination_income": "destination_income",
    "destination_lending": "destination_lending",
    "destination_G8G20": "destination_g8g20",
    "firm": "firm_raw",
    "firm_type": "firm_type_raw",
    "speed actual": "speed_raw",
    "inter lcu bank fx": "interbank_fx_rate",
    "transparent": "transparent_raw",
    "note2": "note2",
    "date": "date_raw",
    "corridor": "corridor_raw",
}
for _cc in AMOUNTS:
    COMMON_RENAME.update({
        f"{_cc} lcu amount": f"{_cc}_lcu_amount",
        f"{_cc} denomination amount": f"{_cc}_denomination_usd",
        f"{_cc} lcu code": f"{_cc}_lcu_code",
        f"{_cc} lcu fee": f"{_cc}_lcu_fee",
        f"{_cc} lcu fx rate": f"{_cc}_applied_fx_rate",
        f"{_cc} fx margin": f"{_cc}_fx_margin_pct",
        f"{_cc} total cost %": f"{_cc}_total_cost_pct",
    })

PRE_ONLY_RENAME = {
    "product": "product_pre",
    "sending location": "sending_location_pre",
    "note1": "note1_pre",
    "coverage": "coverage_pre",
    "pick-up method": "pickup_method_pre",
}
POST_ONLY_RENAME = {
    "payment instrument": "payment_instrument_post",
    "access point": "access_point_post",
    "Standard Note": "standard_note_post",
    "receiving network coverage": "receiving_network_coverage_post",
    "pickup location": "pickup_location_post",
    "pickup method": "pickup_method_post",
}

NUMERIC_FIELDS = ["interbank_fx_rate"] + [
    f"{cc}_{f}" for cc in AMOUNTS
    for f in ("lcu_amount", "denomination_usd", "lcu_fee", "applied_fx_rate", "fx_margin_pct", "total_cost_pct")
]

# Explicit provider aliases beyond case/whitespace folding. Each entry is a documented rebrand
# or spelling variant; the raw value is always retained in `firm_raw`.
PROVIDER_ALIASES = {
    "transferwise": "Wise",
    "taptap send": "TapTap Send",
}
