Azure FinOps Sentinel
💡 Overview
Azure FinOps Sentinel is an automated, serverless solution designed to help organizations and individuals optimize their Azure cloud spending by proactively identifying and managing neglected or underutilized resources. Built as an Azure Function, this tool continuously monitors your Azure subscription for potential cost-saving opportunities, provides actionable insights, and automates reporting and notifications.

The Problem It Solves: Cloud Waste
In dynamic cloud environments, it's easy for resources to become orphaned or idle, consuming budget without providing value. Common culprits include:

Idle Virtual Machines: VMs left running 24/7 with minimal CPU utilization.

Unattached Disks: Managed disks that are no longer connected to any VM.

Unassociated Public IPs: Public IP addresses consuming costs without being linked to an active resource.

Azure FinOps Sentinel addresses this by providing automated detection, tagging, and reporting, ensuring you maintain a lean and cost-efficient cloud footprint.

✨ Features
Automated Resource Scanning: Periodically scans your Azure subscription for various types of wasted resources.

Intelligent Waste Detection:

Identifies idle Virtual Machines based on configurable average CPU utilization thresholds over a defined period (e.g., <10% CPU over 7 days).

Detects unattached Managed Disks.

Finds unassociated Public IP Addresses.

Automated Tagging: Applies a FinOps-Status: Waste-Candidate-* tag to identified resources, making them easy to track and review.

Professional HTML Reports: Generates a comprehensive and well-formatted HTML report summarizing all discovered wasted resources.

Blob Storage Integration: Automatically saves the generated HTML reports to an Azure Blob Storage container for historical tracking and easy access.

Automated Email Notifications: Triggers an Azure Logic App to send email notifications with the detailed HTML report to designated administrators.

Secure Authentication: Leverages Azure Managed Identity for secure and credential-less access to Azure resources.

Serverless & Cost-Efficient: Runs as an Azure Function, providing a highly scalable and cost-effective solution.

⚙️ How It Works (Architecture Overview)
Azure FinOps Sentinel operates as a streamlined FinOps pipeline:

Timer Trigger: An Azure Function (written in Python) is configured to run on a recurring schedule (e.g., every 6 hours).

Resource Discovery: The Function authenticates using Managed Identity and utilizes Azure SDKs to query:

Azure Compute: To list VMs and Disks.

Azure Monitor: To retrieve CPU metrics for running VMs.

Azure Networking: To list Public IP Addresses.

Waste Identification & Tagging: Based on predefined criteria, the Function identifies idle VMs, unattached disks, and unassociated IPs. It then applies appropriate FinOps-Status tags to these resources.

Report Generation: A professional HTML report is dynamically generated, summarizing all identified waste.

Storage: The HTML report is securely uploaded and stored in an Azure Blob Storage container.

Notification: If wasted resources are found, the Function triggers an Azure Logic App. The Logic App, configured with a SendGrid (or other email service) connector, sends the HTML report as an email notification to the specified recipient.

🚀 Getting Started
Follow these steps to deploy and configure Azure FinOps Sentinel in your Azure subscription.

Prerequisites
An active Azure Subscription.

Python 3.11+ installed.

Azure CLI or Azure Functions Core Tools for deployment.

Azure Storage Account for storing reports.

Azure Logic App for sending email notifications (with a configured email connector like SendGrid or Office 365 Outlook).

SendGrid Account (if using SendGrid for emails).

1. Clone the Repository
git clone https://github.com/your-username/azure-finops-sentinel.git
cd azure-finops-sentinel

2. Install Dependencies
Ensure you have a requirements.txt file in your function app root directory with the following packages:

azure-functions
azure-identity
azure-mgmt-compute
azure-mgmt-network
azure-mgmt-resource
azure-mgmt-monitor
azure-storage-blob
pandas
requests

You can install them locally for testing:

pip install -r requirements.txt

3. Deploy the Azure Function App
Deploy your Python Azure Function App to Azure using your preferred method (Azure CLI, VS Code Azure Functions extension, or Azure Portal).

4. Configure Application Settings (Environment Variables)
In your Azure Function App in the Azure Portal, navigate to Configuration > Application settings and add the following settings:

Setting Name

Description

Example Value

AZURE_SUBSCRIPTION_ID

Your Azure Subscription ID.

xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

STORAGE_ACCOUNT_NAME

The name of your Azure Storage Account where reports will be saved.

myfinopsstorage

BLOB_CONTAINER_NAME

The name of the Blob container within your storage account for reports.

reports

LOGIC_APP_URL

The HTTP POST URL for your Azure Logic App trigger.

https://prod-00.eastus.logic.azure.com/...

ADMIN_EMAIL

The email address to which FinOps reports will be sent.

your.email@example.com

IDLE_VM_CPU_THRESHOLD

(Optional) Average CPU threshold (%) for idle VMs. Default is 10.0.

5.0

IDLE_VM_TIMESPAN_DAYS

(Optional) Number of days for CPU average calculation. Default is 7.

3

Important: The finops_sentinel_function now correctly uses blob_container_name parameter, so ensure you have BLOB_CONTAINER_NAME configured in your Function App's Application Settings.

5. Configure Managed Identity & RBAC Permissions
The Azure Function needs permissions to read Azure resources and write to Blob Storage.

Enable Managed Identity:

In your Azure Function App in the Azure Portal, go to Identity (under Settings).

Enable System assigned managed identity.

Assign RBAC Roles: Assign the following roles to the Function App's Managed Identity:

Contributor (at Subscription or Resource Group scope where your resources reside): Required for scanning and tagging VMs, Disks, and Public IPs.

Storage Blob Data Contributor (on your designated Storage Account): Required to write HTML reports to the Blob container.

6. Set up Azure Blob Storage Container
Ensure you have a container named reports (or whatever you set BLOB_CONTAINER_NAME to) in your specified Azure Storage Account. If it doesn't exist, create it manually via Azure Portal: navigate to your Storage Account -> Containers -> + Container.

7. Set up Azure Logic App
Create a new Consumption Logic App in Azure Portal.

HTTP Request Trigger: Add a trigger "When an HTTP request is received". Copy the generated HTTP POST URL – this will be your LOGIC_APP_URL application setting.

JSON Schema: Provide the following JSON schema for the request body to enable dynamic content:

{
    "type": "object",
    "properties": {
        "email": {
            "type": "string"
        },
        "body": {
            "type": "string"
        }
    }
}

Send Email Action: Add an action to "Send an email" using your preferred connector (e.g., SendGrid, Office 365 Outlook).

To: Select email from the "Dynamic content" list (from the HTTP Request trigger).

Subject: Set a subject like "Azure FinOps Sentinel Report".

Body (or HTML Content): Crucially, ensure you select body from the "Dynamic content" list (from the HTTP Request trigger). Make sure the email connector's settings explicitly state that the body content is HTML. For SendGrid, this is typically done by setting "html": "@{triggerBody().body}" and "ishtml": true.

🚀 Usage
Once deployed and configured, the finops_sentinel_function will automatically run based on its timer schedule (0 0 */6 * * * means every 6 hours).

You can also manually trigger the function from the Azure Portal for testing purposes.

Expected Output
Email Notifications: You will receive a professional, well-formatted HTML report in your inbox (sent to ADMIN_EMAIL) detailing all identified wasted resources.

Blob Storage Reports: HTML report files will be saved in your designated Blob Storage container (reports).

Azure Tags: Resources identified as waste candidates will be tagged with FinOps-Status: Waste-Candidate-*.

Azure Function Logs: Detailed logs will be available in Azure Monitor / Application Insights, showing the function's execution status, discovered resources, and any errors.

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements, new waste detection patterns, or bug fixes, please open an issue or submit a pull request.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

📞 Contact
For any questions or inquiries, feel free to reach out.
