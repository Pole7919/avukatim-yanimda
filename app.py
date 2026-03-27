import streamlit as st
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# 2026 GÜNCEL VERİLER (Mart 2026)
ASGARI_UCRET = 42000.00  # 2026 Tahmini rakam
KIDEM_TAVANI = 85000.00  # 2026 Tahmini rakam

# SAYFA AYARLARI
st.set_page_config(page_title="Avukatım Yanımda", page_icon="⚖️", layout="centered")

# AÇIK MAVİ & BEYAZ TEMA (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #F0F8FF; }
    .main-title { color: #0056b3; text-align: center; font-family: 'Arial'; font-weight: bold; }
    .stButton>button { background-color: #0056b3; color: white; border-radius: 20px; width: 100%; border: none; height: 3em; font-weight: bold; }
    .stButton>button:hover { background-color: #004494; color: white; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_config=True)

# ÜST BAŞLIK VE SEO
st.markdown("<h1 class='main-title'>⚖️ Avukatım Yanımda</h1>", unsafe_allow_config=True)
st.markdown("<p style='text-align: center; color: #555;'>Mart 2026 Güncel İş Hukuku Asistanı</p>", unsafe_allow_config=True)
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

# SOKRATİK SORU-CEVAP AKIŞI
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
    sorun = st.text_area("Seni en çok zorlayan sorun nedir? (İstifa etmeyi mi düşünüyorsun, kovuldun mu, mobbing mi var?)")
    if st.button("Analizi Tamamla 🔍"):
        st.session_state.answers['sorun'] = sorun
        st.session_state.step = 5
        st.rerun()

elif st.session_state.step == 5:
    st.markdown("### 📋 Hukuki Analiziniz")
    
    # AI ANALİZİ (GEMINI)
    prompt = f"""
    Sen uzman bir Türk İş Hukuku asistanısın. Mart 2026 tarihindeyiz. 
    Kullanıcı verileri: {st.session_state.answers}.
    Bu verilere göre:
    1. Empatik bir giriş yap.
    2. 4857 Sayılı İş Kanunu'na göre haklarını açıkla (Özellikle Madde 24/II vurgusu yap).
    3. Kullanıcıya 'İstifa' yerine 'Haklı Fesih' yapması gerekip gerekmediğini söyle.
    4. Delil toplaması için (WhatsApp, bordro vb.) somut öneriler ver.
    5. Sokratik bir soru sor: 'Dava süresince 6 ay idare edebilir misin?'
    6. Sonunda mutlaka bir avukata danışması gerektiğini belirt.
    Cevabı halkın anlayacağı açık bir dille yaz.
    """
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        st.write(response.text)
        
        # İHTARNAME OLUŞTURMA (TASLAK)
        st.write("---")
        st.subheader("📄 İhtarname Taslağı")
        ihtar_metni = f"4857 Sayılı İş Kanunu Madde 24 uyarınca; {st.session_state.answers['sorun']} nedeniyle iş sözleşmemi haklı nedenle feshediyorum. Kıdem tazminatımın ve alacaklarımın ödenmesini talep ederim."
        st.text_area("Taslak Metin (Kopyalayabilirsin):", ihtar_metni, height=150)
        
    except Exception as e:
        st.error("AI şu an yoğun, ancak 4857 Sayılı Kanun 24. Madde uyarınca hakların korunmaktadır.")

    if st.button("Baştan Başla 🔄"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.write("---")
st.caption("© 2026 Avukatım Yanımda - Bu bir yapay zeka asistanıdır. Kesin karar vermeden önce mutlaka bir AVUKAT ile görüşünüz.")
