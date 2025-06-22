import streamlit as st
from googletrans import Translator
from gtts import gTTS
import io

st.set_page_config(
    page_title="Language Translation Tool",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title(" AI Language Translator")
st.markdown(
    """
    Welcome to your AI-powered language translation tool!
    Enter text below, select your source and target languages, and hit 'Translate'.
    You can also listen to the translated text.
    """
)

# Initialize the Translator object from googletrans
translator = Translator()

#  Language Options 
languages = {
    "Auto-Detect": "auto", # 'auto' for source language detection
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Japanese": "ja",
    "Chinese (Simplified)": "zh-CN",
    "Arabic": "ar",
    "Russian": "ru",
    "Portuguese": "pt",
    "Italian": "it",
    "Korean": "ko",
    "Dutch": "nl",
    "Turkish": "tr",
    "Vietnamese": "vi",
    "Thai": "th",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Punjabi": "pa",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
}

# UI for Language Selection and Text Input
st.subheader("Text Input and Language Selection")

col1, col2 = st.columns(2)

with col1:
    source_language_name = st.selectbox(
        "Select Source Language:",
        list(languages.keys()),
        index=0,  
        help="Choose the language of the text you are entering."
    )
    source_language_code = languages[source_language_name]

with col2:
    target_lang_options = list(languages.keys())[1:] # Exclude 'Auto-Detect'
    target_language_name = st.selectbox(
        "Select Target Language:",
        target_lang_options,
        index=target_lang_options.index("English"), # Default target to English
        help="Choose the language you want the text translated into."
    )
    target_language_code = languages[target_language_name]

# Text area for user input
text_to_translate = st.text_area(
    "Enter text to translate here:",
    height=200,
    placeholder="Type or paste your text here...",
    help="The text entered here will be translated."
)

# Translation Button
if st.button("Translate", help="Click to translate the entered text."):
    if text_to_translate:
        # Check if source and target languages are the same, and if source is not auto-detect
        if source_language_code != 'auto' and source_language_code == target_language_code:
            st.warning("Source and target languages are the same. No translation needed.")
            st.markdown(f"**Original Text (No Translation):** {text_to_translate}")
        else:
            try:
                with st.spinner("Translating..."):
                    # Perform translation using googletrans
                    translated = translator.translate(
                        text_to_translate,
                        src=source_language_code,
                        dest=target_language_code
                    )
                    translated_text = translated.text

                st.subheader("Translated Text")
                st.info(translated_text)

            
                st.markdown(
                    f"""
                    <button
                        onclick="navigator.clipboard.writeText('{translated_text.replace("'", "\\'")}')"
                        style="
                            background-color: #4CAF50; /* Green */
                            border: none;
                            color: white;
                            padding: 10px 20px;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 16px;
                            margin: 4px 2px;
                            cursor: pointer;
                            border-radius: 8px;
                            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                            transition: 0.3s;
                        "
                        onmouseover="this.style.backgroundColor='#45a049'"
                        onmouseout="this.style.backgroundColor='#4CAF50'"
                    >
                        Copy Translated Text
                    </button>
                    """,
                    unsafe_allow_html=True
                )


                st.subheader("Listen to Translation")
                try:
                    # Generate speech using gTTS
                    tts = gTTS(text=translated_text, lang=target_language_code, slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0) 

                    st.audio(fp, format="audio/mp3", start_time=0)
                except Exception as tts_e:
                    st.error(f"Could not generate audio for the translated text. This might be due to an unsupported language for text-to-speech: {tts_e}")

            except Exception as e:
                st.error(f"An error occurred during translation: {e}")
                st.info("Please ensure you have an active internet connection and that the 'googletrans' library is working correctly. Sometimes, 'googletrans' can have temporary issues due to Google's backend changes.")
    else:
        st.warning("Please enter some text to translate before clicking 'Translate'.")

st.markdown("---")
st.caption("Developed as part of the CodeAlpha AI Internship Task 1.")
st.caption("Translation powered by `googletrans` and Text-to-Speech by `gTTS`.")
