import streamlit as st
import requests

st.set_page_config(page_title="Financial Analyst Assistant", layout="wide")
st.title("📈 Financial Analyst Multi-Agent Assistant")

input_method = st.radio("Choose input method:", ["URL", "Paste Text"])

url_input = ""
text_input = ""

if input_method == "URL":
    url_input = st.text_input("Enter a financial news article URL:")
else:
    text_input = st.text_area("Paste article content here:")

if st.button("Analyze"):
    if (input_method == "URL" and not url_input) or (input_method == "Paste Text" and not text_input):
        st.warning("Please provide the input.")
    else:
        with st.spinner("Analyzing..."):
            try:
                payload = {"url": url_input} if input_method == "URL" else {"text": text_input}
                response = requests.post("http://127.0.0.1:8000/analyze", json=payload)
                result = response.json()

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.subheader("🔍 Source")
                    st.text(result["source"])

                    st.subheader("📃 Scraped/Input Text")
                    st.text(result["scraped_text"])

                    st.subheader("📝 Summary")
                    st.success(result["summary"])

                    st.subheader("📚 Context Documents")
                    for i, doc in enumerate(result["context_docs"]):
                        with st.expander(f"Context Document {i+1}"):
                            st.write(doc)

                    st.subheader("💡 Decision")
                    st.info(result["decision"])
            except Exception as e:
                st.error(f"Something went wrong: {e}")
