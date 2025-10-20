import datetime
import pandas as pd
import os

def fetch_row() -> dict | None:

    dia_hoje = datetime.date.today()
    caminho_arquivo = os.path.join('Assets', 'Dias.csv')
    
    try:
        df_dias = pd.read_csv(
            caminho_arquivo,
            sep="\t",
            encoding='latin1',
            parse_dates=['Data'],
            dayfirst = True
        )

        resultado = df_dias.loc[df_dias['Data'].dt.date == dia_hoje]

        if not resultado.empty:
            return resultado.iloc[0].to_dict()
        else:
            return None

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em: {caminho_arquivo}")
        return None
    except KeyError:
        print(f"Erro: Coluna 'Data' não encontrada em: {caminho_arquivo}")
        return None
    except Exception as e:
        print(f"Erro: {e}")
        return None
    
    
if __name__ == "__main__":
    tarefa = fetch_row()
    if tarefa:
        print(tarefa)
    else:
        print("Nenhuma tarefa encontrada hoje")
    

    