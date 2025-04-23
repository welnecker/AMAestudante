from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def enviar_respostas_em_blocos(linhas, credencial):
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
