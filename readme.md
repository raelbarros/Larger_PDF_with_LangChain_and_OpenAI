
# Project IPA - Batalha de Dados (Hacka 02)

Projeto desenvolvido pela equipe Hacka 02 da 27º Batalha de Dados do Itaú Unibanco.

Esse projeto busca otimizar a triagem de petições de Recuperação Judicial, desenvolvendo um sistema automatizado que processa documentos PDF de grande volume, apoiando na identificação de informações importantes.

O projeto foi desenvolvido em Python com as libs LangChain e OpenAI.

## Organização
```
projeto/
├── .streamlit/             # Pasta de configuração do Streamlit
│   └── config.tom          # Arquivo de configuração do streamlit
├── data/                   # Pasta local para manipulação de arquivos via streamlit
│   ├── input/              # Pasta para armazenar arquivos de entrada
│   └── output/             # Pasta para armazenar arquivos de saida
├── handler/                # Pasta com classes de manipulação de dados 
│   ├── ml_handler.py       # Funções com Machine Learning
│   ├── pdf_handler.py      # Funções para manipulação de documentos PDF
│   └── utils.py            # Funções auxiliares do software
├── dev.ipynb               # Notebook de experimentação
├── main.py                 # Instruções principais
├── streamlit               # Aplicação do streamlit
├── requirements.txt        # Pacotes do projeto
└── docs/                   # Pasta com a documentação do Projeto

```
## Como executar

Recomenda-se a criação de um ambiente virtual (venv) para instalações dos pacotes do projeto.

```bash
  pip install -r requirements.txt
```
    
##### 1. Usando via arquivo .py

Acessar o arquivo `dasdas` alterar a variavel `asdas` do PDF de entrada e a variavel `asdff` com o nome do PDF de saida

!!!! COLOCAR PRINT

##### 2. Usando via streamlit [BETA]

Desenvolvemos uma interface visual utilizando o Streamlit facilidando o uso da aplicação.
> [!WARNING]  
> Essa funcionalidade ainda está em beta.

para inicializar o streamlit execute o seguinte comando:

```bash
streamlit run streamlit.py
```

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

## Logica

Utilizamos a biblioteca LangChain, mais especificamente a função PyPDFLoader, para realizar a leitura completa de documentos. O texto extraído é então submetido a um processo de redução de dimensionalidade baseado em similaridade semântica. Essa etapa visa diminuir a quantidade de tokens, simplificando o processamento subsequente.

Em seguida, empregamos técnicas de embedding para converter o texto em representações numéricas (vetores). Esses vetores são utilizados como entrada para um modelo de clusterização, que tem como objetivo agrupar partes do texto com temáticas semelhantes.

Após a aplicação do modelo de clusterização, identificamos os tópicos mais relevantes presentes no documento. Com base nessa análise, reordenamos o texto de acordo com a importância de cada tópico, gerando um novo documento com uma estrutura mais organizada e informativa.

Com o texto reorganizado, geramos prompts específicos para cada pergunta e os enviamos ao ChatGPT para obter as informações relevantes.


!!! COLOCAR DIAGRAMA

## Proximos passos

Devido as restrições de tempo, não foi possivel implementar todas funcionalidades que desejavamos e entendemos importantes para a aplicação. No entando, para o futuro, enxergamos a solução da seguinte forma.

1. **Adoção do Maestro Streamlit:** Esteira do Streamlit como deploy, possui governança e infraestrutura necessaria (gateway, endpoint etc..).

2. **Banco de dados Transacional (OLTP):** Implantação de um banco de dados para gerenciar requisições do Maestro Streamlit, permitindo armazenamento de historico, buscas etc...

3. **Bucket S3:** Armazenamento dos documentos do processados.

4. **Interagração com o Data Mesh:** Integração com o Data Mesh para de viabilizar visões analiticas mais completas e disponibilidade de dados com outras equipes, caso seja necessario.

5. **Visualização:** Integração com ferramentas de data viz como Tableau e Quicksight para criação de Dashboard personalizados.
