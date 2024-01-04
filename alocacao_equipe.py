import pandas as pd
import json
import numpy as np
from functions import generate_fy_calendar
import datetime


BEGIN_FY = datetime.date(2023, 7, 15)
END_FY = datetime.date(2024, 6, 29)


def main():
    data = []
    date_list = generate_fy_calendar(BEGIN_FY, END_FY)
    for date in date_list:
        formatted_date = date.strftime('%Y-%m-%d')
        data.append(formatted_date)


    df = pd.read_excel(r"Resultado.xlsx")
    df.drop(columns=["Unnamed: 0"], inplace=True)

    for col in df.columns:
        if all(df[col]==0):
            df[col]="F"


    senior = []
    staff3 = []
    staff2 = []
    trainee = []
    sr = df['senior'].sum()
    st3 = df['staff 3'].sum()
    st2 = df['staff 2'].sum()
    tr = df['trainee'].sum()

    for s in range(sr):
        senior.append(f"senior_{s}")
    for s3 in range(st3):
        staff3.append(f"staff3_{s3}")
    for s2 in range(st2):
        staff2.append(f"staff2_{s2}")
    for t in range(tr):
        trainee.append(f"trainee_{t}")



    repeat_factors = df['senior'].values
    repeat_factors = np.where(~np.isnan(repeat_factors) & (repeat_factors.astype(float) == repeat_factors.astype(int)), repeat_factors, 0)
    df_repeated = df.loc[np.repeat(df.index.values, repeat_factors.astype(int))].reset_index(drop=True)
    df_clean = df_repeated.drop(columns=["prioridade", "grupo", "possui trimestral", "deadline", "horas", "senior", "staff 3", "staff 2", "trainee", "fase_planejamento", "fase_interim", "fase_final", "fase_trimestral"])
    df_s = pd.DataFrame(columns=data)
    df_s["equipe"] = pd.DataFrame(senior)
    cols = list(df_s.columns)
    cols = [cols[-1]] + cols[:-1]
    df_s = df_s[cols]
    for index, row in df_clean.iterrows():
        company = df_clean.loc[index, "empresa"]
        for idx, col in enumerate(df_clean.columns[1:]):
            value = row[col]
            if value == 40:
                df_s[col][index]=company
            elif value == "F":
                df_s[col][index] = "F"
            else:
                df_s[col][index] = ""

    df_s.to_csv("senior.csv")
    del df_s
    del repeat_factors
    del df_clean



    repeat_factors = df['staff 3'].values
    repeat_factors = np.where(~np.isnan(repeat_factors) & (repeat_factors.astype(float) == repeat_factors.astype(int)), repeat_factors, 0)
    df_repeated = df.loc[np.repeat(df.index.values, repeat_factors.astype(int))].reset_index(drop=True)
    df_clean = df_repeated.drop(columns=["prioridade", "grupo", "possui trimestral", "deadline", "horas", "senior", "staff 3", "staff 2", "trainee", "fase_planejamento", "fase_interim", "fase_final", "fase_trimestral"])
    df_s = pd.DataFrame(columns=data)
    df_s["equipe"] = pd.DataFrame(staff3)
    cols = list(df_s.columns)
    cols = [cols[-1]] + cols[:-1]
    df_s = df_s[cols]

    for index, row in df_clean.iterrows():
        company = df_clean.loc[index, "empresa"]
        for idx, col in enumerate(df_clean.columns[1:]):
            value = row[col]
            if value == 40:
                df_s[col][index]=company
            elif value == "F":
                df_s[col][index] = "F"
            else:
                df_s[col][index] = ""

    df_s.to_csv("staff3.csv")
    del df_s
    del repeat_factors
    del df_clean


    repeat_factors = df['staff 2'].values
    repeat_factors = np.where(~np.isnan(repeat_factors) & (repeat_factors.astype(float) == repeat_factors.astype(int)), repeat_factors, 0)
    df_repeated = df.loc[np.repeat(df.index.values, repeat_factors.astype(int))].reset_index(drop=True)
    df_clean = df_repeated.drop(columns=["prioridade", "grupo", "possui trimestral", "deadline", "horas", "senior", "staff 3", "staff 2", "trainee", "fase_planejamento", "fase_interim", "fase_final", "fase_trimestral"])
    df_s = pd.DataFrame(columns=data)
    df_s["equipe"] = pd.DataFrame(staff2)
    cols = list(df_s.columns)
    cols = [cols[-1]] + cols[:-1]
    df_s = df_s[cols]

    for index, row in df_clean.iterrows():
        company = df_clean.loc[index, "empresa"]
        for idx, col in enumerate(df_clean.columns[1:]):
            value = row[col]
            if value == 40:
                df_s[col][index]=company
            elif value == "F":
                df_s[col][index] = "F"
            else:
                df_s[col][index] = ""

    df_s.to_csv("staff2.csv")
    del df_s
    del repeat_factors
    del df_clean


    repeat_factors = df['trainee'].values
    repeat_factors = np.where(~np.isnan(repeat_factors) & (repeat_factors.astype(float) == repeat_factors.astype(int)), repeat_factors, 0)
    df_repeated = df.loc[np.repeat(df.index.values, repeat_factors.astype(int))].reset_index(drop=True)
    df_clean = df_repeated.drop(columns=["prioridade", "grupo", "possui trimestral", "deadline", "horas", "senior", "staff 3", "staff 2", "trainee", "fase_planejamento", "fase_interim", "fase_final", "fase_trimestral"])
    df_s = pd.DataFrame(columns=data)
    df_s["equipe"] = pd.DataFrame(trainee)
    cols = list(df_s.columns)
    cols = [cols[-1]] + cols[:-1]
    df_s = df_s[cols]

    for index, row in df_clean.iterrows():
        company = df_clean.loc[index, "empresa"]
        for idx, col in enumerate(df_clean.columns[1:]):
            value = row[col]
            if value == 40:
                df_s[col][index]=company
            elif value == "F":
                df_s[col][index] = "F"
            else:
                df_s[col][index] = ""

    df_s.to_csv("trainee.csv")
    del df_s
    del repeat_factors
    del df_clean


if __name__ == "__main__":
    main()