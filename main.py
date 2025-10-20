import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

from fetch_row import fetch_row
from email_connection import EmailConnector


def format_email_content(tarefa: dict | None):
    

    def parse_task_list(task_string: str | float) -> list[str]:
        if not isinstance(task_string, str):
            return []
        
        # CORREÇÃO: Remova o .replace() problemático
        # A linha agora apenas separa a string por '\x95' e limpa os espaços.
        tasks = [item.strip() for item in task_string.split('\x95') if item.strip()]
        print(tasks)
        return tasks


    # --- CÁLCULO DAS DATAS ---
    data_n5 = datetime(2025, 12, 7)
    data_japao = datetime(2026, 6, 15)
    data_hoje = datetime.now()
    
    dias_n5 = (data_n5 - data_hoje).days
    dias_japao = (data_japao - data_hoje).days
    
    mensagem_jlpt = f"Faltam {dias_n5} dias até nossa prova de JLPT!" if dias_n5 > 0 else ""
    mensagem_japao = f"Faltam {dias_japao} dias até nosso intercâmbio pro Japão!!!!"
    # -----------------------------

    
    if tarefa:
        data_formatada = tarefa['Data'].strftime('%d/%m/%Y')
        subject = f"🇯🇵 Atividades de japonês para hoje: {data_formatada}"
        
        body_parts = []
        mensagem_especial = tarefa.get('Mensagem_Especial')

        if pd.notna(mensagem_especial) and str(mensagem_especial).strip():
            body_parts.append(f"*-- MENSAGEM ESPECIAL --*\n{str(mensagem_especial).strip()}\n\n")

        body_parts.append("Bom dia!\n")
        body_parts.append("Hoje, temos as seguintes atividades para estudarmos para nosso sonhado Intercâmbio:\n\n")


        #! -- Lógica x95

        aulas_do_dia = parse_task_list(tarefa.get('TODO!'))
        print(aulas_do_dia)
        if aulas_do_dia:
            body_parts.append("*Aulas do dia:*\n")
            for aula in aulas_do_dia:
                print(aula)
                body_parts.append(f"- {aula}\n")
            body_parts.append("\n")


        anki_tasks = parse_task_list(tarefa.get('Anki'))
        if anki_tasks:
            body_parts.append("*E para a revisão no Anki:*\n")
            for task in anki_tasks:
                body_parts.append(f"- {task}\n")
            body_parts.append("\n")

        body_parts.append(f"{mensagem_jlpt}\n")
        body_parts.append(f"{mensagem_japao}\n")

        body = "".join(body_parts)
        print(body)

        return subject, body


    else:
        subject = "🇯🇵 Sem atividades de japonês por Hoje!"
        body =f"""
        Não atividades de japonês para hoje!
        Podemos descansar.

        {mensagem_jlpt}
        {mensagem_japao}
        """


    return subject, body


def main():
    load_dotenv()

    SENDER = os.getenv('MEU_EMAIL')
    PASSWORD = os.getenv('MINHA_SENHA')
    RECEIVER = os.getenv('EMAIL_RECEIVER')
    if not all([SENDER, PASSWORD, RECEIVER]):
        print("ERRO: Configure as variáveis de ambiente MEU_EMAIL, MINHA_SENHA_DE_APP e EMAIL_RECEIVER.")
        return
    
    tarefa_de_hoje = fetch_row()
    assunto, corpo = format_email_content(tarefa_de_hoje)

    print(corpo)

    email_service = EmailConnector(email_sender=SENDER, email_password=PASSWORD)
    email_service.send_email(receiver=RECEIVER, subject=assunto, body=corpo)
    print("Email enviado com sucesso!")


if __name__ == "__main__":
    main()