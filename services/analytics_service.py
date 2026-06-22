from queries.analytics_queries import (
    get_today_attendance_stats,
    get_faculty_availability,
    get_today_faculty_status
)
import plotly.express as px
import pandas as pd
from datetime import date, timedelta

from queries.analytics_queries import (
    get_analytics_attendance_counts,
    get_analytics_attendance_by_dept,
    get_analytics_faculty_tasks
)

from queries.semester_queries import (
    get_active_semester_details
)


def _get_date_range(period):
    today = date.today()
    if period == "Today":
        return today, today
    elif period == "This Week":
        return today - timedelta(days=today.weekday()), today
    elif period == "This Month":
        return today.replace(day=1), today
    elif period == "Semester":
        sem = get_active_semester_details()
        if sem:
            return sem[2], sem[3]
        return today - timedelta(days=30), today
    return today, today


def get_analytics_attendance_pie(period):
    start_date, end_date = _get_date_range(period)
    data = get_analytics_attendance_counts(start_date, end_date)
    
    if not data:
        return None
        
    df = pd.DataFrame(data, columns=["Status", "Count"])
    df["Status"] = df["Status"].str.capitalize()
    
    fig = px.pie(df, values='Count', names='Status', hole=0.4)
    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20))
    return fig


def get_analytics_attendance_dept_bar(period):
    start_date, end_date = _get_date_range(period)
    data = get_analytics_attendance_by_dept(start_date, end_date)
    
    if not data:
        return None
        
    df = pd.DataFrame(data, columns=["Department", "Status", "Count"])
    df["Status"] = df["Status"].str.capitalize()
    
    fig = px.bar(df, x="Department", y="Count", color="Status", barmode="group")
    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), xaxis_title="", yaxis_title="Count")
    return fig


def _get_workload_data(department):
    sem = get_active_semester_details()
    if not sem:
        return []
    start_date, end_date = sem[2], sem[3]
    return get_analytics_faculty_tasks(start_date, end_date, department)


def get_analytics_workload_teaching_bar(department):
    data = _get_workload_data(department)
    teaching_data = [row for row in data if row[1] == "Teaching"]
    
    if not teaching_data:
        return None
        
    df = pd.DataFrame(teaching_data, columns=["Faculty", "Task", "Hours"]).drop(columns=["Task"])
    df = df.sort_values(by="Hours", ascending=True)
    
    fig = px.bar(df, x="Hours", y="Faculty", orientation="h")
    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), xaxis_title="Teaching Hours", yaxis_title="")
    return fig


def get_analytics_workload_distribution_pie(department):
    data = _get_workload_data(department)
    
    if not data:
        return None
        
    df = pd.DataFrame(data, columns=["Faculty", "Task", "Hours"])
    task_summary = df.groupby("Task")["Hours"].sum().reset_index()
    
    fig = px.pie(task_summary, values='Hours', names='Task', hole=0.4)
    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20))
    return fig


def get_analytics_workload_free_bar(department):
    data = _get_workload_data(department)
    free_data = [row for row in data if row[1] == "Free"]
    
    if not free_data:
        return None
        
    df = pd.DataFrame(free_data, columns=["Faculty", "Task", "Hours"]).drop(columns=["Task"])
    df = df.sort_values(by="Hours", ascending=True)
    
    fig = px.bar(df, x="Hours", y="Faculty", orientation="h")
    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), xaxis_title="Free Hours", yaxis_title="")
    return fig

def fetch_today_faculty_status():

    return (
        get_today_faculty_status()
    )


def fetch_dashboard_stats():

    return (
        get_today_attendance_stats()
    )


def fetch_faculty_availability(
    slot_number
):

    return (
        get_faculty_availability(
            slot_number
        )
    )