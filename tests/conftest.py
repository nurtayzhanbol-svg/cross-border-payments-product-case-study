import pandas as pd
import pytest

from rpw import config


@pytest.fixture(scope="session")
def wide():
    path = config.PROCESSED_DIR / "rpw_records_wide.parquet"
    if not path.exists():
        pytest.skip("processed data not built; run `PYTHONPATH=src python -m rpw.build`")
    return pd.read_parquet(path)


@pytest.fixture(scope="session")
def long():
    path = config.PROCESSED_DIR / "rpw_quotes_long.parquet"
    if not path.exists():
        pytest.skip("processed data not built")
    return pd.read_parquet(path)
