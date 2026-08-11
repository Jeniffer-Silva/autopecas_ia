##### Identidade do projeto



**Nome:** AutoPeças AI



**Descrição curta:** Agente de IA para consulta e cotação de peças automotivas a partir de um catálogo de produtos.



**Problema:** Um cliente ou vendedor precisa consultar rapidamente informações sobre peças automotivas, como disponibilidade, preço e compatibilidade com determinado veículo.



**Solução:** Um agente de IA que recebe perguntas em linguagem natural, consulta um catálogo de peças e retorna informações sobre preço e estoque.



###### Escopo

1\. Consultar peças.

&#x09;Exemplo: "Tem pastilha de freio para Onix 2020?"

2\. Informar preço.

&#x09;Exemplo: "Quanto custa o filtro de óleo do Corolla?"



3\. Informar estoque

Exemplo: "Tem filtro de ar para Gol?"



4\. Considerar veículo/ano

Exemplo: "Quero uma pastilha para um Onix 2020."



5\. Informar quando não encontrar

Exemplo: "Tem peça para Ferrari 2020?"



Resposta:

"Não encontrei uma peça compatível no catálogo."



###### Fora do escopo

* Vender
* Receber pagamento
* Cadastrar cliente
* Criar pedido
* Controlar estoque real
* Consultar fornecedores
* Enviar WhatsApp
* Fazer diagnóstico mecânico
* Recomendar manutenção
* Trabalhar com banco de dados

###### 

###### Dados

Há um catálogo fictício *catalogo\_pecas.csv*, onde os dados sobre os produtos ficam salvos.



Segue colunas, tipo de dados e objetivo da coluna:



1. código (texto): Identificar a peça
2. peca (texto): Nome da peça
3. marca (texto): Marca do veículo
4. modelo (texto): Modelo do veículo
5. ano\_inicio(inteiro): Primeiro ano compatível
6. ano\_fim (inteiro): Último ano compatível
7. preco (float): Preço da peça
8. estoque (inteiro): Quantidade disponível



###### Casos de teste

###### Teste 1: Peça encontrada

* Pergunta: "Tem pastilha de freio para Onix 2020?"
* Resposta esperada: "Peça encontrada - Preço - Quantidade disponível no estoque"



###### Teste 2: Peça não encontrada

* Pergunta: "Tem pastilha para Ferrari 2020?"
* Resposta esperada: "Não encontrei essa peça no catálogo."



###### Teste 3: Consulta de preço

* Pergunta: "Quanto custa o filtro de óleo do Corolla?"
* Resposta esperada: "Nome - Preço - Quantidade disponível no estoque
* "



###### Teste 4: Estoque

* Pergunta: "Tem filtro de ar para Gol?"
* Resposta esperada: "Peça encontrada - Preço - Quantidade disponível no estoque"



###### Teste 5: Pergunta fora do catálogo

* Pergunta: "Qual é o melhor carro do Brasil?"
* Resposta esperada: "Não consigo responder essa pergunta, meu objetivo é consultar o catálogo de peças."



###### Teste 6: Linguagem natural

* Pergunta: "Oi, preciso trocar as pastilhas do meu Onix, ano 2020. Vocês têm?
* Resposta esperada: "Peça encontrada - Preço - Quantidade disponível no estoque"



###### Critérios de projeto concluído



O AutoPeças AI estará concluído quando conseguir:

1. receber uma pergunta;
2. identificar a peça/veículo;
3. consultar o CSV;
4. retornar preço e estoque;
5. informar quando não encontrar;
6. funcionar pela interface web;
7. estar no GitHub;
8. ter README;
9. estar publicado na nuvem;
10. ter uma URL funcionando.

