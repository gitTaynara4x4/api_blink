from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import re

app = Flask(__name__)

load_dotenv()

BITRIX_API_URL = os.getenv('BITRIX_API_URL')
BLINKCONECTA_API_URL = os.getenv('BLINKCONECTA_API_URL')
BLINKCONECTA_API_URL_VALIDAR = os.getenv("BLINKCONECTA_API_URL_VALIDAR")
BLINKCONECTA_AUTH = os.getenv('BLINKCONECTA_AUTH')

if not all([BITRIX_API_URL, BLINKCONECTA_API_URL, BLINKCONECTA_AUTH, BLINKCONECTA_API_URL_VALIDAR]):
    raise ValueError("Erro: Algumas variáveis de ambiente não foram carregadas corretamente.")

WEBHOOK_URL_BITRIX = f"{BITRIX_API_URL}"
WEBHOOK_URL_BLINK = f"{BLINKCONECTA_API_URL}"
AUTH = f"{BLINKCONECTA_AUTH}"



# Rota para atualizar viabilidade
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

# Rota para validar cliente
@app.route("/api/validar_cliente/deal_id=<int:deal_id>", methods=["POST"])
def validar_cliente(deal_id):
    bitrix_response = requests.get(f"{BITRIX_API_URL}/crm.deal.get?id={deal_id}")

    if bitrix_response.status_code != 200:
        return jsonify({"error": "Erro ao obter dados do Bitrix24", "details": bitrix_response.text}), 500

    deal_data = bitrix_response.json().get("result", {})

    def formatar_data(data_iso):
        try:
            data_convertida = datetime.fromisoformat(data_iso.split("T")[0])  
            return data_convertida.strftime("%d-%m-%Y")  
        except:
            return ""

    def converter_sexo(sexo_id):
        return "F" if sexo_id == "48548" else "M" if sexo_id == "48550" else ""

    def limpar_cpf(cpf):
        return re.sub(r"[.\-]", "", cpf) if cpf else ""

    def limpar_cep(cep):
        return re.sub(r"[-]", "", cep) if cep else ""

    def extrair_telefone(numero_completo):

        if not numero_completo.startswith("+55"):
            numero_completo = "+55" + numero_completo

    
        padrao = re.match(r"\+55(\d{2})(\d{8,9})", numero_completo)  
        if padrao:
            return padrao.group(1), padrao.group(2)  
    
        return "", ""

    telefone_completo = deal_data.get("UF_CRM_1698698407472", "")
    ddd, telefone = extrair_telefone(telefone_completo)

    payload = {
        "nome": deal_data.get("UF_CRM_1697762313423", ""),
        "dtNascimento": formatar_data(deal_data.get("UF_CRM_1723557410", "")),
        "cpfCnpj": limpar_cpf(deal_data.get("UF_CRM_1697807353336", "")),
        "identidade": deal_data.get("UF_CRM_1697807372536", ""),
        "sexo": converter_sexo(deal_data.get("UF_CRM_1724096872", "")),
        "email": deal_data.get("UF_CRM_1697807340141", ""),
        "dddPrimario": ddd,
        "telefonePrimario": telefone,
        "cepInstalacao": limpar_cep(deal_data.get("UF_CRM_1700661314351", "")),
        "bairroInstalacao": deal_data.get("UF_CRM_1700661287551", ""),
        "ufInstalacao": deal_data.get("UF_CRM_1731589190", ""),
        "cidadeInstalacao": deal_data.get("UF_CRM_1731588487", ""),
        "enderecoInstalacao": deal_data.get("UF_CRM_1698688252221", ""),
        "numeroInstalacao": deal_data.get("UF_CRM_1700661252544", ""),
        "idPacote": 110 ,
        "idTipoMidia": 106,
        "idVendedor": 26
    }

    headers = {
        "Authorization": f"Bearer {BLINKCONECTA_AUTH}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    blink_response = requests.post(BLINKCONECTA_API_URL_VALIDAR, json=payload, headers=headers)

    if blink_response.status_code != 200:
        return jsonify({"error": "Erro na validação do cliente", "details": blink_response.text}), 500

    blinkvalue = blink_response.json().get("values", {})


    pendencias_financeiras = blinkvalue.get("serasa_ocorrencias", {}).get("Pendencias Financeiras", {}).get("valor", {})
    score = blinkvalue.get("serasa_score", {})
    pendencias_internas = blinkvalue.get("serasa_ocorrencias", {}).get("Pendencias Internas", {}).get("valor", {})
    protestos_do_estado = blinkvalue.get("serasa_ocorrencias", {}).get("Protestos do Estado", {}).get("valor", {})
    cheques_sem_fundos = blinkvalue.get("serasa_ocorrencias", {}).get("Cheques Sem Fundos Bacen", {}).get("valor", {})
    status_aprovacao = blinkvalue.get("status_aprovacao", {})
    comprovante_komunicar = blinkvalue.get("tipo_midia", {})
    comprovante_vendedor = blinkvalue.get("vendedor", {})

    print(pendencias_internas)
    print(pendencias_financeiras)

    
    if isinstance(pendencias_financeiras, float):
        pendencias_financeiras = str(pendencias_financeiras)
    if isinstance(pendencias_internas, float):
        pendencias_internas = str(pendencias_internas)
    if isinstance(protestos_do_estado, float):
        protestos_do_estado = str(protestos_do_estado)
    if isinstance(cheques_sem_fundos, float):
        cheques_sem_fundos = str(cheques_sem_fundos)
    if isinstance(status_aprovacao, float):
        status_aprovacao = str(status_aprovacao)
    if isinstance(score, float):
        score = str(score)
    if isinstance(comprovante_komunicar, float):
        score = str(comprovante_komunicar)
    if isinstance(comprovante_vendedor, float):
        score = str(comprovante_vendedor)    


    update_payload = {
        "id": deal_id,
        "fields": {
            "UF_CRM_1738270468": f"Pendencias Financeiras: {pendencias_financeiras.upper() if pendencias_financeiras else 0} "
                                f"Pendencias Internas: {pendencias_internas.upper() if pendencias_internas else 0} "
                                f"Protestos do Estado: {protestos_do_estado.upper() if protestos_do_estado else 0 } "
                                f"Cheques sem fundos: {cheques_sem_fundos.upper() if cheques_sem_fundos else 0 } ",

            "UF_CRM_1738270439": f"Status Aprovação: {status_aprovacao.upper()} "
                                f": {score} ",

            "UF_CRM_1738599835": f"Tipo de Imagem: {comprovante_komunicar.upper()} "
                                f"Vendedor: {comprovante_vendedor.upper()} "

        }
    }

    update_response = requests.post(f"{BITRIX_API_URL}/crm.deal.update", json=update_payload)
    
    if update_response.status_code != 200:
        return jsonify({"error": "Erro ao atualizar o status no Bitrix", "details": update_response.text}), 500

    return jsonify({"message": "Cliente validado com sucesso", "data": blink_response.json()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3558, debug=True)
