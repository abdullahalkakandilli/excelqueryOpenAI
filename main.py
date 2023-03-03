import os
import streamlit as st
import pandas as pd
import openai
openai.api_key = os.getenv('OPEN_API_KEY')

def _max_width_():
    max_width_str = f"max-width: 1800px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}

    </style>    
    """,
        unsafe_allow_html=True,
    )

st.set_page_config(page_icon="images/icon.png", page_title="Ask Question to PDF or Link")


c2, c3 = st.columns([6, 1])

with c2:
    c31, c32 = st.columns([12, 2])
    with c31:
        st.caption("")
        st.title("Ask Question to PDF or Link")
    with c32:
        st.image(
            "images/logo.png",
            width=200,
        )
uploaded_file = st.file_uploader(
    " ",
    type="Excel",
    key="1",
    help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",

)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df = df.to_json()
    file_container = st.expander("Check your uploaded .csv")
    file_container.write(df)

else:
    st.info(
        f"""
            👆 Upload a Excel file first - max 50 row!. Sample to try: [biostats.csv](https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv)
            """
    )
    st.stop()


def get_values(question_input):
    try:
        output = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Answer the question truthfully based on the given dataframe below. Made an very short explanation. Use bullet points and find other details about the given question. Question: " + question_input},
                {"role": "system", "content": df},
            ]
        )
        content_value = output['choices'][0]['message']['content']
    except:
        st.write("Please upload a small data - 50 row for the test purposes only")

form = st.form(key="annotation")
with form:
    question_input = st.text_input("Enter your query here")

    submitted = st.form_submit_button(label="Submit your question")
result_df = pd.DataFrame()
if submitted:

    result = get_values(question_input)

c4, c5 = st.columns([6, 1])

with c4:
    st.text(result)