import streamlit as st
import google.generativeai as genai

# SAYFA AYARLARI
st.set_page_config(page_title="Avukatım Yanımda", page_icon="⚖️", layout="centered")

# GÖRÜNÜRLÜK DÜZELTMESİ (Koyu Yazılar, Net Tasarım)
st.markdown("""
    <style>
    /* Arka planı bembeyaz yap */
    .stApp { background-color: #FFFFFF; }
    
    /* Tüm yazıları koyu lacivert yap ki okunsun */
    h1, h2, h3, p, span, div, label { color: #003366 !important; font-family: 'Arial'; }
    
    /* Buton tasarımı */
    .stButton>button { 
        background-color: #0056b3; 
        color: white !important; 
        border-radius: 10px; 
        width: 100%; 
        border: none; 
        height: 3.5em; 
        font-weight: bold; 
        font-size: 1.1em;
    }
    
    /* Bilgi kutusu rengi */
    .stAlert { background-color: #E8F4F8; border: 1px solid #BEE5EB; }
    </style>
    """, unsafe_allow_html=True)

# ÜST BAŞLIK
st.markdown("<h1 style='text-align: center;'>⚖️ Avukatım Yanımda</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Mart 2026 Güncel İş Hukuku Asistanı</b></p>", unsafe_allow_html=True)
st.write("---")

# API ANAHTARI KONTROLÜ
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.warning("⚠️ AI Beyni (API Key) bağlı değil. Lütfen ayarlardan ekleyin.")

# OTURUM YÖNETİMİ
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# SOHBET AKIŞI
if st.session_state.step == 0:
    st.info("👋 Merhaba! Ben senin hukuki asistanınım. Haklarını öğrenmek için birkaç soruma yanıt verir misin? Tamamen anonimiz.")
    if st.button("Başlayalım 🚀"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    st.markdown("### 1. Çalışma Süren")
    st.write("Bu iş yerinde ne kadar süredir çalışıyorsun?")
    sure = st.radio("", ["1 yıldan az", "1 yıldan fazla"], key="sure_radio", label_visibility="collapsed")
    if st.button("Devam Et ➡️"):
        st.session_state.answers['sure'] = sure
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.markdown("### 2. Maaş Ödeme Şekli")
    st.write("Maaşın bankaya tam olarak yatıyor mu?")
    maas = st.radio("", ["Evet, hepsi bankaya", "Hayır, bir kısmı elden", "Tamamı elden"], key="maas_radio", label_visibility="collapsed")
    if st.button("Devam Et ➡️"):
        st.session_state.answers['maas'] = maas
        st.session_state.step = 3
        st.rerun()

elif st.session_state.step == 3:
    st.markdown("### 3. Sigorta Durumu")
    st.write("Sigortan gerçek maaşın üzerinden mi yatıyor?")
    sigorta = st.radio("", ["Evet, gerçek maaşım", "Hayır, asgari ücretten gösteriliyor", "Hiç sigortam yok"], key="sigorta_radio", label_visibility="collapsed")
    if st.button("Devam Et ➡️"):
        st.session_state.answers['sigorta'] = sigorta
        st.session_state.step = 4
        st.rerun()

elif st.session_state.step == 4:
    st.markdown("### 4. Temel Sorun")
    st.write("Seni en çok zorlayan sorun nedir?")
    sorun = st.text_area("", placeholder="Örn: Maaşım 2 aydır ödenmiyor...")
    if st.button("Analizi Tamamla 🔍"):
        st.session_state.answers['sorun'] = sorun
        st.session_state.step = 5
        st.rerun()

elif st.session_state.step == 5:
    st.markdown("### 📋 Hukuki Analiziniz")
    with st.spinner('AI Analiz Ediyor...'):
        try:
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"Sen uzman bir Türk İş Hukuku asistanısın. Kullanıcı verileri: {st.session_state.answers}. Empatik bir dille haklarını açıkla, Madde 24/II vurgusu yap ve sonunda avukata yönlendir."
            response = model.generate_content(prompt)
            st.markdown(f"<div style='background-color: #F8F9FA; padding: 15px; border-radius: 10px; border-left: 5px solid #0056b3; color: #333;'>{response.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error("AI şu an cevap veremiyor. API Anahtarını kontrol et.")

    if st.button("🔄 Yeniden Başla"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.write("---")
st.caption("© 2026 Avukatım Yanımda - Sadece bilgilendirme amaçlıdır.")
