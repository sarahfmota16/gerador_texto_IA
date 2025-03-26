from transformers import pipeline
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DIR_TEXTOS = "textos_gerados"
os.makedirs(DIR_TEXTOS, exist_ok=True)   

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

generator = pipeline("text-generation", model="microsoft/phi-2", eos_token_id=50256) 

@app.post("/gerar_texto/")
def gerar_e_armazenar_texto(request: PromptRequest):
    try:
        texto_gerado = generator(
            request.prompt,
            max_new_tokens=80,  
            temperature=0.01,
            top_p=0.99,
            repetition_penalty=1.5,  
            do_sample=True,
            num_return_sequences=1,
            num_beams=1 
        )[0]["generated_text"]

        def remover_repeticoes(texto):
            frases = texto.split(". ")
            resultado = []
            for frase in frases:
                if frase not in resultado:
                    resultado.append(frase)
            return ". ".join(resultado)

        texto_gerado = remover_repeticoes(texto_gerado)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"{DIR_TEXTOS}/texto_{timestamp}.txt"

        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(texto_gerado)

        logging.info(f"Texto gerado e salvo: {nome_arquivo}")

        return {"mensagem": "Texto gerado com sucesso!", "arquivo": nome_arquivo, "texto": texto_gerado}

    except Exception as e:
        logging.error(f"Erro ao gerar texto: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a requisição")