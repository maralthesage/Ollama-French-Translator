import streamlit as st
import pandas as pd
import ollama
from io import BytesIO

st.set_page_config(page_title="German to French Translator", layout="centered")
st.title("🇩🇪➡️🇫🇷 German to French Translator")

# Function to call Ollama for translation
def translate_text_ollama(text):
    prompt = f"Übersetze folgenden deutschen Text ins Französische.\nGib ausschließlich die französische Übersetzung zurück – kein Zusatz, kein Kommentar, keine Anführungszeichen.\n\n{text}"
    response = ollama.chat(model='mistral-small3.1:latest', messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content'].strip()

# Option to either upload Excel or input text
option = st.radio("Was möchten Sie tun?", ["Excel-Datei hochladen", "Deutschen Text eingeben"])

if option == "Excel-Datei hochladen":
    uploaded_file = st.file_uploader("Excel-Datei hochladen", type=["xlsx", "xls"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.write("Vorschau der Tabelle:")
        st.dataframe(df)

        columns = df.columns.tolist()
        column_to_translate = st.selectbox("Wählen Sie die Spalte mit deutschem Text", columns)

        from io import BytesIO

    if st.button("Übersetzen"):
        with st.spinner("Übersetze..."):
            df["French Translation"] = df[column_to_translate].astype(str).apply(translate_text_ollama)
            st.success("Übersetzung abgeschlossen!")
            st.dataframe(df)

            # Create Excel file in memory
            output = BytesIO()
            df.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            # Provide download button
            st.download_button(
                label="📥 Übersetzte Datei herunterladen",
                data=output,
                file_name="translated.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


else:
    input_text = st.text_area("Deutschen Text eingeben", height=200, placeholder="Geben Sie einen Absatz auf Deutsch ein...")
    if st.button("Absatz übersetzen"):
        if input_text.strip():
            with st.spinner("Übersetze..."):
                translation = translate_text_ollama(input_text)
                st.markdown("**Französische Übersetzung:**")
                st.success(translation)
        else:
            st.warning("Bitte geben Sie einen Text ein.")
