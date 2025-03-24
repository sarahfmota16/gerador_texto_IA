# Use a pipeline as a high-level helper
from transformers import pipeline

text_generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125m")


def gerar_continuacao(texto, max_length=50):
    saidas = text_generator(
        texto,
        max_length=max_length,
        temperature=0.7,
        top_p=0.85,
        repetition_penalty=1.2,
        do_sample=True,
        num_beams=5,
        early_stopping=True,
        truncation=True
    )
    return saidas[0]["generated_text"]

# Recebe o texto do usuário
entrada = input("Digite um texto para continuar: ")

# Gera e exibe a continuação
resultado = gerar_continuacao(entrada)
print("\nContinuação gerada:\n", resultado)