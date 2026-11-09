import joblib, streamlit as st, pandas as pd
from pypdf import PdfReader
from preprocess import limpar_texto
from llm import analisar

st.set_page_config(page_title="Analise Inteligente de Curriculos", layout="wide")
st.title("Analise Inteligente de Curriculos")
st.caption("Apoio a recrutamento: a decisao final e sempre humana.")

@st.cache_resource
def carregar(): return joblib.load("models/classificador.joblib")
modelo = carregar()

def ler_pdf(f): return "\n".join((p.extract_text() or "") for p in PdfReader(f).pages)

c1, c2 = st.columns(2)
with c1:
    arq = st.file_uploader("Curriculo (PDF ou TXT)", type=["pdf", "txt"])
    texto = st.text_area("...ou cole o texto do curriculo", height=150)
with c2:
    vaga = st.text_area("Descricao da vaga", height=250)

if st.button("Analisar", type="primary"):
    if arq: texto = ler_pdf(arq) if arq.name.endswith(".pdf") else arq.read().decode("utf-8", "ignore")
    if not texto.strip() or not vaga.strip(): st.error("Informe curriculo e vaga."); st.stop()
    proba = modelo.predict_proba([limpar_texto(texto)])[0]
    top = pd.Series(proba, index=modelo.classes_).sort_values(ascending=False).head(3)
    st.subheader("1) Classificacao (Machine Learning)")
    st.bar_chart(top)
    st.write(f"Area prevista: **{top.index[0]}** ({top.iloc[0]:.0%})")
    with st.spinner("Consultando o LLM..."):
        try: r = analisar(texto, vaga, top.index[0], float(top.iloc[0]))
        except Exception as e: st.error(f"Falha no LLM: {e}"); st.stop()
    st.subheader("2) Analise (LLM)")
    st.metric("Aderencia a vaga", f"{r['nota_aderencia']}/100"); st.progress(int(r["nota_aderencia"]) / 100)
    st.write(r["resumo"]); st.write("**Habilidades:**", ", ".join(r["habilidades"]))
    a, b = st.columns(2)
    a.success("Pontos fortes\n\n" + "\n".join(f"- {x}" for x in r["pontos_fortes"]))
    b.warning("Lacunas\n\n" + "\n".join(f"- {x}" for x in r["lacunas"]))
    st.info("Justificativa: " + r["justificativa"])
    st.write("**Perguntas para entrevista:**")
    for p in r["perguntas_entrevista"]:
        st.write("-", p)
    rel = f"RELATORIO\nArea: {top.index[0]}\nAderencia: {r['nota_aderencia']}\n{r['justificativa']}"
    st.download_button("Baixar relatorio", rel, "relatorio.txt")
    st.caption("Aviso: resultado automatico, sujeito a erros e vieses. Revisao humana obrigatoria.")
