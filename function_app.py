import logging
import os
import pandas as pd
import requests
import json
from datetime import datetime, timedelta, timezone
import azure.functions as func

# --- Configuration Constants ---
IDLE_VM_CPU_THRESHOLD = 10.0
IDLE_VM_TIMESPAN = timedelta(days=7)

app = func.FunctionApp()

@app.schedule(schedule="0 0 */6 * * *", arg_name="myTimer", run_on_startup=True) 
def finops_sentinel_function(myTimer: func.TimerRequest) -> None:
    logging.info('Azure FinOps Sentinel automation triggered.')
    
    try:
        from azure.identity import DefaultAzureCredential
        from azure.mgmt.compute import ComputeManagementClient
        from azure.mgmt.network import NetworkManagementClient
        from azure.mgmt.resource import ResourceManagementClient
        from azure.mgmt.monitor import MonitorManagementClient

        logging.info("Authenticating with Azure Managed Identity...")
        credential = DefaultAzureCredential()
        subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
        storage_account_name = os.environ.get("STORAGE_ACCOUNT_NAME")

        if not all([subscription_id, storage_account_name]):
            logging.error("CRITICAL: Required App Settings are not set.")
            return

        # Initialize clients
        compute_client = ComputeManagementClient(credential, subscription_id)
        network_client = NetworkManagementClient(credential, subscription_id)
        resource_client = ResourceManagementClient(credential, subscription_id)
        monitor_client = MonitorManagementClient(credential, subscription_id)

        wasted_resources = {
            "Idle Virtual Machines": find_and_tag_idle_vms(compute_client, monitor_client, resource_client),
            "Unattached Disks": find_and_tag_unattached_disks(compute_client, resource_client),
            "Unassociated Public IPs": find_and_tag_unassociated_ips(network_client, resource_client)
        }
        
        # Build the professional HTML report using pandas
        html_report, total_found = build_html_report(wasted_resources)
        
        # If resources were found, save the report and send a notification
        if total_found > 0:
            # Step 1: Save the report to Blob Storage
            save_html_report_to_blob(html_report, storage_account_name, credential)
            
            # Step 2: Send a notification via Logic App
            logic_app_url = os.environ.get("LOGIC_APP_URL")
            admin_email = os.environ.get("ADMIN_EMAIL")
            if logic_app_url and admin_email:
                send_notification_to_logic_app(html_report, logic_app_url, admin_email)
            else:
                logging.warning("LOGIC_APP_URL or ADMIN_EMAIL not set. Skipping notification.")
        else:
            logging.info("No wasted resources found to report.")

        logging.info('Function execution finished successfully.')

    except Exception as e:
        logging.error(f"A critical error occurred: {e}", exc_info=True)


def build_html_report(found_data):
    """Helper function to generate a professional, well-styled HTML content for the report using pandas."""
    report_date = datetime.now(timezone.utc)
    total_found = sum(len(v) for v in found_data.values())

    # --- Start of HTML content ---
    html_body = f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; max-width: 800px; margin: auto; border: 1px solid #e0e0e0; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        <div style="background-color: #0078D4; color: white; padding: 25px; text-align: center; border-top-left-radius: 10px; border-top-right-radius: 10px;">
            <h1 style="margin: 0; font-size: 28px;">🛡️ Azure FinOps Sentinel Report</h1>
            <p style="margin: 8px 0 0; font-size: 14px;">{report_date.strftime('%B %d, %Y at %H:%M UTC')}</p>
        </div>
        <div style="padding: 30px;">
            <div style="background-color: #fff4e5; border-left: 5px solid #ff9800; padding: 20px; margin-bottom: 30px; border-radius: 5px;">
                <h2 style="margin-top: 0; font-size: 20px; color: #c05f00;">🚨 Summary: {total_found} Potential Issues Found</h2>
                <p style="margin-bottom: 0;">The automated scan has detected and tagged the following resources for your review. No resources have been deleted.</p>
            </div>
    """
    resource_map = {
        "Idle Virtual Machines": {"icon": "🖥️", "columns": ["VM Name", "Resource Group", "Avg CPU %"]},
        "Unattached Disks": {"icon": "💾", "columns": ["Disk Name", "Resource Group"]},
        "Unassociated Public IPs": {"icon": "🌐", "columns": ["IP Name", "Resource Group"]}
    }
    
    for resource_type, data in found_data.items():
        map_info = resource_map.get(resource_type)
        html_body += f'<h2 style="font-size: 18px; border-bottom: 2px solid #0078D4; padding-bottom: 5px; margin-top: 30px;">{map_info["icon"]} {resource_type} ({len(data)})</h2>'
        
        if data:
            df = pd.DataFrame(data, columns=map_info["columns"])
            # Use pandas to create the HTML table, adding our custom class
            html_body += df.to_html(index=False, border=0, classes='resource-table')
        else:
            html_body += '<p style="color: #4CAF50;">✅ No issues found in this category.</p>'
        html_body += "<hr style='border: none; border-top: 1px solid #eee; margin: 20px 0;'>"

    html_body += """
        </div>
        <div style="background-color: #f8f9fa; color: #888; padding: 20px; text-align: center; font-size: 12px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;">
            <p style="margin: 0;">This is an automated report from Azure FinOps Sentinel.</p>
        </div>
    </div>
    """

    # Final HTML template with embedded CSS for email clients
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>FinOps Report</title>
    <style>
        .resource-table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 15px;
            font-size: 14px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        .resource-table thead tr {{
            background-color: #005a9e;
            color: #ffffff;
            text-align: left;
        }}
        .resource-table th, .resource-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #dddddd;
        }}
        .resource-table tbody tr:nth-of-type(even) {{
            background-color: #f3f3f3;
        }}
        .resource-table tbody tr:hover {{
            background-color: #e8f4fd;
        }}
    </style>
    </head>
    <body style='background-color: #f4f4f4; padding: 20px;'>
        {html_body}
    </body>
    </html>
    """
    return html_template, total_found

def save_html_report_to_blob(html_report, storage_account_name, credential):
    """Saves the generated HTML report to a blob container."""
    from azure.storage.blob import BlobServiceClient, ContentSettings
    logging.info("Attempting to save HTML report to blob storage...")
    try:
        blob_service_client = BlobServiceClient(
            account_url=f"https://{storage_account_name}.blob.core.windows.net",
            credential=credential
        )
        container_name = "finops-reports"
        report_date = datetime.now(timezone.utc)
        blob_name = f"FinOps-Report-{report_date.strftime('%Y-%m-%d-%H%M')}.html"
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        html_content_settings = ContentSettings(content_type='text/html')
        blob_client.upload_blob(html_report, overwrite=True, content_settings=html_content_settings)
        logging.info(f"Successfully saved report to '{container_name}/{blob_name}'.")
    except Exception as e:
        logging.error(f"Failed to save report to blob storage: {e}", exc_info=True)


def send_notification_to_logic_app(html_report, logic_app_url, admin_email):
    """Sends the HTML report to a Logic App trigger."""
    logging.info("Attempting to send report to Logic App...")
    payload = {"email": admin_email, "body": html_report}
    try:
        response = requests.post(logic_app_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        if 200 <= response.status_code < 300:
            logging.info("Successfully triggered Logic App for email notification.")
        else:
            logging.error(f"Failed to trigger Logic App. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logging.error(f"An error occurred while calling the Logic App: {e}", exc_info=True)

# --- (All other helper functions like apply_tag, find_and_tag_..., get_vm_average_cpu remain the same) ---
def apply_tag(resource_client, resource_id, api_version, tag_value):
    try:
        resource = resource_client.resources.get_by_id(resource_id, api_version)
        tags = resource.tags or {}
        if tags.get('FinOps-Status') == tag_value: return True
        tags['FinOps-Status'] = tag_value
        resource.tags = tags
        resource_client.resources.begin_create_or_update_by_id(resource_id, api_version, resource).result()
        logging.info(f"Successfully tagged: {resource.name}")
        return True
    except Exception as e:
        logging.error(f"Error tagging {resource_id.split('/')[-1]}: {e}")
        return False

def find_and_tag_unattached_disks(compute_client, resource_client):
    logging.info("Scanning for Unattached Disks...")
    tagged = []
    api_version = '2024-03-02'
    for disk in compute_client.disks.list():
        if disk.managed_by is None and apply_tag(resource_client, disk.id, api_version, "Waste-Candidate-Disk"):
            tagged.append([disk.name, disk.id.split('/')[4]])
    return tagged

def find_and_tag_unassociated_ips(network_client, resource_client):
    logging.info("Scanning for Unassociated Public IPs...")
    tagged = []
    api_version = '2023-11-01'
    for ip in network_client.public_ip_addresses.list_all():
        if ip.ip_configuration is None and apply_tag(resource_client, ip.id, api_version, "Waste-Candidate-IP"):
            tagged.append([ip.name, ip.id.split('/')[4]])
    return tagged

def find_and_tag_idle_vms(compute_client, monitor_client, resource_client):
    logging.info("Scanning for Idle VMs...")
    tagged = []
    api_version = '2024-03-01'
    for vm in compute_client.virtual_machines.list_all():
        try:
            vm_details = compute_client.virtual_machines.get(vm.id.split('/')[4], vm.name, expand='instanceView')
            is_running = any(status.code == 'PowerState/running' for status in (vm_details.instance_view.statuses or []))
            if is_running:
                avg_cpu = get_vm_average_cpu(monitor_client, vm.id)
                if avg_cpu is not None and avg_cpu < IDLE_VM_CPU_THRESHOLD:
                    if apply_tag(resource_client, vm.id, api_version, "Waste-Candidate-Idle-VM"):
                        tagged.append([vm.name, vm.id.split('/')[4], f"{avg_cpu:.2f}%"])
        except Exception as e:
            logging.error(f"Could not get details for VM {vm.name}. Error: {e}")
    return tagged
        
def get_vm_average_cpu(monitor_client, vm_resource_id):
    try:
        end_time = datetime.now(timezone.utc)
        start_time = end_time - IDLE_VM_TIMESPAN
        timespan = f"{start_time.strftime('%Y-%m-%dT%H:%M:%SZ')}/{end_time.strftime('%Y-%m-%dT%H:%M:%SZ')}"
        metrics = monitor_client.metrics.list(vm_resource_id, timespan=timespan, interval='P1D', metricnames='Percentage CPU', aggregation='Average')
        series = metrics.value[0].timeseries[0].data
        return sum(m.average for m in series if m.average is not None) / len(series) if series else 0.0
    except Exception as e:
        logging.warning(f"Could not get CPU metrics for {vm_resource_id.split('/')[-1]}: {e}")
        return None


@app.timer_trigger(schedule="0 0 */6 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def timer_trigger10(myTimer: func.TimerRequest) -> None:
    
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')