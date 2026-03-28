import streamlit as st
import google.generativeai as genai
import io

# 2026 GÜNCEL VERİLER (Mart 2026)
ASGARI_UCRET = 42000.00  
KIDEM_TAVANI = 85000.00  

# SAYFA AYARLARI
st.set_page_config(page_title="Avukatım Yanımda", page_icon="⚖️", layout="centered")

# AÇIK MAVİ & BEYAZ TEMA (CSS) - DÜZELTİLDİ
st.markdown("""
    <style>
    .stApp { background-color: #F0F8FF; }
    .main-title { color: #0056b3; text-align: center; font-family: 'Arial'; font-weight: bold; }
    .stButton>button { background-color: #0056b3; color: white; border-radius: 20px; width: 100%; border: none; height: 3em; font-weight: bold; }
    .stButton>button:hover { background-color: #004494; color: white; }
    </style>
    """, unsafe_allow_html=True)

# ÜST BAŞLIK
st.markdown("<h1 class='main-title'>⚖️ Avukatım Yanımda</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Mart 2026 Güncel İş Hukuku Asistanı</p>", unsafe_allow_html=True)
st.write("---")

# API ANAHTARI KONTROLÜ
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.warning("⚠️ AI Beyni (API Key) henüz bağlanmadı. Lütfen ayarlardan ekleyin.")

# OTURUM YÖNETİMİ
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# SOHBET AKIŞI
if st.session_state.step == 0:
    st.info("👋 Merhaba! Ben senin hukuki asistanınım. Yanındayım. Haklarını öğrenmek için birkaç soruma yanıt verir misin? Tamamen anonimiz.")
    if st.button("Başlayalım 🚀"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    st.subheader("1. Çalışma Süren")
    sure = st.radio("Bu iş yerinde ne kadar süredir çalışıyorsun?", ["1 yıldan az", "1 yıldan fazla"], index=None)
    if sure:
        st.session_state.answers['sure'] = sure
        if st.button("Devam Et ➡️"):
            st.session_state.step = 2
            st.rerun()

elif st.session_state.step == 2:
    st.subheader("2. Maaş Ödeme Şekli")
    maas = st.radio("Maaşın bankaya tam olarak yatıyor mu?", ["Evet, hepsi bankaya", "Hayır, bir kısmı elden", "Tamamı elden"], index=None)
    if maas:
        st.session_state.answers['maas'] = maas
        if st.button("Devam Et ➡️"):
            st.session_state.step = 3
            st.rerun()

elif st.session_state.step == 3:
    st.subheader("3. Sigorta Durumu")
    sigorta = st.radio("Sigortan gerçek maaşın üzerinden mi yatıyor?", ["Evet, gerçek maaşım", "Hayır, asgari ücretten gösteriliyor", "Hiç sigortam yok"], index=None)
    if sigorta:
        st.session_state.answers['sigorta'] = sigorta
        if st.button("Devam Et ➡️"):
            st.session_state.step = 4
            st.rerun()

elif st.session_state.step == 4:
    st.subheader("4. Temel Sorun")
    sorun = st.text_area("Seni en çok zorlayan sorun nedir?")
    if st.button("Analizi Tamamla 🔍"):
        st.session_state.answers['sorun'] = sorun
        st.session_state.step = 5
        st.rerun()

elif st.session_state.step == 5:
    st.markdown("### 📋 Hukuki Analiziniz")
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Sen uzman bir Türk İş Hukuku asistanısın. Kullanıcı verileri: {st.session_state.answers}. Empatik bir dille haklarını açıkla, Madde 24/II vurgusu yap, delil toplama önerisi ver ve sonunda avukata yönlendir."
        response = model.generate_content(prompt)
        st.write(response.text)
    except Exception as e:
        st.error("API Anahtarı hatalı veya eksik. Lütfen Streamlit ayarlarından kontrol et.")

    if st.button("Baştan Başla 🔄"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.write("---")
st.caption("© 2026 Avukatım Yanımda - Bilgilendirme amaçlıdır.")
