
# =====================================================================
# ETAPA 1 - PARÂMETROS (altere aqui)
# =====================================================================

M0 = 0.00      # Saldo inicial (R$)
A = 5000.00     # Aporte mensal (R$)
N = 150        # Prazo em meses (10 anos)

# Rentabilidade de cada classe (% ao ANO, valores hipotéticos)
RENDAFIXA_AA = 10.0
PREFIXADO_AA = 11.0
IPCA_AA      = 10.5
ACOES_AA     = 14.0
FIIS_AA      = 12.0

# Taxa de administração de cada modalidade (% ao ANO)
TAXAADM_C_AA = 0.2   # Conservadora
TAXAADM_M_AA = 0.5   # Moderada
TAXAADM_A_AA = 1.0   # Arrojada


# =====================================================================
# ETAPA 2 - CONVERSÃO DE TAXA ANUAL PARA MENSAL
# r_mensal = (1 + r_anual)^(1/12) - 1
# =====================================================================

def mensal(taxa_aa):
    return (1 + taxa_aa / 100) ** (1 / 12) - 1


RENDAFIXA = mensal(RENDAFIXA_AA)
PREFIXADO = mensal(PREFIXADO_AA)
IPCA      = mensal(IPCA_AA)
ACOES     = mensal(ACOES_AA)
FIIS      = mensal(FIIS_AA)


# =====================================================================
# ETAPA 3 - TAXA LÍQUIDA (TL) DE CADA MODALIDADE
# =====================================================================

TLC = 0.70*RENDAFIXA + 0.10*PREFIXADO + 0.20*IPCA - mensal(TAXAADM_C_AA)
TLM = 0.40*RENDAFIXA + 0.10*PREFIXADO + 0.15*IPCA + 0.25*ACOES + 0.10*FIIS - mensal(TAXAADM_M_AA)
TLA = 0.15*RENDAFIXA + 0.05*PREFIXADO + 0.10*IPCA + 0.55*ACOES + 0.15*FIIS - mensal(TAXAADM_A_AA)


# =====================================================================
# ETAPA 4 - SIMULAÇÃO (equação de transição)
# M[n+1] = (M[n] + A) · (1 + TL), arredondado em centavos
# =====================================================================

def simular(m0, aporte, tl, n_meses):
    m = m0
    for n in range(n_meses):
        m = round((m + aporte) * (1 + tl), 2)
    return m


# =====================================================================
# ETAPA 5 - SOLUÇÃO ANALÍTICA (fórmula fechada)
# M[N] = M0·(1+TL)^N + A·[(1+TL)^N − 1] / TL · (1+TL)
# =====================================================================

def analitica(m0, aporte, tl, n_meses):
    f = (1 + tl) ** n_meses
    return m0 * f + aporte * (f - 1) / tl * (1 + tl)


# =====================================================================
# ETAPA 6 - REGRA DE PROTEÇÃO (restrição do modelo)
# Os pesos de uma carteira devem somar 100%.
# =====================================================================



def validar_pesos(pesos):          
    if sum(pesos) != 100:
        raise ValueError(f"Pesos somam {sum(pesos)}%; devem somar 100%.")


# =====================================================================
# ETAPA 7 - VERIFICAÇÃO
# =====================================================================

def teste_caso_limite():
    # Com taxa zero não há juros: o montante deve ser só a soma dos aportes.
    resultado = simular(M0, A, 0.0, N)
    esperado = M0 + N * A
    print(f"Caso-limite (TL = 0): simulado R$ {resultado:,.2f} | esperado R$ {esperado:,.2f} ->",
          "OK" if resultado == esperado else "FALHA")


def teste_correspondencia_logica():
    # Uma carteira com pesos somando 90% deve ser rejeitada.
    try:
        validar_pesos([90, 10])
        print("Correspondência de lógica (pesos = 90%): aceita -> FALHA")
    except ValueError as erro:
        print(f"Correspondência de lógica (pesos = 90%): rejeitada -> OK ({erro})")


def teste_solucao_analitica():
    # Simulação mês a mês × fórmula fechada, carteira Moderada.
    sim = simular(M0, A, TLM, N)
    ana = analitica(M0, A, TLM, N)
    dif = sim - ana
    print(f"Solução analítica (Moderada): simulado R$ {sim:,.2f} | analítico R$ {ana:,.2f} | "
          f"diferença R$ {dif:,.2f} ->", "OK" if abs(dif) < 0.50 else "FALHA")


# =====================================================================
# ETAPA 8 - EXECUÇÃO
# =====================================================================

if __name__ == "__main__":
    
    print(f"M0 = R$ {M0:,.2f} | A = R$ {A:,.2f} | N = {N} meses\n")
    for nome, tl in [("Conservadora", TLC), ("Moderada", TLM), ("Arrojada", TLA)]:
        print(f"{nome:<13} TL = {tl*100:.4f}% a.m. | montante final = R$ {simular(M0, A, tl, N):,.2f}")
    print("\n--- Verificação ---")
    teste_caso_limite()
    teste_correspondencia_logica()
    teste_solucao_analitica()
