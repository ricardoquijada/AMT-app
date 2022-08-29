from asyncore import read
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


@st.cache(allow_output_mutation=True)
def read_sheets(sheet_id):
    df = pd.read_csv(
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
    df.drop_duplicates(subset="Code 86")
    return df


def skill_columns(skill):
    list_columns = answer_df.columns.to_list()
    general_info = list_columns[1:9]
    cols_to_use = general_info
    if skill == "Systems":
        cols_to_use.extend(list_columns[10:22])
        cols_to_use.extend(list_columns[24:40])
    if skill == "Avionics":
        cols_to_use.extend(list_columns[41:53])
        cols_to_use.extend(list_columns[55:66])
    if skill == "Structures":
        cols_to_use.extend(list_columns[67:73])
        cols_to_use.extend(list_columns[75:89])
    if skill == "Interiors":
        cols_to_use.extend(list_columns[90:111])
        cols_to_use.extend(list_columns[113:125])
    return cols_to_use


def total(skill):
    if skill == "All":
        total_surveys = answer_df.shape[0]
    else:
        total_surveys = answer_df[answer_df["Skill"]
                                  == skill_selected].shape[0]
    return total_surveys


answer_sheet = "1Uwhn3yj7SfCRJO1LACrOJ30Q6zDraV4BhUK6i6U2DPw"
answer_df = read_sheets(answer_sheet)
database_sheet = "1I4kLvXgBiSm2Mq_p0hZ2Dv0SLCl9yBGPU-zYyil4QJo"
full_df = read_sheets(database_sheet)

# ----- Sidebar Selection ------
total_per_skill = {
    "Systems": full_df[(full_df["SKILL"] == "SYS")].shape[0],
    "Interiors": full_df[(full_df["SKILL"] == "INT")].shape[0],
    "Structures": full_df[(full_df["SKILL"] == "STR")].shape[0],
    "Avionics": full_df[(full_df["SKILL"] == "AVI")].shape[0],
    "All": full_df.shape[0]
}
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
list_columns = answer_df.columns.to_list()

# ---- Header ----
st.image("./img/aeroman7371.jpg", width=250)
st.write("# AMT Subskill Overview")
Verification, Overview = st.tabs(["Verification", "Overview"])
with Verification:
    code_86 = st.text_input("Code 86")
    if code_86 in full_df["Code 86"].tolist():
        st.success('Complete')
    else:
        st.warning("Pending to survey")
with Overview:
    total_surveys = total(skill_selected)
    st.write(f"  ###  🎯 Total Surveys - {skill_selected}: {total_surveys}")
    st.progress(total_surveys/total_per_skill[skill_selected])
    st.write(
        f"#### {round((total_surveys/total_per_skill[skill_selected])*100,1)} %")
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
        cols_used = skill_columns(skill_selected)
        data_filtered = answer_df[cols_used][(answer_df["Skill"] == skill_selected) & (
            answer_df["Business Unit"] == bu_selected)]
        st.dataframe(data_filtered)
        skill_set = data_filtered.groupby("Current Role").count()
        fig = go.Figure(
            data=go.Bar(x=answer_df["Current Role"].unique(
            ), y=skill_set["Code 86"]), layout_yaxis_range=[0, 90], layout=go.Layout(
                title=go.layout.Title(text=f"Current Role - {skill_selected}")))
        st.plotly_chart(fig)
    if skill_selected == "All":
        st.dataframe(answer_df)
        skill_set = answer_df.groupby("Skill").count()
        x = answer_df.groupby("Business Unit").count()
        BU_fig = px.pie(x, values="E-mail", names=x.index, color=x.index, color_discrete_map={
            "U1": "darkblue",
            "U2": "royalblue",
            "U3": "lightcyan"}, title="Business Unit Distribution", hole=0.3)
        st.plotly_chart(BU_fig)
        x = answer_df.groupby("Current Role").count()
        Role_fig = px.pie(x, values="E-mail", names=x.index, color=x.index,
                          color_discrete_sequence=px.colors.sequential.RdBu, title="Current Role Distribution", hole=0.3)
        st.plotly_chart(Role_fig)
        x = answer_df.groupby("VISA").count()
        Visa_fig = px.pie(x, values="E-mail", names=x.index, color=x.index,
                          color_discrete_sequence=px.colors.sequential.RdBu, title="VISA", hole=0.3)
        st.plotly_chart(Visa_fig)
