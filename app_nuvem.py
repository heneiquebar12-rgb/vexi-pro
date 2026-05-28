import streamlit as st
from supabase import create_client, Client
import pandas as pd
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="VEXI PRO - Dashboard", layout="wide", initial_sidebar_state="collapsed")

# --- CONEXÃO COM O BANCO DE DADOS ---
SUPABASE_URL = "https://pbmdxjmbheezfyekjfno.supabase.co"
SUPABASE_KEY = "sb_publishable_OYnmIG8pxGZiNfv82fgVBg_9-u4WhZV"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# --- ESTILIZAÇÃO CINEMÁTICA ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e2e8f0; }
    .stMetric { background-color: #111827; padding: 15px; border-radius: 10px; border: 1px solid #1f2937; }
    div[data-testid="stMetricValue"] { color: #00ffcc; font-family: 'Courier New', monospace; }
    </style>
""", unsafe_allow_html=True)

st.title("ミ★ VEXI PRO • INTELIGÊNCIA ARTIFICIAL ★彡")
st.write("Painel de Monitoramento Avançado em Nuvem — Operando 100% Real")

# --- PUXAR DADOS DA NUVEM ---
try:
    # Puxa os últimos 15 sinais direto do Supabase ordenados pelo mais recente
    response = supabase.table("sinais_vexi").select("*").order("id", desc=True).limit(15).execute()
    dados_nuvem = response.data
except Exception as e:
    st.error(f"Erro ao conectar com o banco de dados: {e}")
    dados_nuvem = []

if dados_nuvem:
    df = pd.DataFrame(dados_nuvem)
    
    # Card do Último Sinal Emitido
    ultimo = df.iloc[0]
    
    st.subheader("🚨 Último Alerta Detectado")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="📊 ATIVO", value=ultimo['ativo'])
    with col2:
        # Cor de destaque baseada na direção
        tipo_str = ultimo['tipo']
        st.metric(label="⚡ GATILHO", value=tipo_str)
    with col3:
        st.metric(label="🎯 PREÇO DE ENTRADA", value=f"${ultimo['preco']}")
    with col4:
        st.metric(label="🔥 CONFIANÇA IA", value=ultimo['prob'])
        
    st.info(f"**Estratégia:** {ultimo['padrao']} | **Alvos:** SL: {ultimo['sl']} / TP: {ultimo['tp']} | **Relação RR:** {ultimo['rr']}")
    
    # Tabela de Histórico Recente
    st.markdown("---")
    st.subheader("📜 Histórico dos Últimos Sinais Gravados na Nuvem")
    
    # Renomeia as colunas para exibição limpa
    df_exibir = df[['hora', 'ativo', 'tipo', 'preco', 'tp', 'sl', 'prob', 'rr', 'padrao']].copy()
    df_exibir.columns = ['Hora', 'Ativo', 'Tipo', 'Preço Entrada', 'Take Profit', 'Stop Loss', 'Confiança', 'R:R', 'Filtro Base']
    
    st.dataframe(df_exibir, use_container_width=True)
else:
    st.warning("⏳ Aguardando o primeiro sinal do motor local ser enviado para a nuvem...")

# Auto-refresh de 5 em 5 segundos para atualizar a tela sozinho
time.sleep(5)
st.rerun()