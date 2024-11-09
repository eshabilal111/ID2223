from math import radians
import numpy as np
import pandas as pd
from typing import Union

def haversine(long: pd.Series, lat: pd.Series, shift: int) -> np.ndarray:
    """
    Compute Haversine distance between each consecutive coordinate in (long, lat).

    Parameters:
    - long: pandas Series, longitude values
    - lat: pandas Series, latitude values
    - shift: int, the number of positions to shift for calculating distances

    Returns:
    - numpy array, Haversine distances
    """
    long_shifted = long.shift(shift)
    lat_shifted = lat.shift(shift)
    long_diff = long_shifted - long
    lat_diff = lat_shifted - lat

    a = np.sin(lat_diff/2.0)**2
    b = np.cos(lat) * np.cos(lat_shifted) * np.sin(long_diff/2.0)**2
    c = 2*np.arcsin(np.sqrt(a + b))

    return c

def calculate_loc_delta_t_minus_1(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate loc_delta_t_minus_1 for each group.

    Parameters:
    - group: pandas DataFrame group, grouped by 'cc_num'

    Returns:
    - pandas Series, loc_delta_t_minus_1 values
    """
    # Sort values and convert latitude and longitude to radians
    df = df.sort_values("datetime")
    df[["longitude", "latitude"]] = df[["longitude", "latitude"]].applymap(radians)

    df["loc_delta_t_minus_1"] = df.groupby("account_id").apply(
        lambda x: haversine(x["longitude"], x["latitude"], +1)
    ).reset_index(level=0, drop=True).fillna(0)

    return df


def time_delta(datetime_value: pd.Series, shift: int) -> pd.Series:
    """
    Compute time difference between each consecutive transaction.

    Parameters:
    - datetime_value: pandas Series, datetime values
    - shift: int, the number of positions to shift for calculating time differences

    Returns:
    - pandas Series, time differences
    """
    time_shifted = datetime_value.shift(shift)
    return time_shifted


def calculate_time_delta_t_minus_1(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate time_delta_t_minus_1 for each group.

    Parameters:
    - group: pandas DataFrame group, grouped by 'account_id'

    Returns:
    - pandas Series, time_delta_t_minus_1 values
    """
    df = df.sort_values("datetime")
    df["time_delta_t_minus_1"] = df.groupby("account_id") \
        .apply(lambda x: time_delta(x["datetime"], +1))\
        .reset_index(level=0, drop=True)

    # Normalize time_delta_t_minus_1 to days and handle missing values
    df["time_delta_t_minus_1"] = (df["datetime"] - df["time_delta_t_minus_1"]) / np.timedelta64(1, 'D')
    df["time_delta_t_minus_1"] = df["time_delta_t_minus_1"].fillna(0)
    return df
