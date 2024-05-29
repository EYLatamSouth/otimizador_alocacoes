from pathlib import Path

import numpy as np
import pandas as pd

import allocpro.config as cfg


def prepare_outputs():
    categorias = ["trainee", "staff 2", "staff 3", "senior"]

    for cat in categorias:
        df = pd.read_csv(Path(cfg.STAGING_FOLDER).joinpath(f"{cat}.csv"))
        df.drop(columns=["Unnamed: 0", "equipe"], inplace=True)

        # Find the maximum count of non-NaN values across the columns
        max_len = max(df.apply(lambda x: x.dropna().shape[0]))

        # Create a dataframe of NaN values with the necessary length
        res_list = pd.DataFrame(
            None, index=np.arange(max_len), columns=df.columns, dtype="object"
        )

        for col in df.columns:
            res = df[col].dropna().reset_index(drop=True)
            res_list.loc[: len(res) - 1, col] = res

        res_list = pd.DataFrame()

        for col in df.columns:
            res = df[col].dropna().reset_index(drop=True)
            res_df = pd.DataFrame(res)
            res_list = pd.concat([res_list, res_df], axis=1)

        res_list.to_csv(Path(cfg.OUTPUTS_FOLDER).joinpath(f"{cat}_alocacao_final.csv"), index=True)
