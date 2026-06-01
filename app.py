# /app.py

from flask import Flask, render_template, request
from data_engine import get_macro_flows, get_micro_flows, get_ngo_activities
from db_manager import init_db, save_snapshot, get_snapshot, get_all_sessions
import plotly.graph_objects as go
import plotly.utils
import json

app = Flask(__name__)

# Initialize the local SQLite database when the app starts
init_db()

def create_sankey_chart(flows):
    """Converts our tabular data into a Sankey Flow Chart"""
    # Grab the top 25 flows so the chart doesn't get too messy
    top_flows = flows[:25] 
    
    # 1. Create a unique list of all "Nodes" (Donors and Agencies)
    nodes = []
    for f in top_flows:
        if f['donor'] not in nodes: nodes.append(f['donor'])
        if f['agency'] not in nodes: nodes.append(f['agency'])
        
    # 2. Create the links between Donors and Agencies
    source_indices = [nodes.index(f['donor']) for f in top_flows]
    target_indices = [nodes.index(f['agency']) for f in top_flows]
    values = [f['amount'] for f in top_flows]
    
    # 3. Build the Plotly Figure
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15, thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = nodes,
            color = "#3b82f6" # Updated to brighter UN Blue for dark mode
        ),
        link = dict(
            source = source_indices,
            target = target_indices,
            value = values,
            color = "rgba(59, 130, 246, 0.3)" # Transparent brighter blue
        )
    )])
    
    # Update layout for Dark Mode compatibility
    fig.update_layout(
        title_text="Top Financial Flows", 
        font_size=12, 
        height=500,
        template="plotly_dark",               # Forces Dark Mode text/lines
        paper_bgcolor='rgba(0,0,0,0)',        # Makes background transparent
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # Return it as JSON so the HTML page can render it
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@app.route('/')
def home():
    # Grab all past sessions to display on the homepage
    sessions = get_all_sessions()
    return render_template('index.html', sessions=sessions)

@app.route('/cascade')
def cascade():
    # Check if the user clicked a specific past session
    session_id = request.args.get('session_id')
    
    if session_id:
        # --- OFFLINE MODE ---
        snapshot = get_snapshot(session_id)
        if not snapshot:
            return "Session snapshot not found.", 404
            
        country = snapshot['country']
        year = snapshot['year']
        macro_data = snapshot['macro_data']
        micro_data = snapshot['micro_data']
        timestamp = snapshot['timestamp']
        is_offline = True
        
    else:
        # --- LIVE API MODE ---
        country = request.args.get('country', 'UKR').upper()
        year = request.args.get('year', '2023')
        
        # Pull fresh data from UN servers
        macro_data = get_macro_flows(country_code=country, year=year)
        micro_data = get_micro_flows(country_code=country, year=year)
        
        # Save a silent offline snapshot
        save_snapshot(country, year, macro_data, micro_data)
        
        timestamp = "Just Now"
        is_offline = False
    
    # Generate charts and totals (works identically for live and offline data)
    sankey_json = create_sankey_chart(macro_data) if macro_data else None
    total_funding = sum([item['amount'] for item in macro_data])
    
    return render_template(
        'dashboard.html', 
        country=country, 
        year=year, 
        flows=macro_data[:20], 
        micro_flows=micro_data[:30], 
        total=total_funding,
        sankey_json=sankey_json,
        is_offline=is_offline,
        timestamp=timestamp
    )

@app.route('/ngo')
def ngo_drilldown():
    # Grab the parameters passed from the clicked link
    ngo_name = request.args.get('name', 'Unknown NGO')
    country = request.args.get('country', 'UKR').upper()
    year = request.args.get('year', '2023')
    
    # Run our specific data function (Currently remains Live API only)
    activities = get_ngo_activities(ngo_name, country, year)
    
    # Calculate the specific total for this NGO
    total_received = sum([item['amount'] for item in activities])
    
    return render_template(
        'ngo.html',
        ngo_name=ngo_name,
        country=country,
        year=year,
        activities=activities,
        total=total_received
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)