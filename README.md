# 💰 Azure FinOps Sentinel — Intelligent Cloud Cost Optimization

![Azure](https://img.shields.io/badge/Azure-Cloud-blue?logo=microsoftazure\&logoColor=white)
![Python](https://img.shields.io/badge/Python-DarkBlue?logo=python\&logoColor=white)
![Serverless](https://img.shields.io/badge/Serverless-Yes-lightgrey)
![Automation](https://img.shields.io/badge/Automation-Enabled-green)

---

## 🌟 Project Overview

**Azure FinOps Sentinel** is a **fully serverless FinOps governance solution** on **Azure**, designed to **detect under-utilized resources** and **optimize cloud spend** automatically.

It ensures **zero-credential drift** using Managed Identities and provides **real-time HTML reporting** to stakeholders through Azure Logic Apps.

---

## 🚀 Key Achievements

* 🛠 Developed a **Python Azure Function** that scans every 6 hours for:

  * VMs with <10% CPU over 7 days
  * Unattached disks
  * Unused IPs
* 🏷 Automated tagging (`FinOps-Status`) for governance.
* 📊 HTML reporting pipeline archives reports to **Azure Blob Storage** and notifies stakeholders via **Logic Apps**.
* 🔍 Identified and remediated **50+ waste candidates** in the first week.

---

## 🏗️ Architecture Overview

| Component                 | Description                                    |
| ------------------------- | ---------------------------------------------- |
| **Azure Functions**       | Serverless automation tasks                    |
| **Azure Blob Storage**    | Archive HTML reports                           |
| **Azure Logic Apps**      | Real-time notifications to stakeholders        |
| **Terraform & Azure CLI** | Infrastructure provisioning and automation     |
| **Managed Identity**      | Secure access with zero hard-coded credentials |
| **Lifecycle Management**  | Automated cleanup of unused resources          |

### Architecture Diagram

![Workflow](bd681a09-3742-41d1-8cff-6ef3b302d898.png "Azure FinOps Workflow")
*Figure: Serverless automation and cost optimization workflow*

---

## ⚙️ Tech Stack

| Category       | Tools & Services                                                            |
| -------------- | --------------------------------------------------------------------------- |
| **Cloud**      | Microsoft Azure (Functions, Blob Storage, Logic Apps, Lifecycle Management) |
| **Language**   | Python                                                                      |
| **Serverless** | Azure Functions                                                             |
| **Automation** | Terraform, Azure CLI, Logic Apps                                            |
| **Focus**      | Cloud Security, FinOps / Cost Management                                    |

---

## 🔧 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Azure-FinOps-Sentinel.git
cd Azure-FinOps-Sentinel
```

### 2️⃣ Deploy Infrastructure

```bash
terraform init
terraform plan
terraform apply
```

### 3️⃣ Run Sentinel Function

```bash
pip install -r requirements.txt
func start
```

### 4️⃣ View Reports

* Reports stored in **Azure Blob Storage**
* Notifications sent via **Azure Logic Apps**

---

## 📊 Performance Highlights

* ✅ Automated detection and tagging of unused resources
* ✅ Real-time reporting and notifications

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Please **fork** this repo and submit a **pull request**.

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Amr Amer**
🌐 [LinkedIn](https://www.linkedin.com/in/amr-amer) • 💻 [GitHub](https://github.com/ammr102)
