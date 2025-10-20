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

        # Adicionamos a mensagem especial, se existir
        if pd.notna(mensagem_especial) and str(mensagem_especial).strip():
            body_parts.append(f"<p><b>-- MENSAGEM ESPECIAL --</b><br><b>{str(mensagem_especial).strip()}</b></p>")

        # Usamos <p> para parágrafos, que criam espaços automaticamente
        body_parts.append("<br><p>Bom dia!</p>")
        body_parts.append("<p>Hoje, temos as seguintes atividades para estudarmos para nosso sonhado Intercâmbio:</p>")

        # Criamos uma lista HTML (<ul>) para as aulas
        aulas_do_dia = parse_task_list(tarefa.get('TODO!'))
        if aulas_do_dia:
            body_parts.append("<p><b>Aulas do dia:</b></p>")
            body_parts.append("<ul>")
            for aula in aulas_do_dia:
                body_parts.append(f"<li>{aula}</li>") # <li> cria o item da lista
            body_parts.append("</ul>")

        # Criamos outra lista HTML para o Anki
        anki_tasks = parse_task_list(tarefa.get('Anki'))
        if anki_tasks:
            body_parts.append("<p><b>E para a revisão no Anki:</b></p>")
            body_parts.append("<ul>")
            for task in anki_tasks:
                body_parts.append(f"<li>{task}</li>")
            body_parts.append("</ul>")

        # Adicionamos as contagens regressivas em parágrafos
        body_parts.append(f"<p>{mensagem_jlpt}</p>") # <i> para itálico
        body_parts.append(f"<p>{mensagem_japao}</p>")

        # Montamos o corpo final do e-mail
        # Envolvemos tudo em tags <html> e <body> para garantir que seja lido como HTML
        body = f"<html><body style='font-family: Arial, sans-serif; line-height: 1.5;'>{''.join(body_parts)}</body></html>"

        return subject, body

    else:
        subject = "🇯🇵 Sem atividades de japonês por Hoje!"
        # Também formatamos a mensagem de "descanso" como HTML
        body =f"""
        <html>
        <body style='font-family: Arial, sans-serif; line-height: 1.5;'>
            <p>Não há atividades de japonês para hoje!</p>
            <p>Podemos descansar.</p>
            <br>
            <p><i>{mensagem_jlpt}</i></p>
            <p><i>{mensagem_japao}</i></p>
        </body>
        </html>
        """
        return subject, body
    

    

def main():
    load_dotenv()

    SENDER = os.getenv('MEU_EMAIL')
    PASSWORD = os.getenv('MINHA_SENHA')
    RECEIVER_STRING = os.getenv('EMAIL_RECEIVER') 

    if not all([SENDER, PASSWORD, RECEIVER_STRING]):
        print("ERRO: Configure as variáveis de ambiente MEU_EMAIL, MINHA_SENHA_DE_APP e EMAIL_RECEIVER.")
        return
    
    receiver_list = [email.strip() for email in RECEIVER_STRING.split(',')]
    
    tarefa_de_hoje = fetch_row()
    assunto, corpo = format_email_content(tarefa_de_hoje)

    print(corpo)

    email_service = EmailConnector(email_sender=SENDER, email_password=PASSWORD)
    email_service.send_email(receiver_list=receiver_list, subject=assunto, body=corpo)
    print("Email enviado com sucesso!")


if __name__ == "__main__":
    main()