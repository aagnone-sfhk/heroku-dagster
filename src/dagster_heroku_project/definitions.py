import pandas as pd
from dagster import Definitions, asset

@asset
def hello_asset():
    """An example asset that creates and returns a pandas DataFrame."""
    data = {'col1': [1, 2], 'col2': [3, 4]}
    return pd.DataFrame(data=data)

# The Definitions object is the entry point for Dagster to find all your definitions.
defs = Definitions(
    assets=[hello_asset],
)

