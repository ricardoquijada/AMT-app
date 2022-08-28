import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache
def read_sheets(sheet_id):
    df = pd.read_csv(
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
    df.drop_duplicates(subset="Code 86")
    return df


@st.cache
def convert_csv(data):
    return data.to_csv(data).encode("utf-8")


def total(skill):
    if skill == "All":
        total_surveys = answer_df.shape[0]
    else:
        total_surveys = answer_df[answer_df["Skill"]
                                  == skill_selected].shape[0]
    return total_surveys


answer_sheet = "1Uwhn3yj7SfCRJO1LACrOJ30Q6zDraV4BhUK6i6U2DPw"
answer_df = read_sheets(answer_sheet)

subskill = {
    "All": [],
    "Systems": ["Engines", "Flight Control", "Packs", "Landing Gear", "Fuel Tanks"],
    "Structures": ["Minor Repair", "Mid Repair", "Major Repair", "Modifications", "Fuel Tanks"],
    "Interiors": ["Doors", "Windows", "Seats"],
    "Avionics": ["Modifications", "Cockpit Operationals"]
}
skill_selected = st.sidebar.selectbox(
    "Skill", ["All", "Systems", "Avionics", "Structures", "Interiors"])
bu_selected = st.sidebar.selectbox("Business Unit", ["U1", "U2", "U3"])
subskill_selected = st.sidebar.selectbox("Subskill", subskill[skill_selected])
# ---- Header ----
st.image("./img/aeroman7371.jpg", width=250)
st.write("# AMT Subskill Overview")
total_surveys = total(skill_selected)
st.write(f"  ###  🎯 Total Surveys: {total_surveys}")
col1, col2, col3 = st.columns(3)
x = answer_df.value_counts(["Skill", "Business Unit"])
with col1:
    if skill_selected == "All":
        count_1 = answer_df.value_counts(["Business Unit"])["U1"][0]
    else:
        count_1 = x[skill_selected]["U1"]
    st.header(f"U1: {count_1}")

with col2:
    if skill_selected == "All":
        count_2 = answer_df.value_counts(["Business Unit"])["U2"][0]
    else:
        count_2 = x[skill_selected]["U2"]
    st.header(f"U2 : {count_2}")
with col3:
    if skill_selected == "All":
        count_3 = answer_df.value_counts(["Business Unit"])["U3"][0]
    else:
        count_3 = x[skill_selected]["U3"]
    st.header(f"U3: {count_3}")
if skill_selected != "All":
    data_filtered = answer_df[(answer_df["Skill"] == skill_selected) & (
        answer_df["Business Unit"] == bu_selected)]
    st.dataframe(data_filtered)
if skill_selected == "All":
    st.dataframe(answer_df)
