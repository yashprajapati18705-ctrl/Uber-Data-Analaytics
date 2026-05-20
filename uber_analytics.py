import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Uber Data Analytics",layout="wide")

df = pd.read_csv("uber_analytics_dataset.csv")

with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Dataset","Overview","Ride Analytics","Data Assistant"],
        icons=["table","bar-chart","graph-up","robot"],
        menu_icon="car-front",
        default_index=0
    )

if selected == "Dataset":

    st.title("Dataset Explorer")
    st.divider()

    col1 , col2 , col3 = st.columns(3)

    col1.metric("Total Rows : ",df.shape[0])
    col2.metric("Total Cols : ",df.shape[1])
    col3.metric("Total Missing Values : ",df.isna().sum().sum())

    # column selection

    st.subheader("Select Column")

    selected_columns = st.multiselect("Select columns to display ",df.columns,default=df.columns)

    filtered_df = df[selected_columns]

    st.subheader("Search in Dataset ")
    search_value = st.text_input("Search any value")

    if search_value:
        filtered_df = filtered_df[filtered_df.astype(str).apply(
            lambda row: row.str.contains(search_value,case=False).any(),axis=1
        )]

    st.subheader("Column Filter")

    col1 , col2 = st.columns(2)

    with col1:
        filter_column = st.selectbox("Select Column",filtered_df.columns)

    with col2:
        filter_value = st.selectbox("Select Value",filtered_df[filter_column].dropna().unique())

    if st.button("Apply Filter"):
        filtered_df = filtered_df[filtered_df[filter_column]==filter_value]

    st.divider()

    st.subheader("Row Display")

    row = st.slider("Number of Rows to Display",10,len(filtered_df),20)

    st.divider()

    st.subheader("Dataset Table")

    st.dataframe(filtered_df.head(row),use_container_width=True,hide_index=True)

    if st.checkbox("Show Full Dataset"):
        st.dataframe(filtered_df,use_container_width=True)

    st.divider()

    # COLUMN STATS

    st.subheader("Column Stats")

    st.write(filtered_df.describe())
    numeric_cols = filtered_df.select_dtypes(include=["int64","float64"]).columns
    st.write("Numeric Columns")

    if len(numeric_cols)>0:
        selected_numeric = st.selectbox("Select a numeric column",numeric_cols)
        st.write(filtered_df[selected_numeric].describe())

    st.divider()

    st.subheader("Download Data")

    csv = filtered_df.to_csv(index=False)

    st.download_button("Download Filtered dataset",csv,"Filtered_uber_data.csv","text/csv")

elif selected == "Overview":
    st.title("Uber Operations")
    st.markdown("---")

    total_rides = len(df)

    completed_rides = df[df["Booking Status"]=="Completed"]
    total_revenue = completed_rides["Booking Value"].sum()

    avg_distance = completed_rides["Ride Distance"].mean()

    success_rate = (len(completed_rides)/total_rides*100 if total_rides>0 else 0)

    avg_rating = completed_rides["Customer Rating"].mean()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric("Gross Booking Value",f"{total_revenue:,.2f}","Target : $1.1M")

    kpi2.metric("Fulfilment Rate",f"{success_rate:,.1f}","-2.4% vs Last Month")

    kpi3.metric("Avg Trip Distance",f"{avg_distance:,.2f}km")

    kpi4.metric("Avg Customer Rating",f"{avg_rating:,.1f}/5.0")

    st.divider()

    st.subheader("Business Unit Performance Matrix")

    bu_metrics = df.groupby("Vehicle Type").agg(
        Total_Booking=("Booking ID","count"),
        Revenue_Generated=("Booking Value","sum"),
        Avg_Distance=("Ride Distance","mean"),
        Avg_Rating=("Customer Rating","mean")
    )

    bu_metrics["Revenue_Share_%"] = (bu_metrics["Revenue_Generated"]/total_revenue*100 if total_revenue>0 else 0)

    st.dataframe(bu_metrics.style.format({
        "Revenue_Generated":"$ {:,.0f}",
        "Avg_Distance":"{:,.2f}km",
        "Avg_Rating":"{:,.1f}/5.0",
        "Revenue_Share_%":"{:,.1f}%"
    }).background_gradient(subset=["Revenue_Generated"],cmap="Blues"),use_container_width=True)

    st.divider()

    eff_col , can_col = st.columns(2)

    with eff_col:
        st.subheader("Operational Efficiency")
        eff_df = df.groupby("Vehicle Type")[["Avg VTAT","Avg CTAT"]].mean()
        st.write("Average Turn Around Time ( Minutes )")

        st.dataframe(eff_df.style.highlight_max(axis=0,color="#800080").highlight_min(axis=0,color="#8dd7bf"),use_container_width=True)

    with can_col:
        st.header("Cancellation Audit")
        status_count = df["Booking Status"].value_counts().to_frame(name="Count")
        # st.write(status_count)
        status_count["Share_%"] = (status_count["Count"]/total_rides*100)
        st.dataframe(status_count,use_container_width=True)

    st.divider()

    st.header("Financial Deep Dive")

    pay_col , reason_col = st.columns([4,6])

    # Payment Analysis

    with pay_col:
        st.markdown("** Payment Method Preferences")

        pay_summary = (completed_rides["Payment Method"].value_counts(normalize=True)*100)
        st.dataframe(pay_summary.rename("Usage_%"),use_container_width=True)

    with reason_col:
        st.markdown("** Primary Cancellation Triggers")

        cust_reasons = df["Reason for cancelling by Customer"].dropna().value_counts().head(3)
        drv_reasons = df["Driver Cancellation Reason"].dropna().value_counts().head(3)
        cust_reasons.index = "Customer : " + cust_reasons.index
        drv_reasons.index = "Driver : " + drv_reasons.index

        reason_df = pd.concat([cust_reasons,drv_reasons]).to_frame()

        reason_df.columns = ["Incident Count"]
        st.dataframe(reason_df)

elif  selected == "Ride Analytics":
    st.title("Advanced Ride Analytics Dashboard")
    st.divider()

    completed = df[df["Booking Status"]=="Completed"]

    # Sunburst Chart

    st.header("Ride Hierarchy")

    fig1 = px.sunburst(
        completed,
        path=["Vehicle Type","Payment Method"],
        values="Booking Value",
        color="Booking Value",
        color_continuous_scale="Turbo"
    )

    st.plotly_chart(fig1,use_container_width=True)

    st.divider()

    st.header("Revenue Chart")

    fig2 = px.treemap(
        completed,
        path=["Vehicle Type","Payment Method"],
        values="Booking Value",
        color="Booking Value",
        color_continuous_scale="Blues"
    )

    fig2.update_layout(margin=dict(t=20,l=0,r=0,b=0),height=420)
    st.plotly_chart(fig2,use_container_width=True)

    st.divider()

    st.header("Customer Rating Spread")

    fig3 = px.box(
        completed,
        x="Vehicle Type",
        y="Customer Rating",
        color="Vehicle Type"
    )

    st.plotly_chart(fig3,use_container_width=True)

    # Sankey

    st.subheader("Ride Flow Analytics")

    flow = df.groupby(["Vehicle Type","Booking Status"]).size().reset_index(name="count")

    source_label = flow["Vehicle Type"].unique().tolist()
    target_label = flow["Booking Status"].unique().tolist()

    labels = source_label+target_label

    source = flow["Vehicle Type"].apply(
        lambda x: labels.index(x)).tolist()

    target = flow["Booking Status"].apply(
        lambda x: labels.index(x)).tolist()

    values = flow["count"].tolist()

    import plotly.graph_objects as go

    fig4 = go.Figure(
        data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="blue",width=0.5),label=labels
            ),
            link=dict(source=source,target=target,value=values)
        )])

    fig4.update_layout(height=500)
    st.plotly_chart(fig4,use_container_width=True)

elif selected == "Data Assistant":
    st.title("Data Assistant")
    st.divider()

    st.write("Ask Questions about Dataset and get Visual Insights")
    user_question = st.chat_input("Ask your question")

    if user_question:
        q = user_question.lower()

        completed = df[df["Booking Status"]=="Completed"]

        if "total rides" in q:
            total = len(df)
            st.success(f"Total Rides in dataset : {total}")

            status = df["Booking Status"].value_counts()

            fig = px.bar(
                x=status.index,
                y=status.values,
                labels={"x":"Booking Status","y":"Ride Counts"},
                title="Ride Distribution by status"
            )

            st.plotly_chart(fig,use_container_width=True)

        elif "revenue" in q:
            revenue = completed.groupby("Vehicle Type")["Booking Value"].sum()
            st.success(f"Total Revenue {revenue.sum():,.2f}")

            fig = px.bar(
                x=revenue.index,
                y=revenue.values,
                title="Revenue By Vehicle Type",
                labels={"x":"Vehicle Type","y":"Revenue"}
            )
            st.plotly_chart(fig,use_container_width=True)

        elif "distance" in q:
            fig = px.scatter(
                completed,
                x="Ride Distance",
                y="Booking Value",
                color="Vehicle Type",
                title="Ride Distance vs Booking Value"
            )

            st.plotly_chart(fig,use_container_width=True)
            st.success(f"Average Distance {completed["Ride Distance"].mean():,.2f}")

        else:
            st.warning("Question not Recognized. Try asking about revenue, total rides, distance")
            st.divider()