# 💰 Banco Digital - Sistema de Análise Financeira

Sistema simples de simulação de operações bancárias com foco em análise de transações e detecção de gastos suspeitos.  
O projeto integra banco de dados SQLite, processamento com Python e dashboard interativo com Streamlit.

---

## 📌 Objetivo

Simular um ambiente bancário básico para:

- Gerenciar clientes e contas
- Registrar transações financeiras
- Analisar fluxo de caixa
- Detectar possíveis gastos suspeitos
- Visualizar dados em dashboard interativo

---

## 🧠 Funcionalidades

### 🔹 Backend (Python + SQLite)
- Cadastro de clientes
- Criação de contas
- Registro de transações (entrada e saída)
- Persistência em banco SQLite

### 🔹 Análise de Dados (Pandas)
- Agrupamento por mês
- Cálculo de fluxo de caixa
- Ajuste de valores por tipo de transação
- Detecção de anomalias financeiras

### 🔹 Dashboard (Streamlit)
- KPIs financeiros:
  - Entradas totais
  - Saídas totais
  - Saldo
  - Número de transações
- Gráficos:
  - Fluxo de caixa mensal
  - Entradas vs Saídas
- Tabela de transações
- Lista de gastos suspeitos

---

## 🏗️ Estrutura do Projeto

```text
banco_digital/
│
├── main.py
├── app.py
│
├── database/
│   └── init_db.py
│
├── services/
│   ├── cliente_service.py
│   ├── conta_service.py
│   └── transacao_service.py
│
├── analysis/
│   └── analise_financeira.py
│
├── utils/
│   └── helpers.py
│
├── banco.db
````

---

## 🚀 Como executar o projeto

### 1. Clonar repositório

```bash
git clone https://github.com/euwalteraugusto/banco-digital.git
cd banco-digital
```

---

### 2. Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

---

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 4. Inicializar banco e seed

```bash
python main.py
```

---

### 5. Rodar dashboard

```bash
streamlit run app.py
```

---

## 📊 Tecnologias utilizadas

* Python
* SQLite
* Pandas
* Streamlit

---

## 🧪 Exemplo de análise

O sistema detecta automaticamente transações fora do padrão com base em comportamento histórico, destacando possíveis gastos anômalos.

---

## ⚠️ Observações

* O projeto utiliza dados simulados (seed automático)
* Não possui integração com bancos reais
* Foco educacional e demonstrativo

---

## 📈 Possíveis melhorias

* Autenticação de usuários
* API com Flask/FastAPI
* Modelo de score de risco financeiro
* Persistência em PostgreSQL
* Deploy em cloud

---

## 👨‍💻 Autor

Walter Fonseca

Projeto desenvolvido para fins de aprendizado em:

- Engenharia de dados
- Análise financeira
- Estruturação de sistemas backend simples

🔗 LinkedIn: https://www.linkedin.com/in/walteraugusto