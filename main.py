import subprocess

def main():

    # Lista dos seus serviços
    services = ["exec_otimizador.py", "alocacao.py", "concatenar_linhas.py"]

    # Itera através da lista de serviços e os executa em ordem
    for service in services:
        # O comando 'python' pode precisar de ser substituído por 'python3' ou um caminho para o python, dependendo do seu ambiente
        subprocess.run(["python", service])
if __name__ == "__main__":
    main()