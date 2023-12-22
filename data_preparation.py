import pandas as pd
import datetime

from functions import generate_fy_calendar, trainee, staff2, staff3, senior, priority, trimestral, final, interim, planejamento

BEGIN_FY = datetime.date(2023, 7, 1)
END_FY = datetime.date(2024, 6, 22)
VACATIONS = ["23-12-2023", "30-12-2023", "01-06-2024", "08-06-2024", "15-06-2024", "22-06-2024"]

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
    for week in VACATIONS:
        df[week] = "F"

    df['priority'] = df['fy24_total_hours'].apply(priority)
    df['senior'] = df['fy24_total_hours'].apply(senior)
    df['staff3'] = df['fy24_total_hours'].apply(staff3)
    df['staff2'] = df['fy24_total_hours'].apply(staff2)
    df['trainee'] = df['fy24_total_hours'].apply(trainee)
    df = df.reset_index(drop=True)
    df.to_csv("planejamento.csv", index=False)

    #################################
    df_tratados = df[["client", "priority", "fy24_total_hours", "senior", "staff3", "staff2", "trainee", "trimestral"]]
    df_tratados['planejamento'] = df_tratados['fy24_total_hours'].apply(planejamento)
    df_tratados['final'] = df_tratados['fy24_total_hours'].apply(final)
    df_tratados['interim'] = df_tratados['fy24_total_hours'].apply(interim)
    df_tratados['trimestral_1'] = df_tratados['fy24_total_hours'].apply(trimestral)
    df_tratados['trimestral_2'] = df_tratados['fy24_total_hours'].apply(trimestral)
    df_tratados.loc[df_tratados["trimestral"] == "No", ["trimestral_1", "trimestral_2"]] = 0
    df_tratados = df_tratados.drop(columns="fy24_total_hours")
    df_tratados = df_tratados.reset_index(drop=True)
    df_tratados.to_csv("dados_tratados.csv", index=False)


if __name__ =="__main__":
    main()
