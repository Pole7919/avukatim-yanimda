import streamlit as st
import google.generativeai as genai

# SAYFA AYARLARI
st.set_page_config(page_title="Avukatım Yanımda", page_icon="⚖️", layout="centered")

# YÜKSEK KONTRASTLI TASARIM (BEYAZ ARKA PLAN - SİYAH YAZI)
st.markdown("""
    <style>
    /* Arka planı zorla beyaz yap */
    .stApp { background-color: white !important; }
    
    /* Tüm yazıları zorla siyah/koyu yap */
    h1, h2, h3, p, span, div, label, li { color: #000000 !important; font-family: 'Arial', sans-serif; }
    
    /* Butonları belirgin yap (Lacivert üzerine Beyaz yazı) */
    .stButton>button { 
        background-color: #004080 !important; 
        color: white !important; 
        border-radius: 10px !important; 
        font-weight: bold !important;
        height: 3.5em !important;
    }
    
    /* Form kutularını ve yazı alanlarını belirginleştir */
    .stTextArea textarea, .stTextInput input {
        background-color: #f8f9fa !important;
        color: black !important;
        border: 1px solid #004080 !important;
    }
    
    .header-box { text-align: center; padding: 10px; border-bottom: 2px solid #004080; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# ÜST BAŞLIK
st.markdown("<div class='header-box'><h1>⚖️ Avukatım Yanımda</h1><p><b>Mart 2026 Hukuki Analiz Sistemi</b></p></div>", unsafe_allow_html=True)

# API BAĞLANTISI (Model adı gemini-1.5-flash olarak güncellendi)
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # En güncel ve uyumlu model adı
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Bağlantı Ayarı Hatası: {str(e)}")
else:
    st.warning("⚠️ Lütfen 'Manage App -> Settings -> Secrets' kısmına API anahtarını ekleyin.")

# ADIM YÖNETİMİ
if 'step' not in st.session_state: st.session_state.step = 0
if 'answers' not in st.session_state: st.session_state.answers = {}

# SOHBET AKIŞI
if st.session_state.step == 0:
    st.markdown("### 👋 Merhaba! Ben hukuki asistanınım.")
    st.write("Seninle karşılıklı konuşarak durumunu analiz edeceğim. Başlamaya hazır mısın?")
    if st.button("Hadi Başlayalım! 🚀"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    st.markdown("### 🔍 Durumun Nedir?")
    sorun = st.text_area("İş yerinde yaşadığın sorunu buraya detaylıca yazabilirsin:", 
                         placeholder="Örn: 3 aydır maaşım ödenmiyor ve patronum beni işten çıkarmakla tehdit ediyor...", height=200)
    if st.button("Hukuki Analizimi Yap 🔍"):
        if sorun:
            st.session_state.answers['sorun'] = sorun
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Analiz yapabilmem için bir şeyler yazmalısın.")

elif st.session_state.step == 2:
    st.markdown("### 📋 Hukuki Analiziniz")
    try:
        with st.spinner('Analiz ediliyor, lütfen bekle...'):
            prompt = f"""
            Sen uzman bir Türk İş Hukuku asistanısın. Mart 2026 tarihindeyiz. 
            Kullanıcı sorunu: {st.session_state.answers['sorun']}. 
            Bu sorunu 4857 Sayılı İş Kanunu kapsamında değerlendir. 
            Vatandaşa haklarını (özellikle Madde 24/II) empatik bir dille anlat. 
            Sonunda mutlaka 'Bu bilgiler bilgilendirme amaçlıdır, bir avukata danışmalısınız' uyarısını yap.
            """
            response = model.generate_content(prompt)
            st.markdown(f"<div style='background-color: #f1f8ff; padding: 20px; border-radius: 10px; border: 1px solid #004080; color: black;'>{response.text}</div>", unsafe_allow_html=True)
            
            st.write("---")
            st.markdown("### 📄 İhtarname Taslağınız")
            st.write("Noter aracılığıyla gönderebileceğin taslak metin:")
            taslak = f"İHTARNAMEDİR\n\n4857 Sayılı Kanun Madde 24 uyarınca; {st.session_state.answers['sorun']} nedeniyle iş sözleşmemi haklı nedenle feshediyorum. Kıdem tazminatımın ve diğer işçilik alacaklarımın 3 iş günü içinde ödenmesini talep ederim."
            st.text_area("Kopyala ve Notere Götür:", taslak, height=150)
            
    except Exception as e:
        st.error(f"Hata detayı: {str(e)}")
        st.info("Eğer 'Model Not Found' diyorsa, Gemini modelleri güncellenmiş olabilir. Lütfen asistanına bildir.")
    
    if st.button("🔄 Yeniden Başla"):
        st.session_state.clear()
        st.rerun()

st.write("---")
st.caption("© 2026 Avukatım Yanımda - Türkiye İş Hukuku Bilgi Sistemi")
