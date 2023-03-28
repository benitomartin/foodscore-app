
import pandas as pd


def get_df(df: str):

    data = pd.read_csv(df, index_col=[0])

    data_df = pd.DataFrame(data)



    return data_df


def list(df: list):

    list = []

    data_df = pd.DataFrame(data)



    return data_df
