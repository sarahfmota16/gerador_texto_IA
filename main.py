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

generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

@app.post("/gerar_texto/")
def gerar_e_armazenar_texto(request: PromptRequest):
    try:
        texto_gerado = generator(
            request.prompt,
            max_length=100,
            temperature=0.7,
            top_p=0.85,
            repetition_penalty=1.2,
            do_sample=True,
            num_beams=5,
            early_stopping=True,
            truncation=True
            )[0]["generated_text"]
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"{DIR_TEXTOS}/texto_{timestamp}.txt"
        
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(texto_gerado)
        
        logging.info(f"Texto gerado e salvo: {nome_arquivo}")
        
        return {"mensagem": "Texto gerado com sucesso!", "arquivo": nome_arquivo, "texto": texto_gerado}
    except Exception as e:
        logging.error(f"Erro ao gerar texto: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a requisição")

