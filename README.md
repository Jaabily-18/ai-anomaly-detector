# ai-anomaly-detector
Real-time tabular anomaly detection agent using IQR statistics, Google Gemini AI root-cause analysis, and automated email alerts.

## ⚡ Features

* **Universal CSV Ingestion**: Upload any CSV file and pick any numerical metric to evaluate.
* **IQR Statistical Detection**: Uses Tukey's Fences ($1.5 \times \text{IQR}$) to detect extreme spikes or drops without manual rule-writing.
* **Interactive Visuals**: Line charts and anomaly markers built with Plotly.
* **AI Plain-English Diagnosis**: Integrated with `gemini-3.6-flash` to explain what happened, common reasons why, and immediate action steps.
* **Automated Email Dispatch**: Sends diagnostic summaries directly to team members via Gmail SMTP.

---

## 🛠️ Tech Stack

* **Frontend**: Streamlit, Plotly
* **Data Processing**: Pandas
* **AI & LLM**: Google Gemini API (`gemini-3.6-flash`)
* **Alerting**: Python `smtplib`
