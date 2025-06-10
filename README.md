Azure FinOps Sentinel
💡 Overview
Azure FinOps Sentinel is an automated, serverless solution for optimizing Azure cloud spending. It proactively identifies and manages neglected or underutilized resources to prevent budget waste. Built as an Azure Function, it continuously monitors your subscription, provides actionable insights, and automates reporting.

The Problem It Solves: Cloud Waste
Cloud environments often incur unnecessary costs from idle VMs, unattached disks, and unassociated public IPs. FinOps Sentinel addresses this by automating detection, tagging, and reporting, ensuring a lean and cost-efficient cloud presence.

✨ Features
Automated Resource Scanning: Periodically scans your Azure subscription for various wasted resource types.

Intelligent Waste Detection: Identifies idle VMs (based on CPU thresholds), unattached managed disks, and unassociated public IPs.

Automated Tagging: Applies FinOps-Status: Waste-Candidate-* tags for easy tracking and review.

Professional HTML Reports: Generates comprehensive HTML reports summarizing all discovered waste.

Blob Storage Integration: Automatically saves reports to Azure Blob Storage for historical tracking.

Automated Email Notifications: Triggers Azure Logic Apps to email detailed reports to administrators.

Secure Authentication: Uses Azure Managed Identity for secure, credential-less resource access.

Serverless & Cost-Efficient: Runs as a scalable, cost-effective Azure Function.

⚙️ How It Works (Architecture Overview)
Azure FinOps Sentinel operates as a streamlined FinOps pipeline:

Timer Trigger: Python Azure Function runs on a recurring schedule (e.g., every 6 hours).

Resource Discovery: Function authenticates via Managed Identity; queries Azure Compute (VMs, Disks), Monitor (VM CPU), and Networking (Public IPs).

Waste Identification & Tagging: Identifies idle VMs, unattached disks, and unassociated IPs, then applies FinOps-Status tags.

Report Generation: Dynamically generates professional HTML reports of identified waste.

Storage: HTML reports are securely uploaded to an Azure Blob Storage container.

Notification: If wasted resources are found, the Function triggers an Azure Logic App (e.g., via SendGrid) to email HTML reports to specified recipients.

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
Once deployed and configured, the finops_sentinel_function will automatically run based on its timer schedule (0 0 */6 * * * means every 6 hours). Manual triggers are available via Azure Portal for testing.

Expected Output
Email Notifications: Professional HTML reports detailing waste sent to ADMIN_EMAIL.

Blob Storage Reports: HTML reports saved to the configured Blob Storage container.

Azure Tags: Waste candidates tagged with FinOps-Status: Waste-Candidate-*.

Azure Function Logs: Detailed execution logs available in Azure Monitor/Application Insights.

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements, new waste detection patterns, or bug fixes, please open an issue or submit a pull request.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

📞 Contact
For any questions or inquiries, feel free to reach out.
