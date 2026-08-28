"""
Streamlit Dashboard untuk Student Performance Monitoring
Versi dengan error handling dan dummy data yang stabil
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import time

# ========== KONFIGURASI ==========
st.set_page_config(
    page_title="🎓 Student Performance Monitoring",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1a73e8;
            text-align: center;
            padding: 1rem 0;
        }
        .kpi-card {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
            margin: 0.5rem 0;
        }
        .kpi-value {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1a73e8;
        }
        .kpi-label {
            font-size: 1rem;
            color: #666;
        }
        .risk-high { background-color: #dc3545; color: white; }
        .risk-medium { background-color: #ffc107; color: black; }
        .risk-low { background-color: #28a745; color: white; }
    </style>
""", unsafe_allow_html=True)

# ========== DATA GENERATOR (DUMMY DATA) ==========

def create_dummy_data():
    """Buat dummy data yang stabil untuk dashboard"""
    
    # Data mahasiswa
    students = [
        {"id": "S001", "name": "Juvenal da Costa"},
        {"id": "S002", "name": "Nelson Martins da Costa"},
        {"id": "S003", "name": "Raimunda Maria auxiliador aines da Costa"},
        {"id": "S004", "name": "Rosalina De Jesus Gama"},
        {"id": "S005", "name": "José Guterres"},
        {"id": "S006", "name": "Teresa Belo"},
        {"id": "S007", "name": "António Ximenes"},
        {"id": "S008", "name": "Isabel da Costa"},
        {"id": "S009", "name": "Manuel Alves"},
        {"id": "S010", "name": "Francisca Babo"},
        {"id": "S011", "name": "Pedro dos Reis"},
        {"id": "S012", "name": "Cecília Monteiro"},
        {"id": "S013", "name": "Fernando de Jesus"},
        {"id": "S014", "name": "Rosa Fernandes"},
        {"id": "S015", "name": "Domingos da Costa"},
        {"id": "S016", "name": "Olivia Amaral"},
        {"id": "S017", "name": "Luís de Araújo"},
        {"id": "S018", "name": "Marta dos Reis"},
        {"id": "S019", "name": "Hélio Soares"},
        {"id": "S020", "name": "Gracinda Belo"},
    ]
    
    data = []
    now = datetime.now()
    
    for s in students:
        # Generate random values
        total_acts = random.randint(5, 50)
        logins = random.randint(2, 15)
        views = random.randint(2, 20)
        quizzes = random.randint(0, 5)
        assignments = random.randint(0, 4)
        avg_quiz = random.randint(40, 100)
        avg_assign = random.randint(40, 100)
        
        # Risk score: higher when activities are low
        if total_acts < 10:
            risk_score = round(random.uniform(0.6, 0.9), 2)
        elif total_acts < 20:
            risk_score = round(random.uniform(0.3, 0.6), 2)
        else:
            risk_score = round(random.uniform(0.1, 0.3), 2)
        
        # Risk level based on score
        if risk_score >= 0.6:
            risk_level = "🔴 High"
        elif risk_score >= 0.3:
            risk_level = "🟡 Medium"
        else:
            risk_level = "🟢 Low"
        
        # Last activity: random hours ago (convert to timedelta safely)
        hours_ago = random.randint(0, 24)
        last_activity = now - timedelta(hours=hours_ago)
        
        data.append({
            "student_id": s["id"],
            "name": s["name"],
            "course": "Big Data",
            "total_activities": total_acts,
            "logins": logins,
            "views": views,
            "quizzes_taken": quizzes,
            "assignments_submitted": assignments,
            "avg_quiz_score": avg_quiz,
            "avg_assignment_grade": avg_assign,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "last_activity": last_activity.strftime("%Y-%m-%d %H:%M")
        })
    
    return pd.DataFrame(data)

# ========== LOAD DATA ==========

@st.cache_data(ttl=10)
def load_data():
    """Load dummy data untuk demo dashboard"""
    st.info("💡 Menggunakan dummy data untuk demo")
    return create_dummy_data()

# ========== MAIN DASHBOARD ==========

# Header
st.markdown('<div class="main-header">🎓 Student Performance Monitoring Dashboard</div>', unsafe_allow_html=True)
st.caption(f"🔄 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Load data
df = load_data()

# Sidebar Filters
st.sidebar.header("⚙️ Filters")
risk_filter = st.sidebar.multiselect(
    "Risk Level",
    options=df["risk_level"].unique(),
    default=df["risk_level"].unique()
)

# Apply filters
filtered_df = df[df["risk_level"].isin(risk_filter)]

# ========== KPI CARDS ==========
st.markdown("### 📊 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{len(filtered_df)}</div>
            <div class="kpi-label">📚 Total Students</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    active = len(filtered_df[filtered_df['total_activities'] > 10])
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color: #28a745;">{active}</div>
            <div class="kpi-label">🟢 Active Students</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    at_risk = len(filtered_df[filtered_df['risk_level'].str.contains('High')])
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color: #dc3545;">{at_risk}</div>
            <div class="kpi-label">🔴 At-Risk Students</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    avg_score = filtered_df['avg_quiz_score'].mean()
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{avg_score:.1f}</div>
            <div class="kpi-label">📝 Avg Quiz Score</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    total_acts = filtered_df['total_activities'].sum()
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{total_acts:,}</div>
            <div class="kpi-label">📈 Total Activities</div>
        </div>
    """, unsafe_allow_html=True)

# ========== CHARTS ==========
st.markdown("---")
st.markdown("### 📈 Analytics & Trends")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Risk Level Distribution")
    risk_counts = filtered_df["risk_level"].value_counts()
    st.bar_chart(risk_counts)

with col2:
    st.subheader("Activities per Student")
    # Sort by total activities descending, ambil top 10
    top_students = filtered_df.nlargest(10, "total_activities")[["name", "total_activities"]]
    st.bar_chart(top_students.set_index("name"))

# ========== RISK TABLE ==========
st.markdown("---")
st.markdown("### 🚨 Student Risk Monitoring")

def highlight_risk(val):
    if "High" in str(val):
        return "background-color: #dc3545; color: white; font-weight: bold;"
    elif "Medium" in str(val):
        return "background-color: #ffc107; color: black; font-weight: bold;"
    else:
        return "background-color: #28a745; color: white; font-weight: bold;"

display_cols = ["student_id", "name", "total_activities", "logins", 
                "quizzes_taken", "avg_quiz_score", "risk_score", "risk_level", "last_activity"]

# Filter columns that exist
available_cols = [col for col in display_cols if col in filtered_df.columns]

styled_df = filtered_df[available_cols].sort_values("risk_score", ascending=False)
styled_df["risk_score"] = styled_df["risk_score"].apply(lambda x: f"{x:.2%}")

# Apply style
st.dataframe(
    styled_df.style.map(highlight_risk, subset=["risk_level"]),
    use_container_width=True,
    height=400
)

# ========== REAL-TIME ACTIVITY FEED ==========
st.markdown("---")
st.markdown("### 🔄 Real-Time Activity Feed")

# Simulasi aktivitas
activities = [
    "📝 Student logged in",
    "📖 Student viewed course material",
    "📊 Student attempted quiz",
    "📎 Student submitted assignment",
    "💬 Student posted in forum",
    "📹 Student watched video",
    "📚 Student downloaded material",
    "✏️ Student updated profile"
]

student_list = filtered_df["name"].tolist() if not filtered_df.empty else ["Student"]

# Tampilkan 3 aktivitas terbaru
for i in range(3):
    student = random.choice(student_list)
    activity = random.choice(activities)
    mins_ago = random.randint(1, 10)
    
    if mins_ago == 1:
        time_str = f"{mins_ago} minute ago"
    else:
        time_str = f"{mins_ago} minutes ago"
    
    st.info(f"🕐 {time_str} | **{student}** → {activity}")

# ========== REFRESH BUTTON ==========
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# ========== AUTO REFRESH SETTINGS ==========
st.sidebar.markdown("---")
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (10s)", value=False)
if auto_refresh:
    time.sleep(10)
    st.rerun()

# ========== FOOTER ==========
st.markdown("---")
st.caption("📌 **Pipeline:** Simulated Data → Apache Kafka → Apache Spark → MongoDB → Streamlit Dashboard")
st.caption("🏫 **University:** Timor-Leste | **Course:** Big Data | **Semester:** 2026/2")

# Show data source info
st.sidebar.info("📊 **Data Source:** Dummy Data (Demo Mode)")
