import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# PAGE SETUP


st.set_page_config(
    page_title="Student Career Dashboard",
    page_icon="🎓",
    layout="wide"
)


# LOAD DATA


df = pd.read_csv("student_career_performance_cleaned.csv")


# TITLE & DESCRIPTION

st.title("🎓 Student Career & Performance Intelligence Dashboard")

st.caption(
    "Academic performance • Career development • Placement • Student risk"
)

st.write("**Developed by:** Manthan Mohite & Arya Marde")


# SIDEBAR FILTERS

st.sidebar.header("🔎 Dashboard Filters")

department = st.sidebar.multiselect(
    "Department",
    sorted(df["Department"].unique()),
    default=sorted(df["Department"].unique())
)

semester = st.sidebar.multiselect(
    "Semester",
    sorted(df["Semester"].unique()),
    default=sorted(df["Semester"].unique())
)

gender = st.sidebar.multiselect(
    "Gender",
    sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

internship = st.sidebar.multiselect(
    "Internship",
    sorted(df["Internship"].unique()),
    default=sorted(df["Internship"].unique())
)

risk = st.sidebar.multiselect(
    "Risk Level",
    sorted(df["Risk_Level"].unique()),
    default=sorted(df["Risk_Level"].unique())
)


# FILTER DATA


data = df[
    df["Department"].isin(department)
    & df["Semester"].isin(semester)
    & df["Gender"].isin(gender)
    & df["Internship"].isin(internship)
    & df["Risk_Level"].isin(risk)
].copy()

if data.empty:
    st.warning("No students match the selected filters.")
    st.stop()

st.info(f"Showing {len(data)} students out of {len(df)}")


# KPI CALCULATIONS


total = len(data)
avg_percentage = data["Final_Percentage"].mean()
avg_attendance = data["Attendance"].mean()

placement_rate = (
    data["Placement_Status"].eq("Placed").mean() * 100
)

high_risk = data["Risk_Level"].eq("High Risk").sum()

placed = data[data["Placement_Status"] == "Placed"]

avg_package = (
    placed["Package_LPA"].mean()
    if not placed.empty else 0
)


# KPI CARDS


st.subheader("📌 Performance Overview")

c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)

c1.metric("👨‍🎓 Total Students", total)
c2.metric("📈 Avg Percentage", f"{avg_percentage:.2f}%")
c3.metric("🎯 Avg Attendance", f"{avg_attendance:.2f}%")
c4.metric("💼 Placement Rate", f"{placement_rate:.2f}%")
c5.metric("🚨 High Risk", high_risk)
c6.metric("💰 Avg Package", f"{avg_package:.2f} LPA")


# ACADEMIC ANALYSIS


st.divider()
st.header("📚 Academic Performance Analytics")

col1, col2 = st.columns(2)

# Department Performance
with col1:

    st.subheader("📊 Department Performance")

    department_avg = (
        data.groupby("Department")["Final_Percentage"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots()

    department_avg.plot(
        kind="bar",
        ax=ax,
        color="steelblue"
    )

    ax.set_ylabel("Average Percentage")
    ax.set_xlabel("Department")
    ax.tick_params(axis="x", rotation=30)
    ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# Placement Status
with col2:

    st.subheader("💼 Placement Status")

    placement = data["Placement_Status"].value_counts()

    fig, ax = plt.subplots()

    ax.pie(
        placement,
        labels=placement.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Placement Distribution")

    st.pyplot(fig)
    plt.close(fig)

# Attendance vs Percentage
st.subheader("🎯 Attendance vs Final Percentage")

fig, ax = plt.subplots(figsize=(10, 5))

ax.scatter(
    data["Attendance"],
    data["Final_Percentage"],
    alpha=0.6
)

ax.set_xlabel("Attendance (%)")
ax.set_ylabel("Final Percentage (%)")
ax.grid(alpha=0.25)

st.pyplot(fig)
plt.close(fig)


# CAREER & PLACEMENT


st.divider()
st.header("💼 Career & Placement Analytics")

col1, col2 = st.columns(2)

# Projects vs Placement
with col1:

    st.subheader("💻 Projects vs Placement")

    projects = (
        data.groupby("Projects_Completed")["Placement_Status"]
        .apply(lambda x: x.eq("Placed").mean() * 100)
    )

    fig, ax = plt.subplots()

    projects.plot(
        kind="bar",
        ax=ax,
        color="darkorange"
    )

    ax.set_xlabel("Projects Completed")
    ax.set_ylabel("Placement Rate (%)")
    ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# Certifications vs Placement
with col2:

    st.subheader("📜 Certifications vs Placement")

    certifications = (
        data.groupby("Certifications")["Placement_Status"]
        .apply(lambda x: x.eq("Placed").mean() * 100)
    )

    fig, ax = plt.subplots()

    certifications.plot(
        kind="bar",
        ax=ax,
        color="crimson"
    )

    ax.set_xlabel("Certifications")
    ax.set_ylabel("Placement Rate (%)")
    ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# Package by Department
st.subheader("💰 Average Package by Department")

if not placed.empty:

    package = (
        placed.groupby("Department")["Package_LPA"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    package.plot(
        kind="bar",
        ax=ax,
        color="darkviolet"
    )

    ax.set_xlabel("Department")
    ax.set_ylabel("Average Package (LPA)")
    ax.tick_params(axis="x", rotation=30)
    ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# RISK ANALYSIS


st.divider()
st.header("🚨 Student Risk Analysis")

col1, col2 = st.columns(2)

# Risk Distribution
with col1:

    st.subheader("Risk Distribution")

    risk_count = data["Risk_Level"].value_counts()

    fig, ax = plt.subplots()

    risk_count.plot(
        kind="bar",
        ax=ax,
        color="tomato"
    )

    ax.set_xlabel("Risk Level")
    ax.set_ylabel("Students")
    ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# Risk vs Performance
with col2:

    st.subheader("Risk vs Final Percentage")

    risk_performance = (
        data.groupby("Risk_Level")["Final_Percentage"]
        .mean()
        .reindex(
            ["Low Risk", "Medium Risk", "High Risk"]
        )
    )

    fig, ax = plt.subplots()

    risk_performance.plot(
        kind="bar",
        ax=ax,
        color="goldenrod"
    )

    ax.set_xlabel("Risk Level")
    ax.set_ylabel("Average Percentage")
    ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# INDIVIDUAL STUDENT PROFILE
 

st.divider()
st.header("👤 Individual Student Profile")

student_id = st.selectbox(
    "Select Student",
    data["Student_ID"].tolist()
)

student = data[
    data["Student_ID"] == student_id
].iloc[0]

col1, col2, col3 = st.columns(3)

with col1:

    st.subheader("📚 Academic")

    st.write(f"**Department:** {student['Department']}")
    st.write(f"**Semester:** {student['Semester']}")
    st.write(f"**Attendance:** {student['Attendance']:.1f}%")
    st.write(f"**Final Percentage:** {student['Final_Percentage']:.1f}%")
    st.write(f"**Backlogs:** {student['Backlogs']}")

with col2:

    st.subheader("💻 Career")

    st.write(f"**Projects:** {student['Projects_Completed']:.0f}")
    st.write(f"**Certifications:** {student['Certifications']}")
    st.write(
        f"**Coding Hours/Week:** "
        f"{student['Coding_Hours_Per_Week']:.1f}"
    )
    st.write(f"**Internship:** {student['Internship']}")

with col3:

    st.subheader("💼 Placement")

    st.write(f"**Status:** {student['Placement_Status']}")
    st.write(f"**Package:** {student['Package_LPA']:.2f} LPA")
    st.write(f"**Risk:** {student['Risk_Level']}")
    st.write(
        f"**Interview Score:** "
        f"{student['Interview_Score']:.1f}"
    )

# ==================================================
# WHAT-IF SIMULATOR
# ==================================================

st.divider()
st.header("🔮 What-If Performance Simulator")

st.caption(
    "Experiment with attendance and study hours "
    "to explore an estimated performance scenario."
)

col1, col2 = st.columns(2)

with col1:

    new_attendance = st.slider(
        "🎯 Attendance (%)",
        0.0,
        100.0,
        float(student["Attendance"]),
        1.0
    )

with col2:

    new_study_hours = st.slider(
        "📚 Study Hours Per Day",
        0.5,
        10.0,
        float(student["Study_Hours_Per_Day"]),
        0.5
    )

attendance_change = (
    new_attendance - student["Attendance"]
)

study_change = (
    new_study_hours - student["Study_Hours_Per_Day"]
)

estimated = (
    student["Final_Percentage"]
    + attendance_change * 0.10
    + study_change * 1.5
)

estimated = max(0, min(100, estimated))

change = estimated - student["Final_Percentage"]

c1, c2, c3 = st.columns(3)

c1.metric(
    "Current Percentage",
    f"{student['Final_Percentage']:.2f}%"
)

c2.metric(
    "Estimated Percentage",
    f"{estimated:.2f}%"
)

c3.metric(
    "Estimated Change",
    f"{change:+.2f}%"
)

st.info(
    "This is an analytical What-If simulation, "
    "not a guaranteed prediction."
)


# DATA DOWNLOAD


st.divider()
st.header("📋 Student Data")

with st.expander("View Filtered Student Data"):

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "📥 Download Filtered CSV",
        data.to_csv(index=False),
        "filtered_student_data.csv",
        "text/csv"
    )

# ==================================================
# ABOUT PROJECT
# ==================================================

st.divider()
st.header("ℹ️ About the Project")

st.write(
    "**Student Career & Performance Intelligence Dashboard**"
)

st.write(
    "**Group Members:** Manthan Mohite & Arya Marde"
)

st.write(
    "**Technologies:** Python, NumPy, Pandas, Matplotlib, Streamlit"
)

st.write(
    "The project analyzes academic performance, career preparation, "
    "placement outcomes, and student risk using data analysis."
)