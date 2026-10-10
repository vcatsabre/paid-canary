import pandas as pd

def redact(df: pd.DataFrame, role: str) -> pd.DataFrame:
    """If role is 'customer', hide internals like incident_id and root_cause"""
    if role == 'customer':
        safe_cols = [c for c in df.columns if c not in ('incident_id','root_cause','owner','internal_notes')]
        return df[safe_cols]
    return df
