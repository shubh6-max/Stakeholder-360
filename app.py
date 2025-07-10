import streamlit as st
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config

def render_info_table(title, data_dict, color="#cce5ff",name_for_link=None):
    """Render a colored section title + 2-column HTML table with LinkedIn URL as clickable"""
    st.markdown(f"""
        <div style='background-color:{color};padding:8px;border-radius:5px;
        margin-top:20px;margin-bottom:5px;font-weight:bold;font-size:16px'>
            {title}
        </div>
    """, unsafe_allow_html=True)

    table_html = """
        <table style='width:100%;border-collapse:collapse;font-size:15px;'>
    """

    for k, v in data_dict.items():
        if k.lower().startswith("linkedin") and pd.notna(v):
            label = name_for_link or v
            v = f"<a href='{v}' target='_blank' style='color:#1a0dab;text-decoration:underline'>linkedin/{label}</a>"
        elif not pd.notna(v):
            v = "-"

            
        table_html += f"""
        <tr style='border-bottom:1px solid #ddd'>
            <td style='padding:6px 10px;font-weight:600;width:40%;background-color:#f2f2f2'>{k}</td>
            <td style='padding:6px 10px;background-color:#f2f2f2'>{v}</td>
        </tr>
        """

    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)



# Page layout
st.set_page_config(page_title="Stakeholder Org Viewer", layout="wide",page_icon="https://media.licdn.com/dms/image/v2/D4D0BAQFSLuRei6pVZA/company-logo_200_200/B4DZfJuCNfGgAI-/0/1751435978200/themathcompany_logo?e=1756944000&v=beta&t=CkeqG4ihtOep-IGUMLTLMItiVdFJ4-TroEeSoXs1Jxw")

st.markdown("""
    <style>
    /* Remove default Streamlit padding from top */
    .block-container {
        padding-top: 0rem !important;
    }

    .stApp {
        background-color: #ebe3d6;
    }

    .logo-container {
        display: flex;
        align-items: center;
        padding: 5px 0px 0px 10px; /* Reduced top padding */
        margin-top: 20px;  /* Pull logo upward */
        margin-left: -0px;
        margin-bottom: 40px;
    }

    .logo-container img {
        width: 150px;
        background-color: white;
        padding: 5px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    </style>

    <div class="logo-container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/8/88/MathCo_Logo.png" />
    </div>
""", unsafe_allow_html=True)

st.markdown("### **Stakeholder 360**",)

uploaded_file = st.file_uploader("**📂 Upload Excel File**", type=["xlsx"])

col_filter1, col_filter2,col_filter3, col_filter4= st.columns(4)

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    with col_filter1:
        sheet = st.selectbox("**Select Sheet**", ["-- Select Sheet --"] + xls.sheet_names)
        # Block until valid selection
        if sheet == "-- Select Sheet --":
            st.warning("⚠️ Please select the updated sheet to continue.")
            st.stop()  # 🚫 HALTS further app execution
        else:
            df = pd.read_excel(xls, sheet_name=sheet)
    
    df["Vendor CompanyName"].fillna("-")
    
    # st.write(df)

    df = df.dropna(subset=["Client Name"])

    with col_filter2:
        selected_working_group = st.selectbox(
            "**Working Group**", ["All"] + sorted(df["Working Group"].dropna().unique().tolist())
        )

    with col_filter3:
        selected_business_function = st.selectbox(
            "**Business Functions**", ["All"] + sorted(df["Business Functions"].dropna().unique().tolist())
        )

    # --- Apply filtering logic ---
    filtered_df = df.copy()

    if selected_working_group != "All":
        filtered_df = filtered_df[filtered_df["Working Group"] == selected_working_group]

    if selected_business_function != "All":
        filtered_df = filtered_df[filtered_df["Business Functions"] == selected_business_function]

    # --- Stakeholder dropdown ---
    client_names = filtered_df["Client Name"].dropna().unique()

    if len(client_names) == 0:
        st.warning("⚠️ No stakeholders match the selected filters.")
        st.stop()

    with col_filter4:
        selected_client = st.selectbox("**Select Stakeholder**", sorted(client_names))

    # Work only on filtered row
    row = filtered_df[filtered_df["Client Name"] == selected_client].iloc[0]


    if selected_client:
        # Get selected row
        row = df[df["Client Name"] == selected_client].iloc[0]

        # Extract hierarchy
        client = row["Client Name"]
        mgr_1 = row["1st degree Manager"]
        mgr_2 = row["2nd Degree Manager"]

        # --- Build Mini Org Chart with reportees ---
        nodes = []
        edges = []
        added = set()

        def add_node(name, title=None, color="lightblue", shape="box"):
            if pd.notna(name) and name not in added:
                label = name if not title else f"{name}\n{title}"
                nodes.append(Node(
                    id=name,
                    label=label,
                    color=color,
                    shape=shape,
                    font={"size": 25}
                ))
                added.add(name)

        # Managers
        # Add the hidden spacer node
        add_node(mgr_2, color="lightgray")
        add_node(mgr_1, color="#4A90E2")
        add_node(client, color="#6AA84F")

        # Edges upward
        if pd.notna(mgr_2) and pd.notna(mgr_1):
            edges.append(Edge(source=mgr_2, target=mgr_1))
        if pd.notna(mgr_1):
            edges.append(Edge(source=mgr_1, target=client))

        # Reportees of selected client
        reportees_df = df[df["1st degree Manager"] == client]
        for _, rep in reportees_df.iterrows():
            r_name = rep["Client Name"]
            add_node(r_name, color="#FFF2CC")
            edges.append(Edge(source=client, target=r_name))

        # Config for AGraph
        # MAIN
        config = Config(
        width="100%", # type: ignore
        height=600,
        font={"size":25},
        directed=True,
        physics=False,
        hierarchical=True,
        hierarchicalOption={
            "direction": "UD",  # Top-down
            "sortMethod": "directed",
            "nodeSpacing":6000,
            "levelSeparation":600,
            "parentCentralization":True,
        }
    )

        st.subheader(f"🙎🏻‍♂️ Org Chart for {selected_client}")
        agraph(nodes=nodes, edges=edges, config=config)


        
        # ==== DEFINE COLUMNS ====
        col1, col2 = st.columns(2)

        # ==== LEFT COLUMN ====
        with col1:
            render_info_table("👤 Lead Identification & Contact Details", {
        "Business Group":row["Business Group"],
        "Lead Priority":row["Lead Priority"],
        "Client Name":row["Client Name"],
        "Designation": row["Designation"],
        "Location (from teams)": row["Location (from teams)"],
        "Email address": row["Email address"],
        "LinkedIn URL": row["LinkedIn URL"]
    }, name_for_link=row["Client Name"])

            render_info_table("📬 Engagement & Outreach Strategy", {
                "Scope of work/Priorities (internal research)": row["Scope of work/Priorities (internal research)"],
                "Additional Research (External)": row["Additional Research (External)"],
                "MathCo LinkedIn Connects": row["MathCo LinkedIn Connects"],
                "Introduction Path": row["Introduction Path"],
                "Pursured in past": row["Pursured in past"],
                "Relationship Strength": row["Relationship Strength"],
                # "Lead Status": row["Lead Status"],
                "Lead Potential ESS": row["Lead Potential ESS (func. Of designation & Vendor Count)"],
                "Lead Potential DAC": row["Lead Potential DAC (func. Of designation & Vendor Count)"],
                # "Scope of work/Priorities": row["Scope of work/Priorities (internal research)"],
                "If Yes, background/context ?": row["If Yes, background/context ?"],
                "Comments": row["Comments"],
                
            })

        # ==== RIGHT COLUMN ====
        with col2:
            render_info_table("🏢 Company & Department Info", {
                "Business Segment": row["Business Segment"],
                "Working Group": row["Working Group"],
                "Business Functions": row["Business Functions"],
                # "1st Degree Manager": row["1st degree Manager"],
                # "2nd Degree Manager": row["2nd Degree Manager"]
            })

            render_info_table("🧑‍🤝‍🧑 Organizational Hierarchy", {
                "1st Degree Manager": row["1st degree Manager"],
                "2nd Degree Manager": row["2nd Degree Manager"]
            })

            render_info_table("📊 Lead Status & Tracking", {
                "Who will reach out ?": row["Who will reach out ?"],
                "Lever for Reach out(s) ready (Cold email/LinkedIn Message/Demos/PoVs etc.) ?": row["Lever for Reach out(s) ready (Cold email/LinkedIn Message/Demos/PoVs etc.) ?"],
                "Lead Status": row["Lead Status"]
            })
            render_info_table("🧠 Expertise & Experience", {
                "Designation Seniority": row["Designation Seniority"],
                "Location (From LinkedIn)": row["Location (from LinkedIn)"]
            })

            render_info_table("📦 Contractor Information", {
                "Contractor count": (row["Contractor Count"]),
                "Vendor Company Name": (row["Vendor CompanyName"])
            })

