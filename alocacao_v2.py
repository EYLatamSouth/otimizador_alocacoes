import pandas as pd
import json
import numpy as np
from functions import generate_fy_calendar
import datetime


BEGIN_FY = datetime.date(2023, 7, 15)
END_FY = datetime.date(2024, 6, 29)


def process_staff_level(level, staff, df, data):
    repeat_factors = df[level].values
    repeat_factors = np.where(~np.isnan(repeat_factors) & (repeat_factors.astype(float) == repeat_factors.astype(int)), repeat_factors, 0)
    df_repeated = df.loc[np.repeat(df.index.values, repeat_factors.astype(int))].reset_index(drop=True)
    
    columns_to_drop = ["prioridade", "grupo", "possui trimestral", "deadline", "horas", "senior", "staff 3", "staff 2",
                       "trainee", "fase_planejamento", "fase_interim", "fase_final", "fase_trimestral"]
    df_clean = df_repeated.drop(columns=columns_to_drop)
    
    df_s = pd.DataFrame(columns=data)
    df_s["equipe"] = pd.DataFrame(staff)

    cols = list(df_s.columns)
    cols = [cols[-1]] + cols[:-1]
    df_s = df_s[cols]
    
    for index, row in df_clean.iterrows():
        company = df_clean.loc[index, "empresa"]
        for idx, col in enumerate(df_clean.columns[1:]):
            value = row[col]
            if value == 40:
                df_s[col][index] = company
            elif value == "F":
                df_s[col][index] = "F"
            else:
                df_s[col][index] = ""

    df_s.to_csv(f"{level}.csv")



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


    process_staff_level('senior', senior, df, data)
    process_staff_level('staff 3', staff3, df, data)
    process_staff_level('staff 2', staff2, df, data)
    process_staff_level('trainee', trainee, df, data)

if __name__ == "__main__":
    main()


