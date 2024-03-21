import otimizador as ot
import datetime as dt
import pandas as pd

def main():
    print("Inicio da execução!")

    df_configEmpresa = pd.read_csv('bases/Configuracao_Empresas.csv', sep=';').sort_values('prioridade')
    df_fasesProjetos = pd.read_csv('bases/fases_projetos.csv', sep=';')
    
    ot.arrangeAllResources(df_configEmpresa, df_fasesProjetos, '2023-07-15', '2024-06-30')
    
    print("Execução finalizada!")
    

if __name__ == "__main__":
    main()