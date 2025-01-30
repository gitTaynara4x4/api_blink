from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)



load_dotenv()
BITRIX_API_URL = os.getenv('BITRIX_API_URL')
BLINKCONECTA_API_URL = os.getenv('BLINKCONECTA_API_URL')
BLINKCONECTA_AUTH = os.getenv ('BLINKCONECTA_AUTH')


WEBHOOK_URL_BITRIX = f"{BITRIX_API_URL}"
WEBHOOK_URL_BLINK = f"{BLINKCONECTA_API_URL}"
AUTH = f"{BLINKCONECTA_AUTH}"



@app.route("/api/atualizar_viabilidade/deal_id=<int:deal_id>", methods=["POST"])
def atualizar_viabilidade(deal_id):
    bitrix_response = requests.get(f"{WEBHOOK_URL_BITRIX}/crm.deal.get?id={deal_id}")
    
    if bitrix_response.status_code != 200:
        return jsonify({"error": "Erro ao obter dados do Bitrix24", "details": bitrix_response.text}), 500
    
    deal_data = bitrix_response.json().get("result", {})
    
  
    dados = {
        "cidade": deal_data.get("UF_CRM_1731588487", ""),
        "bairro": deal_data.get("UF_CRM_1700661287551", ""),
        "endereco": deal_data.get("UF_CRM_1698688252221", ""),
        "numero": deal_data.get("UF_CRM_1700661252544", "")
    }
    
    
    headers = {"Authorization": BLINKCONECTA_AUTH, "User-Agent": "Mozilla/5.0"}
    viabilidade_response = requests.get(BLINKCONECTA_API_URL, headers=headers, params=dados)
    
    if viabilidade_response.status_code != 200:
        return jsonify({"error": "Erro na consulta de viabilidade", "details": viabilidade_response.text}), 500
    
    viabilidade_data = viabilidade_response.json().get("values", {})
    
    
    status_viabilidade = viabilidade_data.get("status_viabilidade", "")
    descricao = viabilidade_data.get("descricao", "")
    campo_viabilidade = f"Status: {status_viabilidade}\nDescrição: {descricao}"
    
    update_data = {"id": deal_id, "fields": {"UF_CRM_1738254914": campo_viabilidade}}
    update_response = requests.post(f"{WEBHOOK_URL_BITRIX}/crm.deal.update", json=update_data)
    
    if update_response.status_code != 200:
        return jsonify({"error": "Erro ao atualizar campo no Bitrix24", "details": update_response.text}), 500
    
    return jsonify({"message": "Campo atualizado com sucesso no Bitrix24", "status_viabilidade": status_viabilidade, "descricao": descricao})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
