import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Avukatım Yanımda", page_icon="⚖️")

# TASARIM
st.markdown("<h1 style='text-align: center; color: #0056b3;'>⚖️ Avukatım Yanımda</h1>", unsafe_allow_html=True)
st.write("---")

# API KONTROLÜ VE HATA GÖSTERİMİ
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # 2026'da en güncel model 1.5-flash veya pro olacaktır
        model = genai.GenerativeModel('gemini-1.5-flash') 
    except Exception as e:
        st.error(f"Bağlantı Hatası: {str(e)}")
else:
    st.warning("⚠️ API Anahtarı hala 'Secrets' kısmında kayıtlı görünmüyor.")

# ANALİZ EKRANI
sorun = st.text_area("Yaşadığın sorunu buraya yaz:")
if st.button("Hukuki Analizi Al"):
    if sorun:
        try:
            with st.spinner('AI Düşünüyor...'):
                response = model.generate_content(f"Bir işçinin sorunu şu: {sorun}. Türk İş Kanunu'na göre analiz et.")
                st.success(response.text)
        except Exception as e:
            # BURASI HATANIN GERÇEK SEBEBİNİ SÖYLEYECEK
            st.error(f"Gerçek Hata Mesajı: {str(e)}") 
    else:
        st.warning("Lütfen bir sorun yazın.")
