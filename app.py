import streamlit as st
import google.generativeai as genai

# SAYFA AYARLARI
st.set_page_config(page_title="Avukatım Yanımda", page_icon="⚖️", layout="centered")

# TASARIM VE GÖRSEL DÜZENLEME (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    h1, h2, h3, p, span, div, label { color: #003366 !important; font-family: 'Arial'; }
    .stButton>button { 
        background-color: #0056b3; color: white !important; 
        border-radius: 12px; width: 100%; border: none; height: 3.5em; font-weight: bold; 
    }
    .header-logo { text-align: center; font-size: 50px; margin-bottom: 0px; }
    .header-text { text-align: center; margin-top: -10px; margin-bottom: 20px; }
    .analysis-box { background-color: #F8F9FA; padding: 20px; border-radius: 10px; border-left: 5px solid #0056b3; }
    </style>
    """, unsafe_allow_html=True)

# ÜST BAŞLIK (Logo ve Yazı Ayrı)
st.markdown("<div class='header-logo'>⚖️</div>", unsafe_allow_html=True)
st.markdown("<div class='header-text'><h1>Avukatım Yanımda</h1><p><b>Mart 2026 İş Hukuku Asistanı</b></p></div>", unsafe_allow_html=True)
st.write("---")

# API BAĞLANTISI (KESİN MODEL ADI: gemini-pro)
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # En uyumlu model adı
        model = genai.GenerativeModel('gemini-pro') 
    except Exception as e:
        st.error(f"Bağlantı Hatası: {str(e)}")
else:
    st.warning("⚠️ API Anahtarı bulunamadı. Lütfen Secrets kısmına ekleyin.")

# ADIM YÖNETİMİ
if 'step' not in st.session_state: st.session_state.step = 0
if 'answers' not in st.session_state: st.session_state.answers = {}

# SOHBET AKIŞI
if st.session_state.step == 0:
    st.info("👋 Merhaba! Ben senin hukuki asistanınım. Yanındayım. Haklarını öğrenmek için analizini başlatabilirsin.")
    if st.button("Başlayalım 🚀"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    st.markdown("### İş yerindeki temel sorunun nedir?")
    sorun = st.text_area("Lütfen yaşadığın durumu kısaca anlat:", placeholder="Örn: 2 aydır maaşım ödenmiyor...")
    if st.button("Hukuki Analizi Al 🔍"):
        if sorun:
            st.session_state.answers['sorun'] = sorun
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Lütfen bir sorun yazın.")

elif st.session_state.step == 2:
    st.markdown("### 📋 Hukuki Analiziniz")
    try:
        with st.spinner('AI Yanıt Hazırlıyor...'):
            # AI Yanıtı
            prompt = f"Sen uzman bir Türk İş Hukuku asistanısın. Kullanıcı sorunu: {st.session_state.answers['sorun']}. 4857 Sayılı Kanun Madde 24 üzerinden empatik, net ve koruyucu bir analiz yap. Sonunda mutlaka avukat tavsiyesi ver."
            response = model.generate_content(prompt)
            st.markdown(f"<div class='analysis-box'>{response.text}</div>", unsafe_allow_html=True)
            
            st.write("---")
            st.subheader("📄 İhtarname Taslağı")
            ihtar = f"4857 Sayılı Kanun Madde 24 uyarınca; {st.session_state.answers['sorun']} nedeniyle sözleşmemi feshediyorum. Tüm alacaklarımın tarafıma ödenmesini talep ederim."
            st.text_area("Kopyalayabileceğin Taslak:", ihtar, height=100)
            
    except Exception as e:
        st.error(f"Analiz sırasında bir hata oluştu: {str(e)}")
    
    if st.button("🔄 Yeniden Başla"):
        st.session_state.clear()
        st.rerun()

st.write("---")
st.caption("© 2026 Avukatım Yanımda - Sadece bilgilendirme amaçlıdır.")
