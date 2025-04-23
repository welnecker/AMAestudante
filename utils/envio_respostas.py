from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import random

def enviar_respostas_em_blocos(linhas, credencial):
    """
    Envia uma lista de linhas para a aba RESPOSTAS_ALUNOS de uma planilha no Google Sheets.
    """
    creds = Credentials.from_service_account_info(credencial)
    service = build("sheets", "v4", credentials=creds)

    body = {"values": linhas}
    planilha_id = "17SUODxQqwWOoC9Bns--MmEDEruawdeEZzNXuwh3ZIj8"
    intervalo = "RESPOSTAS_ALUNOS!A1"

    service.spreadsheets().values().append(
        spreadsheetId=planilha_id,
        range=intervalo,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()


def escolher_credencial_aleatoria(credenciais_dict):
    """
    Recebe um dicionário de credenciais do secrets e retorna uma delas aleatoriamente.
    Exemplo de entrada:
        {
            "cred1": {...},
            "cred2": {...},
            "cred3": {...}
        }
    """
    if not isinstance(credenciais_dict, dict):
        raise ValueError("As credenciais devem estar em formato de dicionário.")
    return random.choice(list(credenciais_dict.values()))
