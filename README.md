# Azure FinOps Sentinel

**Automated cost-optimization guard for your Azure subscription.**

## 🚀 Overview

Azure FinOps Sentinel is an Azure Function–based solution that continuously scans your subscription for idle or orphaned resources, generates detailed HTML reports, and sends proactive email notifications via Azure Logic Apps. It leverages managed identities for secure access and runs on a timer trigger to ensure 24/7 cost governance.

## 🔑 Key Features

- **Automated Waste Detection**  
  - Identifies VMs with average CPU utilization < 10% over 7 days  
  - Finds unattached managed disks and unassociated public IPs  
- **Proactive Tagging**  
  - Applies `FinOps-Status: Waste-Candidate-*` tags for easy filtering  
- **Professional HTML Reporting**  
  - Generates and stores detailed reports in Azure Blob Storage  
- **Instant Notifications**  
  - Triggers an Azure Logic App to send email alerts to stakeholders  
- **Secure & Scalable**  
  - Uses Azure Managed Identity—no credentials in code  
  - Built in Python with Pandas for data processing  

## 🏗️ Architecture

1. **Timer Trigger** → Azure Function (Python)  
2. Query Azure Compute, Networking, and Monitor Metrics  
3. Process results and generate HTML report  
4. Save report to Azure Blob Storage  
5. If waste detected → HTTP POST to Logic App → Email notification  

*(See `docs/architecture-diagram.png` for a visual overview.)*

## ⚙️ Prerequisites

- Azure Subscription  
- Azure CLI / PowerShell  
- Python 3.8+  
- Azure Function Core Tools  

## 🚀 Getting Started

1. Clone this repo  
   ```bash
   git clone https://github.com/your-org/azure-finops-sentinel.git
   cd azure-finops-sentinel
