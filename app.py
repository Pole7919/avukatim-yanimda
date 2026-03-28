import streamlit as st
import google.generativeai as genai

# SAYFA AYARLARI
st.set_page_config(page_title="Avukatım Yanımda", page_icon="⚖️")

# YÜKSEK OKUNURLUK TASARIMI (BEYAZ ÜSTÜNE SİYAH)
st.markdown("""
    <style>
    .stApp { background-color: white !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, div { color: black !important; font-family: 'Arial' !important; }
    .stButton>button { 
        background-color: #000000 !important; 
        color: white !important; 
        border-radius: 5px !important;
        font-weight: bold !important;
        width: 100% !important;
        height: 3em !important;
    }
    .stTextArea textarea { background-color: #f0f2f6 !important; color: black !important; border: 2px solid black !important; }
    .result-box { background-color: #ffffff !important; padding: 20px; border: 3px solid black; border-radius: 10px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# ÜST BAŞLIK
st.markdown("<h1 style='text-align: center;'>⚖️ AVUKATIM YANIMDA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; border-bottom: 2px solid black; padding-bottom: 10px;'>Mart 2026 İş Hukuku Analiz Sistemi</p>", unsafe_allow_html=True)

# API ANAHTARI BAĞLANTISI
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ API Anahtarı eksik! Lütfen Secrets kısmına ekle.")

# SORU ALANI
st.markdown("### Sorununuz Nedir?")
sorun = st.text_area("", placeholder="Örn: 2 aydır maaşım ödenmiyor, ne yapmalıyım?", height=150)

if st.button("HUKUKİ ANALİZİ BAŞLAT"):
    if sorun:
        with st.spinner('Analiz yapılıyor...'):
            # AKILLI MODEL SEÇİCİ (Hata almamak için 3 farklı modeli deniyoruz)
            success = False
            for model_name in ["gemini-1.5-flash", "gemini-pro", "gemini-1.5-pro"]:
                if success: break
                try:
                    model = genai.GenerativeModel(model_name)
                    prompt = f"Sen uzman bir Türk İş Hukuku asistanısın. Kullanıcı sorunu: {sorun}. 4857 Sayılı Kanun Madde 24 üzerinden analiz yap. Empatik ol ve avukat tavsiyesi ver."
                    response = model.generate_content(prompt)
                    
                    st.markdown("### 📋 SONUÇ VE ANALİZ")
                    st.markdown(f"<div class='result-box'>{response.text}</div>", unsafe_allow_html=True)
                    
                    st.write("---")
                    st.markdown("### 📄 İHTARNAME TASLAĞI")
                    taslak = f"İHTARNAMEDİR\n\n4857 Sayılı İş Kanunu Madde 24 uyarınca; {sorun} sebebiyle sözleşmemi haklı nedenle feshediyorum. Tüm alacaklarımın 3 gün içinde ödenmesini talep ederim."
                    st.text_area("Noter İçin Taslak:", taslak, height=120)
                    success = True
                except Exception as e:
                    continue # Bu model çalışmadıysa bir sonrakini dene
            
            if not success:
                st.error("Google sistemleri şu an yanıt vermiyor. Lütfen 1 dakika sonra tekrar dene.")
    else:
        st.warning("Lütfen bir sorun yazın.")

st.write("---")
st.caption("© 2026 Avukatım Yanımda - Bilgilendirme amaçlıdır. Mutlaka bir avukata danışın.")
