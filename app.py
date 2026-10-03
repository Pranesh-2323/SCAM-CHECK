import os, json
import streamlit as st
import streamlit.components.v1 as components
from rules import analyse, mask

st.set_page_config(page_title="Scam Check", page_icon="🛡️")

LANGS = {"English": "en-IN", "தமிழ்": "ta-IN", "हिन्दी": "hi-IN"}
LLM_NAME = {"en-IN": "English", "ta-IN": "Tamil", "hi-IN": "Hindi"}

UI = {
 "en-IN": dict(title="🛡️ Scam Check", sub="Paste a suspicious investment message. We'll point out warning signs. Nothing is stored.",
   box="Paste the message here", btn="Check message", shot="Or upload a screenshot", flags="Warning signs found",
   none="No obvious warning signs found. This does NOT mean it is safe - always verify.",
   next="What to do next", unsure="We can be wrong. Treat this as a warning aid, not a final verdict.",
   steps=["Do not send money or share OTP/PIN/Aadhaar.", "Check if the person/firm is registered on the official SEBI website (sebi.gov.in).",
          "Report fraud: cybercrime.gov.in or call 1930. Investor complaints: SEBI SCORES portal.", "Talk to a family member before deciding."],
   lvl=dict(high="🔴 HIGH risk", medium="🟠 MEDIUM risk", low="🟡 LOW risk", none="⚪ No clear red flags"),
   f=dict(guaranteed="Promises guaranteed or very high returns. Real investments always carry risk.",
          urgency="Pushes you to act quickly. Scammers create pressure so you don't think.",
          group="Invites you to a private 'VIP' or tips group on WhatsApp/Telegram.",
          payment="Asks for money to a personal UPI ID/account or a 'fee'.",
          authority="Claims to be SEBI/RBI approved. Verify it yourself on the official website.",
          tips="Uses 'sure shot' / 'insider' / 'target' style tip language.",
          app="Pushes an unknown app or shortened link.",
          otp="Asks for OTP, Aadhaar, PAN or card details. Never share these.",
          crypto="Mentions crypto/forex, a common scam theme.")),
 "ta-IN": dict(title="🛡️ மோசடி சோதனை", sub="சந்தேகமான முதலீட்டு செய்தியை ஒட்டவும். எச்சரிக்கை அறிகுறிகளைக் காட்டுவோம். எதுவும் சேமிக்கப்படாது.",
   box="செய்தியை இங்கே ஒட்டவும்", btn="சோதிக்கவும்", shot="அல்லது ஸ்கிரீன்ஷாட் பதிவேற்றவும்", flags="கண்டறியப்பட்ட எச்சரிக்கை அறிகுறிகள்",
   none="தெளிவான எச்சரிக்கை அறிகுறிகள் இல்லை. ஆனால் இது பாதுகாப்பானது என்று அர்த்தமல்ல - எப்போதும் சரிபார்க்கவும்.",
   next="அடுத்து என்ன செய்வது", unsure="நாங்கள் தவறாகவும் இருக்கலாம். இது ஒரு எச்சரிக்கை உதவி மட்டுமே.",
   steps=["பணம் அனுப்ப வேண்டாம்; OTP/PIN/ஆதார் பகிர வேண்டாம்.", "அந்த நபர்/நிறுவனம் SEBI இணையதளத்தில் (sebi.gov.in) பதிவு செய்யப்பட்டுள்ளதா எனப் பாருங்கள்.",
          "மோசடியைப் புகாரளிக்க: cybercrime.gov.in அல்லது 1930. முதலீட்டாளர் புகார்: SEBI SCORES.", "முடிவெடுக்கும் முன் குடும்பத்தினருடன் பேசுங்கள்."],
   lvl=dict(high="🔴 அதிக ஆபத்து", medium="🟠 நடுத்தர ஆபத்து", low="🟡 குறைந்த ஆபத்து", none="⚪ தெளிவான எச்சரிக்கை இல்லை"),
   f=dict(guaranteed="உத்தரவாத அல்லது மிக அதிக லாபம் என்கிறது. உண்மையான முதலீட்டில் எப்போதும் ஆபத்து உண்டு.",
          urgency="அவசரப்படுத்துகிறது. யோசிக்க விடாமல் இருக்க மோசடிக்காரர்கள் இப்படிச் செய்வார்கள்.",
          group="WhatsApp/Telegram 'VIP' குழுவில் சேர அழைக்கிறது.",
          payment="தனிப்பட்ட UPI/கணக்குக்கு அல்லது 'கட்டணம்' என்று பணம் கேட்கிறது.",
          authority="SEBI/RBI அனுமதி என்று கூறுகிறது. அதிகாரப்பூர்வ தளத்தில் நீங்களே சரிபாருங்கள்.",
          tips="'sure shot' / 'insider' / 'target' போன்ற டிப்ஸ் மொழி உள்ளது.",
          app="தெரியாத ஆப் அல்லது சுருக்கிய இணைப்பைத் தள்ளுகிறது.",
          otp="OTP, ஆதார், PAN அல்லது கார்டு விவரம் கேட்கிறது. ஒருபோதும் பகிர வேண்டாம்.",
          crypto="Crypto/forex பற்றிப் பேசுகிறது - இது பொதுவான மோசடி தலைப்பு.")),
 "hi-IN": dict(title="🛡️ स्कैम चेक", sub="संदिग्ध निवेश संदेश यहाँ पेस्ट करें। हम चेतावनी के संकेत बताएँगे। कुछ भी सेव नहीं होता।",
   box="संदेश यहाँ पेस्ट करें", btn="जाँचें", shot="या स्क्रीनशॉट अपलोड करें", flags="मिले चेतावनी संकेत",
   none="कोई स्पष्ट चेतावनी नहीं मिली। इसका मतलब सुरक्षित होना नहीं है - हमेशा खुद जाँचें।",
   next="आगे क्या करें", unsure="हम गलत भी हो सकते हैं। यह सिर्फ़ चेतावनी में मदद है।",
   steps=["पैसे न भेजें; OTP/PIN/आधार साझा न करें।", "देखें कि व्यक्ति/कंपनी SEBI की वेबसाइट (sebi.gov.in) पर पंजीकृत है या नहीं।",
          "धोखाधड़ी की शिकायत: cybercrime.gov.in या 1930। निवेशक शिकायत: SEBI SCORES।", "फ़ैसले से पहले परिवार से बात करें।"],
   lvl=dict(high="🔴 ज़्यादा जोखिम", medium="🟠 मध्यम जोखिम", low="🟡 कम जोखिम", none="⚪ कोई स्पष्ट संकेत नहीं"),
   f=dict(guaranteed="गारंटीड या बहुत ज़्यादा रिटर्न का वादा। असली निवेश में हमेशा जोखिम होता है।",
          urgency="जल्दबाज़ी करवा रहा है। ठग सोचने का समय नहीं देते।",
          group="WhatsApp/Telegram के 'VIP' ग्रुप में बुला रहा है।",
          payment="निजी UPI/खाते में या 'फ़ीस' के नाम पर पैसे माँग रहा है।",
          authority="SEBI/RBI मान्यता का दावा। आधिकारिक वेबसाइट पर खुद जाँचें।",
          tips="'sure shot' / 'insider' / 'target' जैसी टिप वाली भाषा।",
          app="अनजान ऐप या छोटा लिंक भेज रहा है।",
          otp="OTP, आधार, PAN या कार्ड की जानकारी माँग रहा है। कभी साझा न करें।",
          crypto="क्रिप्टो/फ़ॉरेक्स का ज़िक्र - आम स्कैम थीम।")),
}

def llm_explain(text, flags, lang):
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key or not flags:
        return None
    try:
        import anthropic
        r = anthropic.Anthropic(api_key=key).messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=350,
            messages=[{"role": "user", "content":
              f"In simple {LLM_NAME[lang]}, in 3 short sentences, explain why this message may be an investment scam. "
              f"Detected flags: {flags}. Say you are not certain. NEVER give investment advice, stock tips or predictions.\n\nMessage:\n{text}"}])
        return r.content[0].text
    except Exception:
        return None

def ocr(file):
    try:
        import pytesseract
        from PIL import Image
        return pytesseract.image_to_string(Image.open(file), lang="eng+tam+hin")
    except Exception:
        return ""

def speak_button(text, lang):
    components.html(f"""<button style="padding:8px 14px;font-size:16px" onclick="speechSynthesis.cancel();
      var u=new SpeechSynthesisUtterance({json.dumps(text)});u.lang='{lang}';speechSynthesis.speak(u)">🔊 Listen</button>""", height=50)

def mic_widget(lang):
    components.html(f"""<button id=b style="padding:8px 14px;font-size:16px">🎤 Speak</button>
      <textarea id=t rows=3 style="width:100%;margin-top:6px" placeholder="Transcript - copy it into the box above"></textarea>
      <script>const R=window.SpeechRecognition||window.webkitSpeechRecognition;
      document.getElementById('b').onclick=()=>{{if(!R){{alert('Use Chrome for voice input');return}}
      const r=new R();r.lang='{lang}';r.onresult=e=>document.getElementById('t').value=e.results[0][0].transcript;r.start()}}</script>""", height=150)

lang_name = st.radio("Language / மொழி / भाषा", list(LANGS), horizontal=True)
lang = LANGS[lang_name]; T = UI[lang]

st.title(T["title"]); st.caption(T["sub"])
text = st.text_area(T["box"], height=160)
with st.expander("🎤"):
    mic_widget(lang)
img = st.file_uploader(T["shot"], type=["png", "jpg", "jpeg"])

if st.button(T["btn"], type="primary"):
    if img:
        text = (text + "\n" + ocr(img)).strip()
    if not text.strip():
        st.warning("..."); st.stop()
    level, score, flags = analyse(text)
    st.subheader(T["lvl"][level])
    summary = [T["lvl"][level]]
    if flags:
        st.markdown(f"**{T['flags']}**")
        for f in flags:
            st.markdown(f"- {T['f'][f]}"); summary.append(T["f"][f])
        extra = llm_explain(mask(text), flags, lang)   # masked text only
        if extra:
            st.info(extra); summary.append(extra)
    else:
        st.write(T["none"]); summary.append(T["none"])
    st.markdown(f"**{T['next']}**")
    for s in T["steps"]:
        st.markdown(f"- {s}")
    st.caption(T["unsure"])
    summary += T["steps"]
    speak_button(" ".join(summary), lang)
