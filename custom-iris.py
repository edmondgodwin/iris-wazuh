#!/usr/bin/env python3
# custom-iris.py
# Custom Wazuh integration script to send alerts to DFIR-IRIS

import sys
import json
import requests
from requests.auth import HTTPBasicAuth

# Function to create a formatted string from alert details
def format_alert_details(alert_json):
    rule = alert_json.get("rule", {})
    agent = alert_json.get("agent", {})
    data = alert_json.get("data", {})

    # Extracting MITRE information from the nested 'rule' structure
    mitre = rule.get("mitre", {})
    mitre_ids = ', '.join(mitre.get("id", ["N/A"]))
    mitre_tactics = ', '.join(mitre.get("tactic", ["N/A"]))
    mitre_techniques = ', '.join(mitre.get("technique", ["N/A"]))


    details = [
        f"Rule ID: {rule.get('id', 'N/A')}",
        f"Rule Level: {rule.get('level', 'N/A')}",
        f"Rule Description: {rule.get('description', 'N/A')}",
        f"Agent ID: {agent.get('id', 'N/A')}",
        f"Agent IP: {agent.get('ip', 'N/A')}",
        f"Agent Name: {agent.get('name', 'N/A')}",
        f"Source IP: {data.get('srcip', 'N/A')}",
        f"Source Port: {data.get('srcport', 'N/A')}",
        f"Source User: {data.get('srcuser', 'N/A')}",
        f"MITRE IDs: {mitre_ids}",
        f"MITRE Tactics: {mitre_tactics}",
        f"MITRE Techniques: {mitre_techniques}",
        f"Location: {alert_json.get('location', 'N/A')}",
        f"Full Log: {alert_json.get('full_log', 'N/A')}",
        f"Timestamp: {alert_json.get('timestamp', 'N/A')}",
        f"PCIDSS: {rule.get('pci_dss', 'N/A')}"
    ]
    return '\n'.join(details)

# Read parameters when integration is run
alert_file = sys.argv[1]
api_key = sys.argv[2]
hook_url = sys.argv[3]

# Read the alert file
with open(alert_file) as f:
    alert_json = json.load(f)

# Prepare alert details
alert_details = format_alert_details(alert_json)

# Convert Wazuh rule levels(0-15) -> IRIS severity(1-6)
alert_level = alert_json.get("rule", {}).get("level")
if(alert_level < 5):
    severity = 2
elif(alert_level >= 5 and alert_level < 7):
    severity = 3
elif(alert_level >= 7 and alert_level < 10):
    severity = 4
elif(alert_level >= 10 and alert_level < 13):
    severity = 5
elif(alert_level >= 13):
    severity = 6
else:
    severity = 1

# Generate request
payload = json.dumps({
    "alert_title": alert_json.get("rule", {}).get("description", "No Description"),
    "alert_description": alert_details,
    "alert_source": "Wazuh",
    "alert_source_ref": alert_json.get("id", "Unknown ID"),
    "alert_source_link": "https://wazuh-ip-or-url",  # Replace with actual Wazuh URL
    "alert_severity_id": severity,
    "alert_status_id": 2,  # 'New' status
    "alert_source_event_time": alert_json.get("timestamp", "Unknown Timestamp"),
    "alert_note": "",
    "alert_tags": f"wazuh,{alert_json.get('agent', {}).get('name', 'N/A')}",
    "alert_customer_id": 2,  # '1' for default 'IrisInitialClient'
    "alert_source_content": alert_json  # raw log
})

# Send request to IRIS
response = requests.post(hook_url, verify=False, data=payload, headers={"Authorization": "Bearer " + api_key, "content-type": "application/json"})

sys.exit(0)