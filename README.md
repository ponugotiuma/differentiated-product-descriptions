# 🤖 Differentiated Product Descriptions

An AI-powered e-commerce application that uses **Google Gemini multimodal AI** to analyze product images and information and generate three differentiated product descriptions for different business purposes.

The system generates **SEO-focused, customer-benefit-focused, and marketplace-focused descriptions**, evaluates their quality, and provides a human review and approval workflow before the final content is exported.

---

## 📌 Overview

Creating product descriptions manually for large e-commerce catalogs can be time-consuming and difficult to maintain consistently.

This project uses **Generative AI and Multimodal AI** to automate product-description generation while keeping humans involved in the final review process.

The application accepts a product image along with optional product information and generates multiple content variations based on different objectives.

### Generated Content

* 🔍 **SEO-Focused** — optimized around relevant product information and search visibility
* 🛍️ **Customer-Benefit-Focused** — emphasizes customer value, benefits, and usability
* 🏪 **Marketplace-Focused** — provides concise and useful content suitable for e-commerce marketplaces

---

## ✨ Features

* 🖼️ Product image understanding using Gemini multimodal AI
* ✍️ AI-generated product descriptions
* 🎯 Three differentiated content strategies
* 🔍 SEO-oriented content analysis
* 📊 Product attribute coverage analysis
* 🔗 Semantic similarity analysis
* 🛡️ Factuality guidance to reduce unsupported product claims
* 👤 Human-in-the-loop review
* ✏️ Edit and regenerate descriptions
* ✅ Approve or reject generated content
* 📥 Export approved content
* 🗃️ Product and description persistence using SQLite
* 🧪 Demo mode for running the application without a live API key

---

## 🔄 Workflow

```text
Product Image + Product Information
                ↓
       Gemini Product Analysis
                ↓
      Generate 3 Descriptions
                ↓
        Quality Evaluation
                ↓
          Human Review
                ↓
       Edit / Regenerate
                ↓
        Approve / Reject
                ↓
          Final Export
```

---

## 🧠 AI Approach

This project uses multiple AI concepts:

| Concept                        | Role                                                     |
| ------------------------------ | -------------------------------------------------------- |
| **Artificial Intelligence**    | Overall intelligent application                          |
| **Generative AI**              | Generates new product descriptions                       |
| **Large Language Model (LLM)** | Understands prompts and produces natural language        |
| **Multimodal AI**              | Processes product images along with text                 |
| **Prompt Engineering**         | Controls the generation strategy and output requirements |

### AI Model

**Google Gemini**

Gemini is used for multimodal product understanding and description generation.

---

## 🏗️ Architecture

The application follows a simple AI-powered content workflow:

```text
                 USER
                  │
                  ▼
          Streamlit Interface
                  │
                  ▼
       Product Image + Details
                  │
                  ▼
          Gemini Multimodal AI
                  │
                  ▼
       Description Generation
          ┌───────┼────────┐
          ▼       ▼        ▼
        SEO    Customer  Marketplace
                Benefits
          │       │        │
          └───────┼────────┘
                  ▼
          Quality Analysis
                  │
                  ▼
            Human Review
                  │
                  ▼
          Approved Content
                  │
                  ▼
             Export
```

---

## 🛠️ Tech Stack

### Programming

* Python

### AI / Machine Intelligence

* Google Gemini API
* Generative AI
* Multimodal AI
* Large Language Models
* Prompt Engineering

### Application

* Streamlit

### Data & Storage

* SQLite
* Pandas

### Analysis

* SEO analysis
* Semantic similarity
* Product attribute coverage

### Development

* Git
* GitHub
* Python Virtual Environment
* dotenv

---

## 📁 Project Structure

```text
differentiated-product-descriptions/
│
├── ai/
├── analysis/
├── data/
├── database/
├── uploads/
├── utils/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
└── .env
```

Each component is separated based on its responsibility, making the application easier to maintain and extend.

---

## ⚙️ How It Works

### 1. Upload Product

The user uploads a product image and can provide additional product information.

### 2. Analyze Product

Gemini analyzes the available visual and textual information.

### 3. Generate Descriptions

The system generates three different descriptions based on predefined content objectives.

### 4. Evaluate Content

The generated descriptions are evaluated using multiple quality signals such as:

* SEO characteristics
* Semantic similarity
* Product attribute coverage

### 5. Human Review

The user reviews the generated content and can:

* Edit
* Regenerate
* Approve
* Reject

### 6. Export

Approved product descriptions can be exported for further use.

---

## 🎯 Target Users

This application can be useful for:

* E-commerce businesses
* Product managers
* Merchandisers
* Content teams
* Online retailers
* D2C brands
* Marketplace sellers
* Digital marketing teams
* E-commerce agencies

---

## 💡 Why This Project?

Traditional product-content creation requires considerable manual effort, especially when the same product needs different descriptions for different platforms or objectives.

This project explores how **Generative AI can be integrated into a practical business workflow**, rather than using AI only as a simple text-generation chatbot.

The focus is on:

> **Generation → Validation → Human Review → Approval**

---

## ⭐ Key Differentiation

A basic AI application might follow:

```text
Product → AI → Description
```

This project extends the workflow:

```text
Product
   ↓
Multimodal AI
   ↓
Multiple Content Variants
   ↓
Quality Analysis
   ↓
Human Review
   ↓
Approval
   ↓
Final Content
```

The main focus is therefore not just generating text, but building a **structured AI-assisted product-content workflow**.

---

## 🛡️ Factuality & Hallucination Control

Generative AI can sometimes produce information that is not supported by the provided product data.

The project addresses this by:

* Providing product information to the model
* Using the product image as an additional source
* Applying factuality-oriented prompting
* Evaluating generated content
* Keeping a human reviewer in the workflow

The system is designed to reduce unsupported product claims rather than blindly publishing AI-generated content.

---

## 🗄️ Data Storage

The application uses **SQLite** for local persistence.

The database can maintain information related to:

* Products
* Generated descriptions
* Quality analysis
* Reviews
* Approval status

This allows generated content and review information to persist between application sessions.

---

## 🧪 Demo Mode

The application supports a demo mode for testing the interface and workflow without requiring a live Gemini API request.

Configure the `.env` file according to the environment in which the application is being run.

Example:

```env
GEMINI_API_KEY=your_api_key
DEMO_MODE=false
```

**Never commit your actual API key to GitHub.**

---

## 🚀 Getting Started

### Clone the Repository

```bash
git clone <repository-url>
cd differentiated-product-descriptions
```

### Create Virtual Environment

```bash
python -m venv .venv
```
run with -- "streamlit run app.py"