
# Project IPA - Batalha de Dados (Hacka 02)

Projeto desenvolvido pela equipe Hacka 02 da 27º Batalha de Dados do Itaú Unibanco.

Esse projeto busca otimizar a triagem de petições de Recuperação Judicial, desenvolvendo um sistema automatizado que processa documentos PDF de grande volume, apoiando na identificação de informações importantes.

O projeto foi desenvolvido em Python com as libs LangChain e OpenAI





## Como executar

Recomenda-se a criação de um ambiente virtual (venv) para instalações dos pacotes do projeto.

```bash
  pip install -r requirements.txt
```
    
### Usando via arquivo .py

Acessar o arquivo `dasdas` alterar a variavel `asdas` para o caminho do PDF desejado.

!!!! COLOCAR PRINT

### Usando via streamlit [BETA]

> [!WARNING]  
> Essa funcionalidade ainda está em beta.

Desenvolvemos uma interface visual utilizando o Streamlit facilidando o uso da aplicação.

Para inicializar o streamlit execute o seguinte comando:

```bash
streamlit run streamlit.py
```