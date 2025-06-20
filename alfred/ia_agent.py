import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    print("ERRO: A chave da API do Google Gemini não foi encontrada no .env.")
    sys.exit(1)

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    chat = model.start_chat(history=[])
except Exception as e:
    print(f"Erro ao inicializar o Gemini: {e}")
    sys.exit(1)

def enviar_para_gemini(prompt_usuario, dados_coingecko):
    if dados_coingecko:
        mensagem = "--- DADOS ATUALIZADOS COINGECKO ---\n" + dados_coingecko
        mensagem += ("Instruções:\n"
                     "Com base nos dados fornecidos, responda à solicitação do usuário de forma clara.\n"
                     "Se ele pediu os ativos mais valorizados e os ativos em queda, apresente duas listas separadas.\n"
                     "Mantenha o foco nas variações percentuais e faça comparativos quando solicitados.\n")
        mensagem += f"Usuário: {prompt_usuario}"
    else:
        mensagem = f"Usuário: {prompt_usuario}\n(Nenhum dado atualizado foi encontrado na CoinGecko para esta consulta.)"

    try:
        resposta = chat.send_message(mensagem)
        return resposta.text.strip()
    except Exception as e:
        return f"Erro ao enviar mensagem ao Gemini: {e}"

