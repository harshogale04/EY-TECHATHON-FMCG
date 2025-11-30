

# RFP Agentic AI System

**An Autonomous Agentic Pipeline for Government Tender Discovery and Proposal Generation**

The RFP Agentic AI System is a fully automated, multi-agent platform that discovers government RFPs, analyzes technical specifications, performs cost estimation, and generates submission-ready proposals. It is designed for manufacturers bidding on high-value tenders and enables fast, accurate, and data-driven bidding using intelligent agents.

---

## Features

* **Automated RFP Discovery** — Scans multiple government portals to fetch relevant tenders.
* **Fit Ranking Engine** — Scores and ranks tenders by relevance, feasibility, and strategic alignment.
* **Technical Specification Matching** — Achieves 90%+ matching accuracy against OEM cable catalogs.
* **Pricing & BOM Calculation** — Computes materials, testing charges, and final tender cost.
* **Automated Proposal Generation** — Produces both JSON and professional PDF output ready for submission.
* **End-to-End Agentic Workflow** — Sales Agent → Technical Agent → Pricing Agent → Main Agent.

---

## Inspiration

Government bidding is slow, manual, and error-prone. Companies lose tenders because they can’t scan all portals, match specifications quickly, or generate accurate costing on time.
Our goal was to build a **zero-human intervention system** — where AI handles discovery, analysis, pricing, and proposal creation automatically.

---

## Architecture Overview

The system uses a 4-agent pipeline, each responsible for a critical stage:

* **Sales Agent** — Scrapes portals and ranks RFPs.
* **Technical Agent** — Extracts specs and maps them to OEM products with high accuracy.
* **Pricing Agent** — Calculates BOM, testing fees, and total pricing.
* **Main Agent** — Generates final output (rfp_response.json + proposal PDF).

Each agent operates modularly with clean hand-offs, allowing fast, scalable tender processing.

---

## How We Built It

* Designed modular Python agents communicating via shared data structures (JSON).
* Implemented a specification matching engine that compares voltage, material, conductor, and insulation data.
* Built a pricing engine using structured CSV data for cable and test pricing.
* Automated proposal creation using a PDF generation module.
* Ensured reproducible, consistent outputs for demo and production scenarios.






---

## Installation & Setup

### Prerequisites

* Python 3.8+
* Required libraries from `requirements.txt`
* CSV data for product catalog and pricing

### Steps

```bash
# Clone the repository
git clone https://github.com/your-username/rfp-agentic-system.git
cd rfp-agentic-system

# Install dependencies
pip install -r requirements.txt

# Run the full agentic pipeline
python -m agents.main_agent

# Generate the final PDF
python demo_pdf_export.py
```

The system outputs the best match in a pdf format


