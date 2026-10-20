import time
import matplotlib.pyplot as plt
import numpy as np
import random

# =========================================================
# 1. PARÂMETROS DA SIMULAÇÃO (Configurável para a aula)
# =========================================================

tempo_total = 30           # Duração total da simulação (segundos)
tempo_troca_sinal = 10     # O semáforo troca a cada X segundos
chegadas_por_segundo = 2   # Quantos carros entram na fila por segundo
saida_por_segundo = 3      # Quantos carros passam por segundo (se VERDE)
fila = 0                   # Fila inicial

# Controle do Semáforo
sinal = "VERMELHO"
tempo_no_sinal = 0

historico_tempo = []
historico_fila = []

# =========================================================
# 2. EXECUÇÃO DA SIMULAÇÃO
# =========================================================

print("--- INÍCIO DA SIMULAÇÃO ---")

for t in range(tempo_total):

    # Se deu o tempo limite do semáforo, inverte o sinal e zera o contador
    if tempo_no_sinal == tempo_troca_sinal:
        if sinal == "VERMELHO":
            sinal = "VERDE"
        else:
            sinal = "VERMELHO"
        tempo_no_sinal = 0

for t in range(tempo_total):

    # Se deu o tempo limite do semáforo, inverte o sinal e zera o contador
    if tempo_no_sinal == tempo_troca_sinal:
        if sinal == "VERMELHO":
            sinal = "VERDE"
        else:
            sinal = "VERMELHO"
        tempo_no_sinal = 0

    # Lógica de saída de carros
    if sinal == "VERMELHO":
        saida = 0
    else:
        saida = saida_por_segundo

    # Equação de Estado: Fila nova = Fila antiga + Chegadas - Saídas
    fila += chegadas_por_segundo - saida

    # Regra: Fila não fica negativa
    if fila < 0:
        fila = 0

    # Salva dados para o gráfico
    historico_tempo.append(t)
    historico_fila.append(fila)

    # Imprime os logs em tempo real
    print(f"Tempo: {t:02d}s | Sinal: {sinal:8s} | Fila: {fila:2d} carros")
    time.sleep(0.5)

    # Conta +1 segundo para o sinal atual
    tempo_no_sinal += 1

print("--- FIM DA SIMULAÇÃO ---")


plt.step(historico_tempo, historico_fila, where='post')
plt.title("Simulação Discreta: Fila de Carros no Semáforo")
plt.xlabel("Tempo (segundos)")
plt.ylabel("Nº de Carros na Fila")
plt.grid(True, linestyle="--", alpha=0.7)
plt.show()


