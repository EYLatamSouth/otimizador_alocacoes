import pandas as pd
import datetime

from functions import generate_fy_calendar, trainee, staff2, staff3, senior, priority

BEGIN_FY = datetime.date(2023, 7, 1)
END_FY = datetime.date(2024, 6, 22)
WEEK_HOLLIDAYS = ["23-12-2023", "30-12-2023", "15-06-2024", "22-06-2024"]

def main():

    dados_entrada = pd.read_csv("dados_cliente.csv")
    dados_entrada = dados_entrada.dropna()
    planning_spreadsheet = ["priority","client", "nome_retain", "renocao_prevista", "fy24_total_hours", "horas_demanda", "trimestral", "senior", "staff3", "staff2", "trainee", "horas_locadas"]

    date_list = generate_fy_calendar(BEGIN_FY, END_FY)
    for date in date_list:
        formatted_date = date.strftime('%d-%m-%Y')
        planning_spreadsheet.append(formatted_date)

    df = pd.DataFrame(columns=planning_spreadsheet)

    df["client"] = dados_entrada[dados_entrada.columns[0]]
    df["nome_retain"] = dados_entrada[dados_entrada.columns[1]]
    df["renocao_prevista"] = dados_entrada[dados_entrada.columns[2]]
    df["fy24_total_hours"] = dados_entrada[dados_entrada.columns[3]]
    df["horas_demanda"] = dados_entrada[dados_entrada.columns[4]]
    df["trimestral"] = dados_entrada[dados_entrada.columns[6]]

    hollidays = WEEK_HOLLIDAYS
    for week in hollidays:
        df[week] = "F"

    df['priority'] = df['fy24_total_hours'].apply(priority)
    df['senior'] = df['fy24_total_hours'].apply(senior)
    df['staff3'] = df['fy24_total_hours'].apply(staff3)
    df['staff2'] = df['fy24_total_hours'].apply(staff2)
    df['trainee'] = df['fy24_total_hours'].apply(trainee)

    print(df.head(10))

if __name__ =="__main__":
    main()
