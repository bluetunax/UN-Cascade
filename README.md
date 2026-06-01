# 🌊 UN Cascade

**An Open-Source Intelligence (OSINT) tool for tracking international aid flows from global donors to local NGO implementers.**

UN Cascade pulls live financial data from the United Nations' internal reporting architecture. It allows researchers, journalists, and data analysts to track the "Donor-to-Delivery Pipeline"—visualizing how billions of dollars flow from sovereign governments, into massive UN agencies, and eventually shatter into micro-grants for local Non-Governmental Organizations (NGOs).

---

## Key Features

*   **Macro Visualization:** Automatically generates dark-mode Sankey flow charts (via Plotly) mapping the aggregate capital flows between major governments and UN agencies (e.g., USA ➔ WFP).
*   **The Implementer Ledger:** Explicitly filters UN datasets to isolate downstream funding to local and international NGOs. 
*   **Drill-Down Project Tracking:** Click on any specific NGO to view a localized ledger of their reported project activities, dates, and funding channels.
*   **Offline Snapshots:** UN API data changes, and records are occasionally scrubbed. UN Cascade utilizes a local SQLite database to silently create immutable, timestamped snapshots of every search you perform. You can reload these snapshots instantly without pinging the UN servers.

## Data Architecture & Methodology

Data is sourced directly from the **UN OCHA Financial Tracking Service (FTS) API** (HPC Tools v1).

1.  **The Source (Macro):** Sovereign Wealth / Member States appropriate funds.
2.  **The Switchboard (Meso):** The UN Agencies (OCHA, UNDP, UNICEF) receive and allocate the funds.
3.  **The Implementers (Micro):** ECOSOC NGOs, local charities, and private vendors who actually execute the work on the ground.

*Disclaimer: FTS relies on voluntary reporting from UN member states and agencies. Some downstream implementing partner data may be delayed, aggregated, or anonymized due to operational security concerns in conflict zones.*

---

## 💻 Installation & Setup

This project uses **Conda** to manage Python dependencies, ensuring a stable environment for data processing and visualization.

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/un-cascade.git
cd un-cascade
