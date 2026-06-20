import streamlit as st
import pandas as pd
from google import genai
import os
from dotenv import load_dotenv

# .env file load
load_dotenv()


gemini_key = os.getenv("GEMINI_API_KEY")

if not gemini_key:
    st.error("ERROR IN FINDING API KEY in .env")
    st.stop()

client = genai.Client(api_key=gemini_key)

st.title("📊 TalkToData: AI Data Visualizer")
st.write("#### Build free AI charts or graphs by giving your csv files.")

uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.xlsx'):
        my_file = pd.read_excel(uploaded_file)
    else:
        my_file = pd.read_csv(uploaded_file)
        
    st.write("### Data Preview:", my_file.head())
    
    user_prompt = st.text_input("Prompt here that what type of chart do you want on which parameter?")
    
    if st.button("Generate Visualization ✨") and user_prompt:
        system_instruction = """
        You are an expert data analyst. Generate ONLY valid Python code using matplotlib or seaborn to visualize the data.
        The dataframe is already loaded as 'my_file'. 
        Do not include any explanation, markdown, or code block markers (like ```python). 
        Just return the raw python code that creates the plot and ends with st.pyplot().
        """
        
        full_prompt = f"{system_instruction}\n\nData columns are: {list(my_file.columns)}. User wants: {user_prompt}"
        
        with st.spinner("AI is thinking.... 🧠"):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt,
                )
                
                #(clean raw code)
                generated_code = response.text.replace("```python", "").replace("```", "").strip()
                
                st.write("### Generated Code:")
                st.code(generated_code, language="python")
                
                st.write("### Result:")
                exec(generated_code, globals(), locals())
                
            except Exception as e:
                st.error(f"Error!!!: {e}")