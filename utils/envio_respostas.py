import streamlit as st
import pandas as pd
from datetime import datetime
import unicodedata
import time
import sys
import os
import json

# Ajusta o caminho para permitir importações do nível raiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import random

def enviar_respostas_em_blocos(linhas, credencial):
    """
    Envia uma lista de linhas para a aba ATIVIDADES de uma planilha no Google Sheets.
    """
    creds = Credentials.from_service_account_info(credencial)
    service = build("sheets", "v4", credentials=creds)

    body = {"values": linhas}
    planilha_id = "17SUODxQqwWOoC9Bns--MmEDEruawdeEZzNXuwh3ZIj8"
    intervalo = "ATIVIDADES!A1"

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
    """
    if not isinstance(credenciais_dict, dict):
        raise ValueError("As credenciais devem estar em formato de dicionário.")
    return random.choice(list(credenciais_dict.values()))
