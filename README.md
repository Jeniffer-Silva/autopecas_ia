# 🚗 AutoPeças AI

Agente de IA para consulta de peças automotivas a partir de perguntas em linguagem natural e de um catálogo estruturado de produtos.

🌐 **Aplicação pública:** https://assistente-autopecas.streamlit.app

## 📌 Sobre o projeto

### Problema

Um cliente ou vendedor precisa consultar rapidamente informações sobre peças automotivas, como disponibilidade, preço e compatibilidade com determinado veículo.

### Solução

O **AutoPeças AI** recebe perguntas em linguagem natural, utiliza o Google Gemini para interpretar a solicitação, consulta um catálogo de autopeças e retorna uma resposta amigável com os dados encontrados.

A aplicação possui validações de entrada e regras para evitar consultas inadequadas e impedir a geração de informações que não estejam presentes no catálogo.

## ✅ Funcionalidades

- Consultar peças automotivas em linguagem natural.
- Identificar peça, marca, modelo e ano do veículo.
- Consultar aplicação por veículo e faixa de anos.
- Informar preço e estoque quando disponíveis.
- Informar quando uma peça não é encontrada.
- Rejeitar perguntas fora do escopo.
- Validar anos informados pelo usuário.
- Limitar perguntas a 250 caracteres.
- Disponibilizar a aplicação publicamente na internet.

## 💬 Exemplos de perguntas e respostas esperadas

A aplicação aceita perguntas em linguagem natural relacionadas a autopeças e veículos. Alguns exemplos de utilização são:

### Caso 1 — Peça encontrada

**Pergunta:**

> Tem pastilha de freio para Onix 2020?

**Resposta esperada:**

> Peça encontrada, com informações de aplicação, preço e quantidade disponível em estoque.

---

### Caso 2 — Peça não encontrada

**Pergunta:**

> Tem pastilha para Ferrari 2020?

**Resposta esperada:**

> Não encontrei essa peça no catálogo.

A aplicação não deve inventar preço, estoque ou compatibilidade quando não houver registro correspondente.

---

### Caso 3 — Consulta de preço

**Pergunta:**

> Quanto custa o filtro de óleo do Corolla?

**Resposta esperada:**

> Informar o nome da peça, o preço e a quantidade disponível em estoque, quando houver correspondência no catálogo.

---

### Caso 4 — Consulta de estoque

**Pergunta:**

> Tem filtro de ar para Gol?

**Resposta esperada:**

> Informar se a peça foi encontrada e apresentar o preço e a quantidade disponível em estoque.

---

### Caso 5 — Pergunta fora do escopo

**Pergunta:**

> Qual a previsão do tempo para amanhã?

**Resposta esperada:**

> Não consigo responder essa pergunta. Posso ajudar com consultas sobre autopeças e veículos.

---

### Caso 6 — Linguagem natural

**Pergunta:**

> Oi, preciso de filtro de óleo pro meu Onix, ano 2020. Vocês têm?

**Resposta esperada:**

> Identificar a peça e o veículo, consultar o catálogo e informar a disponibilidade, o preço e o estoque quando houver correspondência.

---

### Caso 7 — Peça inexistente no catálogo

**Pergunta:**

> Tem bomba de combustível para Volkswagen Fusca 1972?

**Resposta esperada:**

> Não encontrei uma peça correspondente no catálogo.

Esse caso também foi utilizado durante a homologação para validar o comportamento do guardrail e sua correção.

---

### Caso 8 — Campo vazio

**Pergunta:**

> *(nenhuma pergunta informada)*

**Resposta esperada:**

> Digite uma pergunta antes de consultar.

---

### Caso 9 — Ano inválido

**Pergunta:**

> Tem pastilha de freio para Chevrolet Onix 2200?

**Resposta esperada:**

> O ano informado está fora de um intervalo válido.

---

### Caso 10 — Ano informado por extenso

**Pergunta:**

> Tem filtro de óleo para Chevrolet Onix dois mil e vinte?

**Resposta esperada:**

> Para evitar interpretações incorretas, informe o ano com quatro dígitos, por exemplo, 2020.

---

### Caso 11 — Pergunta acima de 250 caracteres

**Pergunta:**

> Pergunta com mais de 250 caracteres.

**Resposta esperada:**

> Sua pergunta é muito longa. Digite uma dúvida com até 250 caracteres.


## 🛡️ Validações e guardrails

A aplicação valida a entrada antes de realizar a consulta.

- **Campo vazio:** solicita que o usuário informe uma pergunta.
- **Limite de caracteres:** rejeita perguntas com mais de 250 caracteres.
- **Escopo:** restringe as consultas a autopeças e veículos.
- **Ano inválido:** rejeita anos fora do intervalo definido.
- **Ano por extenso:** solicita o ano com quatro dígitos.
- **Peça não encontrada:** informa a ausência no catálogo sem inventar preço, estoque ou aplicação.

## 🏗️ Arquitetura

![Arquitetura do projeto](arquitetura.png)

### Principais componentes

**Streamlit Cloud** — hospeda a aplicação web.

**`app_langchain.py`** — controla a interface, validações, prompts, comunicação com o modelo e apresentação da resposta.

**Guardrails** — validam a entrada do usuário.

**Google Gemini API** — interpreta a pergunta e gera a resposta final.

**LangChain** — estrutura os prompts e a integração com o modelo e a Tool.

**`consultar_catalogo`** — realiza a consulta dos dados das peças.

**`catalogo_pecas.csv`** — fonte de dados utilizada pela aplicação.

**Streamlit Secrets** — armazena a chave da API sem expô-la no código-fonte ou no GitHub.

### Fluxo

1. O usuário envia uma pergunta.
2. Os guardrails validam a entrada.
3. O Gemini interpreta a solicitação.
4. A aplicação identifica peça, marca, modelo e ano.
5. A Tool `consultar_catalogo` consulta `catalogo_pecas.csv`.
6. O resultado é enviado ao modelo para geração da resposta final.
7. A resposta é apresentada ao usuário.

## 🤖 Integração com LangChain

O projeto utiliza:

- `ChatPromptTemplate`;
- `ChatOpenAI`;
- Tool `consultar_catalogo`.

A primeira chamada ao modelo transforma a pergunta em uma estrutura com:

```json
{
  "peca": "...",
  "marca": "...",
  "modelo": "...",
  "ano": 2020
}
```

Esses dados são utilizados pela Tool para consultar o catálogo. Em seguida, o resultado da consulta é enviado ao modelo para geração da resposta final.

## 📊 Dados

A fonte de dados é o arquivo `catalogo_pecas.csv`.

| Campo | Tipo | Objetivo |
|---|---|---|
| `código` | texto | Identificar a peça |
| `peca` | texto | Nome da peça |
| `marca` | texto | Marca do veículo |
| `modelo` | texto | Modelo do veículo |
| `ano_inicio` | inteiro | Primeiro ano compatível |
| `ano_fim` | inteiro | Último ano compatível |
| `preco` | decimal | Preço da peça |
| `estoque` | inteiro | Quantidade disponível |

## 🚫 Fora do escopo

O AutoPeças AI foi desenvolvido para **consulta de informações do catálogo**.

Não fazem parte do escopo atual:

- venda de produtos;
- pagamentos;
- cadastro de clientes;
- criação de pedidos;
- controle de estoque real;
- consulta a fornecedores;
- envio de mensagens pelo WhatsApp ou ferramentas similares;
- diagnóstico mecânico;
- recomendação de manutenção;
- utilização de banco de dados como fonte principal.

## 🧪 Homologação

A aplicação foi testada no ambiente público.

| Cenário | Resultado |
|---|---|
| Consulta válida | ✅ Aprovado |
| Campo vazio | ✅ Aprovado |
| Pergunta fora do escopo | ✅ Aprovado |
| Ano inválido | ✅ Aprovado |
| Ano por extenso | ✅ Aprovado |
| Mais de 250 caracteres | ✅ Aprovado |
| Produto inexistente no catálogo | ✅ Aprovado |
| Reteste após ajuste do guardrail | ✅ Aprovado |
| Acesso público sem autenticação | ✅ Aprovado |

As evidências estão na pasta:

```text
evidencias_homologacao/
```

### Ajuste realizado durante a homologação

Durante os testes, uma consulta sobre **bomba de combustível** foi inicialmente bloqueada pelo guardrail porque os termos correspondentes não estavam na lista de palavras-chave.

A regra foi ajustada e o teste foi repetido localmente e no ambiente público. Após a correção, a consulta passou corretamente para a etapa de consulta ao catálogo, que informou a ausência da peça sem inventar dados.

## 🔐 Segurança da API

A chave do Google Gemini não é armazenada no código-fonte.

Localmente, é utilizada em:

```text
.streamlit/secrets.toml
```

com:

```toml
GOOGLE_API_KEY = "SUA_CHAVE"
```

Esse arquivo está protegido pelo `.gitignore`.

Em produção, a chave é armazenada nos **Secrets do Streamlit Cloud**.

## 🛠️ Tecnologias

- Python
- Streamlit
- LangChain
- Google Gemini API
- Git
- GitHub
- Streamlit Community Cloud
- CSV

## 📦 Dependências

As dependências diretas do projeto estão definidas em `requirements.txt`:

```text
streamlit==1.61.1
langchain-core==1.5.4
langchain-openai==1.5.0
openai==3.0.0
```

## ▶️ Como executar localmente

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd autopecas_ia
```

### 2. Criar o ambiente virtual

```powershell
python -m venv .venv
```

### 3. Ativar o ambiente

```powershell
.venv\Scripts\activate
```

### 4. Instalar as dependências

```powershell
pip install -r requirements.txt
```

### 5. Configurar a API

Criar o arquivo:

```text
.streamlit/secrets.toml
```

com:

```toml
GOOGLE_API_KEY = "SUA_CHAVE"
```

### 6. Executar

```powershell
streamlit run app_langchain.py
```

## 🌐 Deploy

A aplicação está publicada no **Streamlit Community Cloud**.

**URL pública:** https://assistente-autopecas.streamlit.app

O código é versionado no GitHub e o aplicativo é atualizado a partir do repositório conectado ao Streamlit Cloud.

O repositório pode permanecer privado enquanto a aplicação é disponibilizada publicamente.

## 📁 Estrutura do projeto

```text
autopecas_ia/
│
├── .streamlit/
│   └── secrets.toml # criado localmente
├── evidencias_homologacao/
├── app.py
├── app_langchain.py
├── catalogo_pecas.csv
├── ferramentas.py
├── arquitetura.png
├── requirements.txt
├── README.md
└── .gitignore
```

> `.streamlit/secrets.toml` não é versionado no GitHub.

## ✅ Critérios de conclusão

- [x] Funcionar localmente.
- [x] Receber perguntas em linguagem natural.
- [x] Identificar peça e veículo.
- [x] Consultar o catálogo.
- [x] Retornar preço e estoque quando disponíveis.
- [x] Informar quando não encontrar a peça.
- [x] Funcionar por meio de interface web.
- [x] Estar versionado no GitHub.
- [x] Possuir README.
- [x] Estar publicado em nuvem.
- [x] Possuir URL pública funcionando.
- [x] Possuir evidências de homologação.

## 📌 Resultado

O **AutoPeças AI** demonstra a aplicação de IA generativa, LangChain, ferramentas de consulta, validações de entrada e publicação em nuvem para solucionar um cenário de consulta de peças automotivas.

🌐 **Acesse:** https://assistente-autopecas.streamlit.app