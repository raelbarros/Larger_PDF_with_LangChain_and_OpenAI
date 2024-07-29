
# Larger PDF with LangChain and OpenAI

O objetido do projeto é processar PDF Grande utilizando a lib LangChain, clusterizar a pagina e enviar para o ChatGPT e extraindo informações importantes.

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
├── main.py                 # Instruções principais
├── streamlit               # Aplicação do streamlit
├── requirements.txt        # Pacotes do projeto
└── README.md               # Documentação do Projeto

```
## Como executar

Recomenda-se a criação de um ambiente virtual (venv) para instalações dos pacotes do projeto.

```bash
  pip install -r requirements.txt
```
    
##### 1. Usando via arquivo .py

Acessar o arquivo `main.py` alterar a variavel `pdf_in_path` do PDF de entrada e a variavel `pdf_out_path` com o nome do PDF de saida.


##### 2. Usando via streamlit [BETA]

Desenvolvemos uma interface visual utilizando o Streamlit facilidando o uso da aplicação.
> [!WARNING]  
> Essa funcionalidade ainda está em beta.

Para inicializar o streamlit execute o seguinte comando:

```bash
streamlit run streamlit.py
```

## Logica

Utilizamos a biblioteca LangChain, mais especificamente a função PyPDFLoader, para realizar a leitura completa de documentos. O texto extraído é então submetido a um processo de redução de dimensionalidade baseado em similaridade semântica. Essa etapa visa diminuir a quantidade de tokens, simplificando o processamento subsequente.

Em seguida, empregamos técnicas de embedding para converter o texto em representações numéricas (vetores). Esses vetores são utilizados como entrada para um modelo de clusterização, que tem como objetivo agrupar partes do texto com temáticas semelhantes.

Após a aplicação do modelo de clusterização, identificamos os tópicos mais relevantes presentes no documento. Com base nessa análise, reordenamos o texto de acordo com a importância de cada tópico, gerando um novo documento com uma estrutura mais organizada e informativa.

Com o texto reorganizado, geramos prompts específicos para cada pergunta e os enviamos ao ChatGPT para obter as informações relevantes.


## Limitações

- Numero idela de cluster do modelo K-Means pode variar de acordo com o tamanho do documento.
- Limitação de tokens da API da OpenAI

## Referencias

- https://medium.com/@myscale/how-to-summarize-large-documents-with-langchain-and-openai-4312568e80b1
- https://medium.com/@johnidouglasmarangon/how-to-summarize-text-with-openai-and-langchain-e038fc922af
- https://www.youtube.com/watch?v=qaPMdcCqtWk&t=870s
- https://github.com/gkamradt/langchain-tutorials/blob/main/data_generation/5%20Levels%20Of%20Summarization%20-%20Novice%20To%20Expert.ipynb
- https://thenewstack.io/how-to-summarize-large-documents-with-langchain-and-openai/
