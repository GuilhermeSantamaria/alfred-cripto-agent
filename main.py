from alfred.crypto_service import get_crypto_data
from alfred.prompt_handler import identify_cryptos_in_prompt
from alfred.ia_agent import enviar_para_gemini

def main():
    print("\n--- Alfred, agente financeiro de ativos digitais ---\n")
    print("\n")
    print("Olá! Sou Alfred, seu agente de IA especializado em criptomoedas.\n")
    print("Possuo dados de Preço (USD), Variação percentual em 24hrs, Capitalização de Mercado (USD) e Volume de Negociação em 24hs (USD)\n")
    print("Digite o nome ou sigla do ativo que deseja consultar (ex: Bitcoin, ETH, Litecoin, Etc...) ou faça perguntas como:\n"
          "- Quais os ativos mais rentáveis das últimas 24h?\n"
          "- Quais ativos estão em queda nas últimas 24h?\n"
          "Ou até mesmo:\n"
          "- Me informe uma quantidade (x) de ativos que mais valorizaram e (y) de ativos que estão em queda.\n"
          "- Faça o comparativo entre o ativo (x), (y) e (z)"
          "\n")
    print("Digite 'fim' quando quiser encerrar a interação comigo.\n")
    print("\n")
    print("Como posso lhe ajudar hoje?\n")

    while True:
        prompt = input("Você: ")
        if prompt.strip().lower() == 'fim':
            print("Agente: Até mais!")
            break

        cryptos = identify_cryptos_in_prompt(prompt)
        dados_coingecko_str = ""

        if cryptos:
            dados = get_crypto_data(cryptos)
        else:
            dados = get_crypto_data()

        if dados:
            dados_coingecko_str = "--- DADOS ATUALIZADOS COINGECKO ---\n"
            for k, v in dados.items():
                dados_coingecko_str += (
                    f"Cripto: {v['name']} ({v['symbol']})\n"
                    f"  Preço: {v['price']:.2f} USD\n"
                    f"  Variação 24h: {v['change']:.2f}%\n"
                    f"  Capitalização: {v['market_cap']:,} USD\n"
                    f"  Volume 24h: {v['volume']:,} USD\n\n"
                )
            dados_coingecko_str += (
                "Instruções:\n"
                "Com base nos dados fornecidos, responda à solicitação do usuário de forma clara.\n"
                "Se ele pediu os ativos mais valorizados e os ativos em queda, apresente duas listas separadas:\n"
                "- Para os mais valorizados: informe o nome, sigla e quanto subiu em % nas últimas 24h.\n"
                "- Para os em queda: informe o nome, sigla e quanto caiu em % nas últimas 24h.\n"
                "- Para casos onde o usuário solicita comparativos específicos entre variados ativos, faça sempre o que foi pedido com o máximo de precisão, usando os dados da API CoinGecko.\n"
                "Não inclua valores repetidos ou irrelevantes. Mantenha o foco apenas nas variações percentuais.\n"
                "Lembre-se do histórico da conversa para responder a perguntas que se referem a análises anteriores.\n"
            )

        if dados_coingecko_str:
            mensagem_para_gemini = f"{dados_coingecko_str}\nUsuário: {prompt}"
        else:
            mensagem_para_gemini = f"Usuário: {prompt}"
            if not dados:
                mensagem_para_gemini += "\n(Nenhum dado atualizado foi encontrado na CoinGecko para esta consulta. Informe que os dados não estão disponíveis.)"

        resposta = enviar_para_gemini(prompt, dados_coingecko_str)
        print("\n--- Análise: ---")
        print(resposta)
        print("--------------\n")

if __name__ == '__main__':
    main()
