import json
import streamlit as st
from langchain_ot import langchain_output

st.set_page_config(layout="wide")


def load_questions():
    with open('test.json') as json_file:
        data = json.load(json_file)

    questions = []
    for i, q in enumerate(data['data'][0]['paragraphs'][0]['qas']):
        question = data['data'][0]['paragraphs'][0]['qas'][i]['question']
        questions.append(question)
    return questions


def load_contracts():
    with open('test.json') as json_file:
        data = json.load(json_file)

    contracts = []
    for i, q in enumerate(data['data']):
        contract = ' '.join(data['data'][i]['paragraphs'][0]['context'].split())
        contracts.append(contract)
    return contracts

questions = load_questions()
contracts = load_contracts()

contract = contracts[0]

st.header("Legal Document QA Engine")

selected_question = st.selectbox('Choose any one query from the pool:', questions)
question_set = [questions[0], selected_question]

contract_type = st.radio("Select Contract", ("Sample Contract", "New Contract"))
if contract_type == "Sample Contract":
    sample_contract_num = st.slider("Select Sample Contract #")
    contract = contracts[sample_contract_num]
    with st.expander(f"Sample Contract #{sample_contract_num}"):
        st.write(contract)
else:
    contract = st.text_area("Input New Contract", "", height=256)

Run_Button = st.button("Run", key=None)
if Run_Button == True and not len(contract) == 0 and not len(question_set) == 0:
    predictions = langchain_output(question_set, contract)

    for i, p in enumerate(predictions):
        print(predictions[p])
        if i != 0: st.write(f"Question: {question_set[int(p)]}\n\nAnswer: {predictions[p]}\n\n")
