# ⚡ Integração Bitrix24 com a Operadora Blink (Provedor de Internet) via API Flask 🇧🇷  
_(Scroll down for English version 🇺🇸)_

Este projeto foi desenvolvido para **provedores de internet**, como a **Blink**, que utilizam o Bitrix24 como CRM.  
Ele automatiza duas tarefas críticas no fluxo comercial:

- **Verificação de viabilidade técnica de instalação** no endereço do cliente.  
- **Validação completa do cliente** (incluindo CPF, pendências, score e mais).  

Tudo isso é feito via **integração com a API da Blink** e atualização automática no Bitrix24.

---

### ✅ O que essa API faz?

- Consulta os dados de um negócio (deal) no Bitrix24.  
- Envia esses dados para a API da operadora Blink.  
- Recebe as informações de retorno (viabilidade e validação).  
- Atualiza campos personalizados no Bitrix24 automaticamente.  

---

### 🔧 Endpoints disponíveis

1. `POST /api/atualizar_viabilidade/deal_id=<ID>`  
   → Consulta a viabilidade técnica com base no endereço.  

2. `POST /api/validar_cliente/deal_id=<ID>`  
   → Valida os dados do cliente (CPF, nome, score, pendências etc.).  

---

### 📡 Ideal para provedores como a Blink

- Automatize etapas burocráticas do atendimento comercial.  
- Tenha respostas rápidas sobre a viabilidade de instalação.  
- Saiba se o cliente está apto a contratar o serviço.  
- Evite retrabalho e erros manuais ao atualizar o CRM.

---

### 🛡️ Segurança e confiabilidade

- Tokens e URLs sensíveis armazenados via `.env`.  
- Comunicação segura com as APIs da Blink e Bitrix24.  
- Tratamento de erros completo e respostas estruturadas em JSON.  

---

### 📈 Benefícios para provedores de internet

- Mais agilidade no atendimento ao cliente.  
- Integração fluida entre Blink e Bitrix24.  
- Redução de erros e aumento da produtividade do time comercial.  
- Processos mais confiáveis, rápidos e escaláveis.

> É da Blink ou de outro provedor? Personalizamos essa solução para você! 😉

---

# ⚡ Bitrix24 Integration with Blink ISP via Flask API 🇺🇸

This project was built for **internet providers like Blink** that use Bitrix24 as their CRM.  
It automates two key processes in the sales pipeline:

- **Checking installation feasibility** at the customer address.  
- **Validating customer identity and risk data** (CPF, score, debts, etc.).  

All data is exchanged through **Blink’s official API**, and Bitrix24 is updated automatically.

---

### ✅ What this API does

- Fetches deal info from Bitrix24.  
- Sends it to Blink’s API for feasibility and client validation.  
- Receives structured response.  
- Updates Bitrix24 custom fields automatically.  

---

### 🔧 Available endpoints

1. `POST /api/atualizar_viabilidade/deal_id=<ID>`  
   → Checks installation feasibility by address.  

2. `POST /api/validar_cliente/deal_id=<ID>`  
   → Validates customer identity and risk information.  

---

### 📡 Built for ISPs like Blink

- Automate pre-sales validation tasks.  
- Get fast answers on feasibility and customer eligibility.  
- Minimize manual errors and improve CRM data reliability.

---

### 🛡️ Security

- Tokens and sensitive URLs handled via `.env`.  
- Secure HTTPS calls to Blink and Bitrix24 APIs.  
- Full error handling and JSON responses for integration.  

---

### 📈 Benefits for ISPs

- Faster onboarding and lead handling.  
- Real-time risk analysis and feasibility check.  
- Reliable, scalable automation of repetitive tasks.

> Work at Blink or another ISP? We can customize this solution for your business. 😉

