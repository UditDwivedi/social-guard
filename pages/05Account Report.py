import streamlit as st
import os
import pandas as pd
import altair as alt

# Path to the CSV file
csv_file_path = "Accountreport.csv"

# Check if the file exists
if not os.path.exists(csv_file_path):
    st.write("No Report Found. Please Start New Analysis.")
    
    # Wrap the submit button in a form
    with st.form(key='request_analysis_form'):
        submitted = st.form_submit_button("Request Analysis")
        
        if submitted:
            st.switch_page("pages/01Request Analysis.py")
else:
    # Load the CSV file
    df = pd.read_csv(csv_file_path)
    st.title("Account Report")
    st.header("Account Analysis Report")
    st.write(df)




    if True:  
        c = st.multiselect(
            "Choose Status", ["Red", "Green", "Yellow"], ["Red", "Green"]
        )

        # If no status is selected, show an error message
        if not c:
            st.error("Please select at least one status.")
        else:
            # Filter the data based on the selected statuses
            data = df[df['Status'].isin(c)]

            # Display the filtered data as a table
            st.subheader("Filtered Data")


            # Prepare data for charting
            # Count the occurrences of each status
            status_counts = data['Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            color_scale = alt.Scale(domain=["Red", "Green", "Yellow"], range=["red", "green", "Yellow"])


            # Create an Altair chart to visualize the counts of each status
            chart = (
                alt.Chart(status_counts)
                .mark_bar()
                .encode(
                    x="Status:N",  # X-axis: Status (categorical)
                    y="Count:Q",   # Y-axis: Count (quantitative)
                    color=alt.Color("Status:N", scale=color_scale),  # Apply color scale
                )
            )

            # Display the chart in the Streamlit app
            st.altair_chart(chart, use_container_width=True)

red_data = df[df['Status'] == "Red"]
            
            # Display the filtered "Red" accounts
st.subheader("Termination Accounts")
st.write(red_data)

            # Save the filtered "Red" accounts to a CSV file for termination
terminate_file_path = "terminate.csv"
red_data.to_csv(terminate_file_path, index=False)
st.write(f"Red accounts saved to {terminate_file_path}")