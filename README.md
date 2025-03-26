# Geração de Texto com FastAPI e Transformers 📜

Este projeto utiliza o modelo `microsoft/phi-2` da biblioteca `transformers` para gerar texto a partir de prompts fornecidos via uma API FastAPI. Os textos gerados são armazenados em arquivos `.txt`.

## Instalação 🔧

1.  Clone este repositório:

    ```bash
    git clone <URL_do_seu_repositório>
    cd <nome_do_repositório>
    ```

2.  Instale as dependências:

    ```bash
    pip install transformers fastapi uvicorn pydantic
    ```

## Execução 

1.  Execute o servidor FastAPI:

    ```bash
    uvicorn main:app --reload
    ```

2.  A API estará disponível em `http://127.0.0.1:8000`.

## Uso

### Endpoint: `/gerar_texto/`

* **Método:** `POST`
* **Corpo da requisição:**

    ```json
    {
        "prompt": "Seu prompt de texto aqui"
    }
    ```

* **Resposta:**

    ```json
    {
        "mensagem": "Texto gerado com sucesso!",
        "arquivo": "textos_gerados/texto_YYYYMMDD_HHMMSS.txt",
        "texto": "Texto gerado pelo modelo."
    }
    ```

    * `mensagem`: Indica o sucesso da operação.
    * `arquivo`: Caminho para o arquivo `.txt` contendo o texto gerado.
    * `texto`: O texto gerado pelo modelo.

## Detalhes da Implementação

* O modelo `microsoft/phi-2` é utilizado para geração de texto.
* Os textos gerados são salvos no diretório `textos_gerados/`, com nomes de arquivo baseados no timestamp.
* A API utiliza `FastAPI` para receber prompts e retornar os textos gerados.
* A classe `PromptRequest` (usando `pydantic`) define o formato esperado para os prompts de entrada.
* A função `remover_repeticoes` remove frases repetidas do texto gerado.
* Logging é utilizado para registrar informações e erros durante a execução.
