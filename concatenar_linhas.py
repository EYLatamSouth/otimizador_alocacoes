import pandas as pd
import numpy as np

def main():

    categorias = ["trainee", "staff 2", "staff 3", "senior"]

    for cat in categorias:

        df = pd.read_csv(f"{cat}.csv")
        df.drop(columns=["Unnamed: 0", "equipe"], inplace=True)

        # Find the maximum count of non-NaN values across the columns
        max_len = max(df.apply(lambda x: x.dropna().shape[0]))

        # Create a dataframe of NaN values with the necessary length
        res_list = pd.DataFrame(np.nan, index=np.arange(max_len), columns=df.columns)

        for col in df.columns:
            res = df[col].dropna().reset_index(drop=True)
            res_list.loc[:len(res)-1, col] = res

        res_list = pd.DataFrame()

        for col in df.columns:
            res = df[col].dropna().reset_index(drop=True)
            res_df = pd.DataFrame(res)
            res_list = pd.concat([res_list, res_df], axis=1)
        

        res_list.to_csv(f'{cat}_alocacao_final.csv', index=True)

if __name__ == "__main__":
    main()
