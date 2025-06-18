import streamlit as st
import pandas as pd

# Carica il file CSV con gli annunci immobiliari
data = pd.read_csv("immobili_italia.csv")

st.title("📊 Analisi Immobili per Investimento (Italia)")

# Parametri di input globali per il calcolo
st.sidebar.header("Parametri di calcolo")
tasso_mutuo = st.sidebar.number_input("Tasso mutuo (%)", 0.0, 10.0, 4.0)
durata_anni = st.sidebar.slider("Durata mutuo (anni)", 5, 30, 20)
anticipo = st.sidebar.number_input("Anticipo (%)", 0.0, 100.0, 20.0)
tasse_annual = st.sidebar.number_input("Tasse annuali (€)", 0, 5000, 1000)
assicurazione = st.sidebar.number_input("Assicurazione annuale (€)", 0, 5000, 300)
costi_gestione = st.sidebar.number_input("Gestione annuale (€)", 0, 5000, 500)

# Funzione per calcolo rata mutuo
def calcola_rata_mutuo(prezzo, anticipo, tasso_annuo, anni):
    prestito = prezzo * (1 - anticipo / 100)
    rate = anni * 12
    tasso_mensile = tasso_annuo / 100 / 12
    if tasso_mensile == 0:
        return prestito / rate
    return prestito * (tasso_mensile * (1 + tasso_mensile) ** rate) / ((1 + tasso_mensile) ** rate - 1)

# Calcolo rendimento per ogni immobile
results = []
for idx, row in data.iterrows():
    prezzo = row["prezzo"]
    affitto = row["affitto_mensile"]
    rata = calcola_rata_mutuo(prezzo, anticipo, tasso_mutuo, durata_anni)
    spese_annue = tasse_annual + assicurazione + costi_gestione
    spese_mensili = spese_annue / 12
    cash_flow = affitto - rata - spese_mensili
    investimento_iniziale = prezzo * (anticipo / 100)
    coc_return = (cash_flow * 12) / investimento_iniziale * 100

    results.append({
        "Città": row["città"],
        "Prezzo (€)": prezzo,
        "Affitto (€)": affitto,
        "Cash Flow (€)": round(cash_flow, 2),
        "Cash-on-Cash Return (%)": round(coc_return, 2),
        "Link": row["link"]
    })

# Mostra i risultati in una tabella ordinabile
results_df = pd.DataFrame(results)
ordina_per = st.selectbox("Ordina per:", ["Cash-on-Cash Return (%)", "Cash Flow (€)"])
results_df = results_df.sort_values(by=ordina_per, ascending=False).reset_index(drop=True)

st.dataframe(results_df, use_container_width=True)

# Mostra link per ogni riga
for i, riga in results_df.iterrows():
    st.markdown(f"[{riga['Città']} - Vedi annuncio]({riga['Link']})")
