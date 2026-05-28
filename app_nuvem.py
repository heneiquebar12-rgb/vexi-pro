import streamlit as st
import streamlit.components.v1 as components
import os
import json
import time
import pandas as pd
import base64 # Importação necessária para codificar a imagem
from supabase import create_client, Client # <-- ADICIONADO PARA CONEXÃO COM A NUVEM

# Configuração da página
st.set_page_config(page_title="ミ★ ░V░E░X░I░ ★彡  ", layout="wide")

# --- CONEXÃO COM O BANCO DE DADOS NA NUVEM (ADICIONADO) ---
SUPABASE_URL = "https://pbmdxjmbheezfyekjfno.supabase.co"
SUPABASE_KEY = "sb_publishable_OYnmIG8pxGZiNfv82fgVBg_9-u4WhZV"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# Função para codificar a imagem local em base64 (necessário para o Streamlit)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Nome do arquivo da imagem que você salvou na mesma pasta
nome_imagem_fundo = 'background.png' # <- SALVE A IMAGEM FORNECIDA COM ESTE NOME

try:
    bin_str = get_base64_of_bin_file(nome_imagem_fundo)
    background_image_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed; /* Opcional: mantém o fundo fixo ao rolar */
        color: white; /* Mantém a cor do texto padrão */
    }}
    </style>
    """
except FileNotFoundError:
    # Caso a imagem não seja encontrada, mantém o fundo original e avisa
    background_image_style = f"""
    <style>
    .stApp {{ background-color: #0d1117; color: white; }}
    </style>
    """
    st.error(f"Erro: Arquivo de imagem '{nome_imagem_fundo}' não encontrado. Por favor, salve a imagem na mesma pasta do script.")

st.markdown(background_image_style, unsafe_allow_html=True)


st.markdown("""
    <style>
    /* .metric-card e áreas internas agora com transparência (RGBA) */
    .metric-card { background: rgba(22, 27, 34, 0.7); border: 1px solid #30363d; padding: 15px; border-radius: 10px; text-align: center; }
   
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
   
    .vexi-title {
        font-size: 70px !important;
        font-weight: bold;
        margin-bottom: 20px;
        color: white;
        text-shadow: 0px 0px 15px rgba(255,255,255,0.2);
    }

    div[data-baseweb="input"] {
        width: 350px !important;
        margin: 0 auto !important;
    }
   
    div.stButton > button {
        display: block;
        margin: 20px auto;
        width: 200px;
    }

    div[data-testid="stFormElement"] label {
        display: none;
    }

    button[data-baseweb="tab"] {
        font-size: 20px !important;
        border: 2px solid #30363d !important;
        border-radius: 50px !important;
        padding: 10px 25px !important;
        margin: 5px !important;
        background-color: transparent !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #58a6ff !important;
        color: white !important;
        border-color: #58a6ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

def tocar_alerta():
    audio_html = """
        <iframe src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" allow="autoplay" style="display:none"></iframe>
        <audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg"></audio>
    """
    components.html(audio_html, height=0, width=0)

if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    login_placeholder = st.empty()
    with login_placeholder.container():
        st.write("<br><br><br><br><br>", unsafe_allow_html=True)
        st.markdown('<div class="login-container"><h1 class="vexi-title">ミ★ ░V░E░X░I░ ★彡</h1></div>', unsafe_allow_html=True)
       
        _, col_mid, _ = st.columns([1, 1, 1])
        with col_mid:
            senha = st.text_input("Chave de Acesso", type="password", placeholder="Sua Chave de Acesso...", label_visibility="collapsed", key="pw")
            if st.button("Entrar no painel", use_container_width=True):
                if senha == "qqpp12345":
                    st.session_state['auth'] = True
                    login_placeholder.empty()
                    st.rerun()
                else:
                    st.error("Chave incorreta.")
        st.stop()

st.markdown('<div class="login-container"><h1 class="vexi-title">ミ★ ░V░E░X░I░ ★彡</h1></div>', unsafe_allow_html=True)

tab_sinal, tab_calculadora, tab_historico, tab_graficos, tab_mapa, tab_noticias = st.tabs([
    "🔔 SINAL AO VIVO", "📊 CALCULADORA DE RISCO", "📜 HISTÓRICO", "📈 ANÁLISE TÉCNICA", "🔥 HEATMAP", "📰 NOTÍCIAS"
])

# --- LEITURA GLOBAL DA NUVEM (ADICIONADO PARA SUBSTITUIR ARQUIVO LOCAL) ---
dados_robo = {}
dados_h = []

try:
    # Puxa o último sinal e o histórico direto do Supabase
    response = supabase.table("sinais_vexi").select("*").order("id", desc=True).limit(15).execute()
    if response.data:
        # Formata o sinal atual igual ao seu dicionário original esperado
        ultimo = response.data[0]
        dados_robo = {
            "Hora": ultimo["hora"],
            "Ativo": ultimo["ativo"],
            "Tipo": ultimo["tipo"],
            "Preco": ultimo["preco"],
            "TP": ultimo["tp"],
            "SL": ultimo["sl"],
            "Prob": ultimo["prob"],
            "RR": ultimo["rr"],
            "Padrao": ultimo["padrao"]
        }
        
        # Reconstrói a lista do histórico no formato das suas colunas originais
        for item in response.data:
            dados_h.append({
                "Hora": item["hora"], "Ativo": item["ativo"], "Tipo": item["tipo"],
                "Preco": item["preco"], "TP": item["tp"], "SL": item["sl"],
                "Prob": item["prob"], "RR": item["rr"], "Padrao": item["padrao"]
            })
except Exception as e:
    pass

with tab_sinal:
    sinal_container = st.empty()
    if dados_robo:
        tipo_sinal = dados_robo.get('Tipo', '---')
        cor = "#00ff00" if "LONG" in str(tipo_sinal) or "COMPRA" in str(tipo_sinal) else "#ff4b4b"
        horario_entrada = dados_robo.get('Hora', '--:--:--')
        preco = dados_robo.get('Preco') or "0.00"
        padrao_msg = dados_robo.get('Padrao', 'Analisando Mercado...')
        rr_dinamico = dados_robo.get('RR', '---')

        if 'ultimo_sinal' not in st.session_state:
            st.session_state['ultimo_sinal'] = horario_entrada
       
        if horario_entrada != st.session_state['ultimo_sinal']:
            tocar_alerta()
            st.toast(f"🚀 NOVO SINAL: {tipo_sinal}", icon="🔔")
            st.session_state['ultimo_sinal'] = horario_entrada
       
        with sinal_container.container():
            st.markdown(f"""
            <div style="border: 2px solid {cor}; padding: 30px; border-radius: 15px; background-color: rgba(22, 27, 34, 0.85);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <h2 style="margin:0; color: white;">💎 {dados_robo.get('Ativo', '---')}</h2>
                    <div style="text-align: right;">
                        <p style="color: #58a6ff; margin:0; font-size: 14px; font-weight: bold;">{padrao_msg}</p>
                        <p style="color: #8b949e; margin:0; font-size: 12px;">🕒 ENTRADA ÀS: {horario_entrada}</p>
                    </div>
                </div>
                <h1 style="color: {cor}; font-size: 55px; margin: 15px 0;">{tipo_sinal}</h1>
                <hr style="border: 0.1px solid #30363d; margin: 20px 0;">
                <h3 style="color: white;">💰 PREÇO DE ENTRADA: {preco}</h3>
                <div style="display: flex; gap: 40px; margin: 25px 0;">
                    <div>
                        <p style="color: #8b949e; margin:0;">ALVO (TP)</p>
                        <h2 style="color: #00ff00; margin:0;">🎯 {dados_robo.get('TP', '0.00')}</h2>
                    </div>
                    <div>
                        <p style="color: #8b949e; margin:0;">PROTEÇÃO (SL)</p>
                        <h2 style="color: #ff4b4b; margin:0;">🛑 {dados_robo.get('SL', '0.00')}</h2>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="metric-card" style="border-top: 3px solid #58a6ff;">
                        <p style="color: #8b949e; font-size: 14px; margin:0;">RELAÇÃO RISCO:RETORNO</p>
                        <h2 style="color: #58a6ff; margin:0;">{rr_dinamico}</h2>
                    </div>
                    <div class="metric-card" style="border-top: 3px solid #ffffff;">
                        <p style="color: #8b949e; font-size: 14px; margin:0;">PROBABILIDADE DE SUCESSO</p>
                        <h2 style="color: white; margin:0;">{dados_robo.get('Prob', '---')}</h2>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aguardando robô...")

with tab_calculadora:
    st.subheader("📊 GESTÃO DE RISCO VEXI")
   
    lista_ativos = ["BTCUSDm", "XAUUSDm", "USOILm", "TSLAm", "US500m", "USTECm"]
    ativo_atual = dados_robo.get('Ativo', 'BTCUSDm')
   
    if ativo_atual not in lista_ativos:
        index_padrao = 0
    else:
        index_padrao = lista_ativos.index(ativo_atual)

    col_calc1, col_calc2 = st.columns(2)
    with col_calc1:
        st.markdown("### 📱 Cálculos")
        banca = st.number_input("Saldo da Conta (USD):", min_value=0.0, value=1000.0, step=100.0)
        risco_per = st.slider("Risco por trilha (%):", 0.1, 10.0, 1.0, 0.1)
        st.divider()
       
        tipo_mercado = st.selectbox("Tipo de Ativo:", lista_ativos, index=index_padrao)
       
        preco_ent = st.number_input("Preço de Entrada:", value=float(dados_robo.get('Preco', 0)), format="%.5f")
        preco_sl = st.number_input("Preço do Stop Loss:", value=float(dados_robo.get('SL', 0)), format="%.5f")

    with col_calc2:
        st.markdown(f"### 🎯 Resultado para {tipo_mercado}")
        distancia_sl = abs(preco_ent - preco_sl)
        valor_risco = banca * (risco_per / 100)
       
        if distancia_sl > 0:
            # CORREÇÃO: Mapeamento de Tamanho de Contrato Exness
            contratos = {
                "BTCUSDm": 1,
                "XAUUSDm": 100,    
                "USOILm": 1000,    
                "TSLAm": 100,      
                "US500m": 1,      
                "USTECm": 1,  
            }
           
            tamanho_contract = contratos.get(tipo_mercado, 1)
           
            # FÓRMULA CORRIGIDA: Lote = Risco Financeiro / (Distância do Stop * Tamanho do Contrato)
            lote_sugerido = valor_risco / (distancia_sl * taxation_contract if 'taxation_contract' in locals() else distancia_sl * tamanho_contract)
           
            st.markdown(f"""
            <div class="metric-card" style="border-top: 3px solid #00ff00; margin-bottom: 20px;">
                <p style="color: #8b949e; font-size: 14px; margin:0;">VALOR EM RISCO</p>
                <h2 style="color: #ff4b4b; margin:0;">$ {valor_risco:.2f}</h2>
            </div>
            <div class="metric-card" style="border-top: 3px solid #58a6ff;">
                <p style="color: #8b949e; font-size: 14px; margin:0;">VOLUME (LOTES)</p>
                <h1 style="color: #58a6ff; margin:0; font-size: 45px;">{max(lote_sugerido, 0.01):.2f}</h1>
                <p style="color: #8b949e; font-size: 12px;">Base Exness: 1 lote de {tipo_mercado} = {tamanho_contract} unidades</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Aguardando definição de preços...")

with tab_historico:
    st.subheader("📜 ÚLTIMAS OPERAÇÕES VEXI")
    if dados_h:
        try:
            df_hist = pd.DataFrame(dados_h)
            cols_visiveis = [c for c in df_hist.columns if c not in ['range', 'ema5', 'ema20', 'macd', 'signal_line']]
            st.dataframe(df_hist[cols_visiveis], use_container_width=True, hide_index=True)
        except:
            st.write("Atualizando...")

with tab_graficos:
    c1, c2 = st.columns(2)
    with c1: components.iframe("https://s.tradingview.com/widgetembed/?symbol=BINANCE%3ABTCUSDT&theme=dark", height=450)
    with c2: components.iframe("https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&theme=dark", height=450)
    c3, c4 = st.columns(2)
    with c3: components.iframe("https://s.tradingview.com/widgetembed/?symbol=TVC%3AUSOIL&theme=dark", height=450)
    with c4: components.iframe("https://s.tradingview.com/widgetembed/?symbol=NASDAQ%3ATSLA&theme=dark", height=450)
    c5, c6 = st.columns(2)
    with c5: components.iframe("https://s.tradingview.com/widgetembed/?symbol=OANDA%3ASPX500USD&theme=dark", height=450)
    with c6: components.iframe("https://s.tradingview.com/widgetembed/?symbol=NASDAQ%3ANDX&theme=dark", height=450)

with tab_mapa:
    components.iframe("https://www.coinglass.com/pro/futures/LiquidationHeatMap", height=700, scrolling=True)

with tab_noticias:
    st.subheader("🗓️ CALENDÁRIO ECONÔMICO E NOTÍCIAS")
    col_n1, col_n2 = st.columns([2.2, 1])
    with col_n1:
        components.html("""
            <div style="background-color: #0d1117; height: 100%;">
            <iframe src="https://sslecal2.investing.com?importance=1,2,3&features=datepicker,timezone&countries=5,25,32,6,37,72,22,17,39,14,10,35,43,56,36,110,11,26,12,4,8&calType=day&timeZone=12&lang=12"
            width="100%" height="700" frameborder="0" allowtransparency="true"></iframe>
            </div>
        """, height=700)
    with col_n2:
        components.html("""
            <iframe src="https://www.tradingview-widget.com/embed-widget/timeline/?colorTheme=dark&width=100%25&height=700&locale=br"
            width="100%" height="700" frameborder="0" allowtransparency="true"></iframe>
        """, height=700)

time.sleep(5)
st.rerun()