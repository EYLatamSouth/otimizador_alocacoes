import pandas as pd

import allocpro.config as cfg
import allocpro.otimizador as ot


def start_allocation():
    print("Inicio da Alocação!")

    df_config_empresa = (pd.read_csv(cfg.CONFIG_EMPRESAS_FILEPATH, sep=";")
                         .sort_values("prioridade"))

    df_fases_projetos = pd.read_csv(cfg.FASES_PROJETO_FILEPATH, sep=";")

    ot.arrange_all_resources(df_config_empresa, df_fases_projetos,
                             cfg.START_DATE, cfg.END_DATE)

    print("Alocação finalizada!")
