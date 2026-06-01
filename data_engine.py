# /data_engine.py

import requests

def get_macro_flows(country_code="UKR", year="2023"):
    """Pulls top-level funding (Donors -> UN Agencies)."""
    url = f"https://api.hpc.tools/v1/public/fts/flow?countryISO3={country_code}&year={year}"
    response = requests.get(url)
    
    if response.status_code != 200: return []
    flows = response.json().get('data', {}).get('flows', [])
    
    parsed_flows = []
    for f in flows:
        try:
            amount = f.get('amountUSD', 0)
            if amount == 0: continue
            
            source = f.get('sourceObjects', [{}])[0].get('name', 'Unknown Source')
            dest_obj = f.get('destinationObjects', [{}])[0]
            destination = dest_obj.get('name', 'Unknown Destination')
            
            # We only want MACRO flows here (to UN Agencies, Governments, or Funds)
            org_type = str(dest_obj.get('organizationTypes', '')).lower()
            if 'ngo' not in org_type:
                parsed_flows.append({
                    "donor": source,
                    "agency": destination,
                    "amount": amount,
                    "date": f.get('date', 'Unknown')[:10]
                })
        except: continue
            
    return sorted(parsed_flows, key=lambda x: x['amount'], reverse=True)

def get_micro_flows(country_code="UKR", year="2023"):
    """Pulls ground-level funding (UN Agencies/Donors -> Local NGOs)."""
    url = f"https://api.hpc.tools/v1/public/fts/flow?countryISO3={country_code}&year={year}"
    response = requests.get(url)
    
    if response.status_code != 200: return []
    flows = response.json().get('data', {}).get('flows', [])
    
    micro_flows = []
    for f in flows:
        try:
            amount = f.get('amountUSD', 0)
            if amount == 0: continue
            
            dest_obj = f.get('destinationObjects', [{}])[0]
            org_type = str(dest_obj.get('organizationTypes', '')).lower()
            
            # Filter specifically for NGOs! (This is your ECOSOC target list)
            if 'ngo' in org_type or 'red cross' in org_type:
                source = f.get('sourceObjects', [{}])[0].get('name', 'UN Pooled Fund')
                
                # Tag it as Local vs International based on UN metadata
                ngo_type = "Local/National NGO" if 'national' in org_type else "International NGO"
                
                micro_flows.append({
                    "donor": source, # Usually a UN agency passing the money down
                    "ngo": dest_obj.get('name', 'Unknown NGO'),
                    "amount": amount,
                    "type": ngo_type
                })
        except: continue
            
    return sorted(micro_flows, key=lambda x: x['amount'], reverse=True)

def get_ngo_activities(ngo_name, country_code, year):
    """Pulls specific project descriptions and activities for a single NGO."""
    url = f"https://api.hpc.tools/v1/public/fts/flow?countryISO3={country_code}&year={year}"
    response = requests.get(url)
    
    if response.status_code != 200: return []
    flows = response.json().get('data', {}).get('flows', [])
    
    activities = []
    for f in flows:
        try:
            dest_obj = f.get('destinationObjects', [{}])[0]
            destination = dest_obj.get('name', '')
            
            # Check if this flow went to our target NGO
            if destination.lower() == ngo_name.lower():
                amount = f.get('amountUSD', 0)
                if amount == 0: continue
                
                source = f.get('sourceObjects', [{}])[0].get('name', 'Unknown Donor')
                date = f.get('date', 'Unknown')[:10]
                
                # Extract the project description or fallback to flow description
                description = f.get('description', 'No specific activity description provided by UN.')
                
                # Check if it's tied to a specific project code
                project_obj = f.get('projectObjects', [{}])
                project_name = project_obj[0].get('name', 'General/Core Funding') if project_obj else 'General/Core Funding'
                
                activities.append({
                    "donor": source,
                    "amount": amount,
                    "date": date,
                    "project": project_name,
                    "description": description
                })
        except: continue
            
    return sorted(activities, key=lambda x: x['date'], reverse=True)