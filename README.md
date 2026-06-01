# 🌊 UN Cascade

**An Open-Source Intelligence (OSINT) tool for tracking international aid flows from global donors to local NGO implementers.**

UN Cascade pulls live financial data from the United Nations' internal reporting architecture. It allows researchers, journalists, and data analysts to track the "Donor-to-Delivery Pipeline"—visualizing how billions of dollars flow from sovereign governments, into massive UN agencies, and eventually shatter into micro-grants for local Non-Governmental Organizations (NGOs).

---

## 🚀 Key Features

*   **Macro Visualization:** Automatically generates dark-mode Sankey flow charts (via Plotly) mapping the aggregate capital flows between major governments and UN agencies (e.g., USA ➔ WFP).
*   **The Implementer Ledger:** Explicitly filters UN datasets to isolate downstream funding to local and international NGOs. 
*   **Drill-Down Project Tracking:** Click on any specific NGO to view a localized ledger of their reported project activities, dates, and funding channels.
*   **Offline Snapshots:** UN API data changes, and records are occasionally scrubbed. UN Cascade utilizes a local SQLite database to silently create immutable, timestamped snapshots of every search you perform. You can reload these snapshots instantly without pinging the UN servers.

## 🏗️ Data Architecture & Methodology

Data is sourced directly from the **UN OCHA Financial Tracking Service (FTS) API** (HPC Tools v1).

1.  **The Source (Macro):** Sovereign Wealth / Member States appropriate funds.
2.  **The Switchboard (Meso):** The UN Agencies (OCHA, UNDP, UNICEF) receive and allocate the funds.
3.  **The Implementers (Micro):** ECOSOC NGOs, local charities, and private vendors who actually execute the work on the ground.

*Disclaimer: FTS relies on voluntary reporting from UN member states and agencies. Some downstream implementing partner data may be delayed, aggregated, or anonymized due to operational security concerns in conflict zones.*

---

## 💻 Installation & Setup

You can set up UN Cascade using either **Conda** (Recommended for data environments) or standard **Pip/venv**.

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/un-cascade.git
cd un-cascade
```

### 2. Install Dependencies

**Option A: Using Conda (Recommended)**
Uses the provided `environment.yml` file to create an isolated environment.
```bash
conda env create -f environment.yml
conda activate un-cascade
```

**Option B: Using standard Pip / Virtualenv**
Uses the provided `requirements.txt` file.
```bash
# Create and activate a virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Create and activate a virtual environment (Mac/Linux)
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```
*The app will automatically initialize the local `sessions.db` SQLite database on its first run.*

Open your browser and navigate to: **http://127.0.0.1:5000**

---

## 🗺️ File Structure

```text
un_cascade/
│
├── app.py                  # Main Flask application and routing
├── data_engine.py          # UN API worker (Macro, Micro, and NGO specific pulls)
├── db_manager.py           # SQLite engine for the Offline Snapshot system
├── environment.yml         # Conda dependencies
├── requirements.txt        # Pip dependencies
│
├── static/
│   └── style.css           # Dark-mode Bloomberg-terminal style CSS
│
└── templates/
    ├── index.html          # Search interface and Snapshot History
    ├── dashboard.html      # Sankey chart and Macro/Micro data tables
    └── ngo.html            # Drill-down ledger for specific NGO activities
```

---

## 🕵️‍♂️ Usage Example

1. Open the app and enter a crisis code (e.g., **UKR** for Ukraine, **SDN** for Sudan, **SYR** for Syria) and a reporting year (e.g., **2023**).
2. Click **Trace Funds (Live API)**.
3. View the top-level Sankey chart to see which global superpowers are funding which UN agencies.
4. Scroll down to **Step 2: The Micro Layer** and click on an implementing NGO (e.g., *Save the Children* or *Ukrainian Red Cross*).
5. Review the specific project descriptions tied to that NGO. 
6. Click **Back to Search**. You will now see your search saved locally in the **🗄️ Local Offline Snapshots** table. Clicking it will load the data instantly from your local SQLite ledger.

---
*Built for financial transparency and humanitarian aid traceability.*
