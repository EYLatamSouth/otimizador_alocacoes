from allocpro.utils import find_project_root_directory

START_DATE = "2023-07-15"
END_DATE = "2024-06-30"

BACKUP_FOLDERS_PERSISTENCE = 30  # 30 days

ROOT_DIR = find_project_root_directory()

BACKUP_FOLDER = ROOT_DIR.joinpath("Backups")
INPUTS_FOLDER = ROOT_DIR.joinpath("bases")
STAGING_FOLDER = ROOT_DIR.joinpath("Staging")
OUTPUTS_FOLDER = ROOT_DIR.joinpath("Outputs")

RESULTADO_FILEPATH = OUTPUTS_FOLDER.joinpath("Resultado.xlsx")

FASES_PROJETO_FILEPATH = INPUTS_FOLDER.joinpath("fases_projetos.csv")
CONFIG_EMPRESAS_FILEPATH = INPUTS_FOLDER.joinpath("Configuracao_Empresas.csv")

STAGING_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUTS_FOLDER.mkdir(parents=True, exist_ok=True)
