import os
import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai
from dotenv import load_dotenv
from email_alert import send_alert_email

# Load API keys from .env
load_dotenv()

st.set_page_config(page_title="AI Data Monitor", layout="wide")
st.title("Anomaly Detection & Business Insight Agent")

api_key = st.secrets.get("GEMINI_API_KEY") if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Initialize session memory for AI insights
if "ai_insights" not in st.session_state:
    st.session_state["ai_insights"] = ""

# 1. File Uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.subheader("Raw Data Preview")
    st.dataframe(df.head(5))

    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
    
    if numeric_columns:
        target_col = st.selectbox("Select metric to analyze:", numeric_columns)
        
        # 2. IQR Anomaly Detection Logic
        q25 = df[target_col].quantile(0.25)
        q75 = df[target_col].quantile(0.75)
        iqr = q75 - q25
        
        lower_bound = q25 - (1.5 * iqr)
        upper_bound = q75 + (1.5 * iqr)
        
        anomalies = df[(df[target_col] < lower_bound) | (df[target_col] > upper_bound)]
        
        # 3. KPI Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", len(df))
        col2.metric("Anomalies Detected", len(anomalies))
        col3.metric("Normal Range", f"{lower_bound:.2f} to {upper_bound:.2f}")
        
        # 4. Interactive Plotly Line Chart (Safe Index Handling)
        df_plot = df.reset_index()
        x_axis = "Date" if "Date" in df.columns else "index"
        
        fig = px.line(
            df_plot, 
            x=x_axis, 
            y=target_col, 
            title=f"Distribution & Outlier Plot for {target_col}",
            labels={"index": "Student Record / Row #"}
        )
        
        if not anomalies.empty:
            anomalies_plot = anomalies.reset_index()
            fig.add_scatter(
                x=anomalies_plot[x_axis],
                y=anomalies_plot[target_col],
                mode="markers",
                marker=dict(color="red", size=8),
                name="Anomaly"
            )
        st.plotly_chart(fig, use_container_width=True)
        
        # 5. Flagged Records Table & AI Section
        if not anomalies.empty:
            st.warning(f"⚠️ {len(anomalies)} Outlier(s) Detected:")
            st.dataframe(anomalies)
            
            st.markdown("---")
            st.subheader("💡 AI Placement / Metric Analysis")
            
            if st.button("Generate Executive Insights with Gemini"):
                with st.spinner("Analyzing anomalies with Gemini..."):
                    # Sample up to 10 anomalies for Gemini prompt to avoid token overflow on large datasets
                    sample_anomalies = anomalies.head(10)[[target_col]].to_string()
                    
                    prompt = f"""
                    You are a pragmatic institutional analyst reviewing student placement and readiness performance metrics.
                    We analyzed the metric '{target_col}'.
                    The standard expected range is between {lower_bound:.2f} and {upper_bound:.2f}.
                    
                    A total of {len(anomalies)} records fell outside this expected range.
                    Here is a sample of the flagged values:
                    {sample_anomalies}
                    
                    Explain what this indicates in plain, conversational language.
                    
                    Structure your answer with these clear sections:
                    1. What Caught Our Attention: Explain what these extreme high or low scores mean for this cohort.
                    2. Practical Reasons: 2-3 realistic explanations for why these specific outliers exist in student data.
                    3. Recommended Next Steps: 2-3 practical actions placement officers or faculty should take regarding these students.
                    """
                    
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )
                    
                    st.session_state["ai_insights"] = response.text
            
            if st.session_state["ai_insights"]:
                st.success("Analysis Ready!")
                st.write(st.session_state["ai_insights"])
                
                st.markdown("---")
                st.subheader("Send Alert to Team")
                recipient = st.text_input("Enter recipient email address:")
                
                if st.button("Send Alert Email"):
                    if recipient:
                        with st.spinner("Sending email..."):
                            success = send_alert_email(recipient, target_col, st.session_state["ai_insights"])
                            if success:
                                st.success(f"Alert sent successfully to {recipient}!")
                            else:
                                st.error("Failed to send email. Check your .env credentials.")
                    else:
                        st.warning("Please provide a recipient email address.")
        else:
            st.success(f"✅ All {len(df)} records are within standard bounds ({lower_bound:.2f} to {upper_bound:.2f}). No outliers found!")
            st.session_state["ai_insights"] = ""
    else:
        st.error("No numeric columns found in this file.")
