import allocpro.config as cfg
from allocpro.alocacao import run_allocation_process
from allocpro.backup import backup_staging_and_outputs, cleanup_old_backups
from allocpro.concatenar_linhas import prepare_outputs
from allocpro.exec_otimizador import start_allocation


def main():
    try:
        backup_staging_and_outputs()
        cleanup_old_backups(backup_folder=cfg.BACKUP_FOLDER,
                            days=cfg.BACKUP_FOLDERS_PERSISTENCE)
    except Exception as exc:  # pylint: disable=broad-except
        print(exc)
        print("Failed to backup previous execution outputs. Skipping this step.")

    start_allocation()
    run_allocation_process()
    prepare_outputs()


if __name__ == "__main__":
    main()
