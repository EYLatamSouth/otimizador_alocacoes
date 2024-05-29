# Otimizador de Alocações

Projeto otimiza a alocação de profissionais de Assurance, conforme
a quantidade de profissionais disponíveis, horas requeridas por cada projeto e
suas respectivas especificidades.

## Clonando este Projeto

Execute o seguinte comando no seu terminal (Command Prompt, Terminal):

```console
git clone https://github.com/EYLatamSouth/otimizador_alocacoes.git
```


## Criando Novo Environment

Recomendamos que você crie um novo ambiente para execução deste projeto.
Caso tenha o Anaconda ou Miniconda instalado em sua máquina, execute os 
seguintes comandos:

### Passo 1: Criando um novo ambiente de execução

Para criar um novo ambiente de execução, execute o comando abaixo, 
modificando o valor `<NOME-DO-ENV>` pelo nome que deseja dar ao novo 
ambiente de execução.

```console
conda create -n <NOME-DO-ENV> -y python=3.11 
```

O comando acima cria um novo ambiente de execução chamado `<NOME-DO-ENV>` e 
instala a versão `3.11` do Python.

> **Exemplo:** Para criar um ambiente de execução novo com o nome `ey-otm`,
> podemos executar o seguinte comando acima da seguinte maneira:
> 
> ```console
> conda create -n ey-otm -y python=3.11 
> ```

### Passo 2: Ativando o novo ambiente de execução criado

Para ativar o ambiente de execução que você acabou de criar, execute o comando:

```console
conda activate <NOME-DO-ENV>
```

> Novamente, para o exemplo dado no **Passo 1**, caso o environment tenha
> sido criado com o nome `ey-otm`, podemos ativar este novo ambiente
> executando o comando:
> 
> ```console
> conda activate ey-otm
> ```

### Passo 3: Instalação

![](/Resources/instalando-aplicacao.gif)

Para instalar a aplicação de alocação de recursos e todas suas bibliotecas
auxiliares, execute o seguinte comando:

```console
pip install -e .
```

O comando acima irá instalar a aplicação de alocação de recursos, assim como,
todos os pacotes necessários para a execução do processo de otimização de
alocações.

## Executando Aplicação

Para executar a aplicação e gerar os arquivos com as alocações de
recursos otimizadas, execute o seguinte comando:

```console
run-allocation
```

O comando acima irá ler as bases de input de dentro da pasta [Bases](/Bases)
e, a partir destes arquivos de input e as configurações utilizadas para
a rodada, gerar os arquivos de resultado com as alocações de profissionais
de cada ranking. Os arquivos de resultado são então salvos dentro da pasta
[Outputs](/Outputs).

### Parâmetros de Execução

Alêm dos arquivos de input mencionados acima, a aplicação também possui o 
seguinte arquivo que reúne os parâmetros configuráveis de execução: [config.py](/src/allocpro/config.py)

Neste arquivo é possível especificar o diretório de onde os inputs serão lidos,
a pasta onde os resultados das alocações deverão ser salvos, assim como,
as datas de início e fim do ano fiscal.

