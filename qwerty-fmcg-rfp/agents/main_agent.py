# agents/main_agent.py (COMPLETE FIXED VERSION)
import json
from datetime import datetime
from typing import List, Dict
import sys
import os
sys.path.append('.')

from agents.sales_agent import SalesAgent
from agents.technical_agent import TechnicalAgent
from agents.pricing_agent import PricingAgent

class MainAgent:
    """Orchestrates entire RFP workflow"""
    
    def __init__(self, catalog_csv: str = "data/products/product_catalog.csv", 
                 product_prices_csv: str = "data/products/product_catalog.csv", 
                 test_prices_csv: str = "data/pricing/test_prices.csv"):
        self.name = "Main Agent (Orchestrator)"
        self.catalog_csv = catalog_csv
        self.product_prices_csv = product_prices_csv
        self.test_prices_csv = test_prices_csv
        
        # Initialize agents with correct paths
        self.sales_agent = SalesAgent()
        self.technical_agent = TechnicalAgent(catalog_csv)
        self.pricing_agent = PricingAgent(product_prices_csv, test_prices_csv)
        
        print(f"[{self.name}] ✅ Initialized with:")
        print(f"   📁 Catalog: {catalog_csv}")
        print(f"   💰 Pricing: {product_prices_csv}")
        print(f"   🧪 Tests: {test_prices_csv}")
    
    def run_full_workflow(self):
        """Main orchestration workflow - NO INPUT NEEDED"""
        
        print("\n" + "=" * 80)
        print("🚀 RFP AGENTIC AI SYSTEM - COMPLETE WORKFLOW")
        print("=" * 80)
        
        # Step 1: Sales Agent - Find & rank RFPs
        print("\n>>> STEP 1: SALES AGENT - Identify & Rank RFPs")
        top_rfps = self.sales_agent.scan_portals()
        selected_rfp = top_rfps[0]  # Top ranked RFP
        print(f"🎯 SELECTED: {selected_rfp['title']} (Fit: {selected_rfp['fit_score']}%)")
        
        # Step 2: Technical Agent - Match specs
        print("\n>>> STEP 2: TECHNICAL AGENT - Match Specs to OEM Products")
        # Pass RFP title as text (mock PDF content)
        technical_result = self.technical_agent.execute(selected_rfp['title'])
        
        # Print top matches
        print(f"\n[{self.name}] Top recommendations:")
        for product_name, rec in technical_result["recommendations"].items():
            top_match = rec["matches"][0]
            print(f"   {product_name} → {top_match['sku']} ({top_match['match_score']}%)")
        
        # Step 3: Pricing Agent - Calculate costs
        print("\n>>> STEP 3: PRICING AGENT - Calculate Costs")
        pricing_result = self.pricing_agent.execute(technical_result)
        
        # Step 4: Consolidate & Save
        print("\n>>> STEP 4: MAIN AGENT - Consolidate Response")
        final_response = self.consolidate_response(selected_rfp, technical_result, pricing_result)
        
        # Save & Display
        self.save_response(final_response)
        self.display_summary(final_response)
        
        return final_response
    
    def consolidate_response(self, rfp: Dict, technical: Dict, pricing: Dict) -> Dict:
        """Consolidate all results"""
        return {
            "rfp_id": rfp.get("id", "N/A"),
            "project_name": rfp.get("title", "N/A"),
            "client_name": rfp.get("client", "N/A"),
            "due_date": rfp.get("due_date", "N/A"),
            "strategic_fit_score": rfp.get("fit_score", 0),
            "rfp_value": rfp.get("value", "N/A"),
            "technical_recommendations": technical["recommendations"],
            "pricing_summary": {
                "material_cost": pricing["material_cost"],
                "test_cost": pricing["test_cost"],
                "grand_total": pricing["grand_total"]
            },
            "status": "Ready for Review ✓",
            "generated_at": datetime.now().isoformat()
        }
    
    def save_response(self, response: Dict):
        """Save to JSON"""
        with open("rfp_response.json", "w") as f:
            json.dump(response, f, indent=2, default=str)
        print(f"\n[{self.name}] ✓ Response saved to: rfp_response.json")
    
    def display_summary(self, response: Dict):
        """Display final summary"""
        print("\n" + "=" * 80)
        print("📋 FINAL RFP RESPONSE SUMMARY")
        print("=" * 80)
        print(f"🎯 RFP: {response['project_name']}")
        print(f"🏢 Client: {response['client_name']}")
        print(f"📅 Due: {response['due_date']}")
        print(f"⭐ Strategic Fit: {response['strategic_fit_score']:.0f}%")
        print(f"\n💰 Material Cost: ₹{response['pricing_summary']['material_cost']:,.0f}")
        print(f"🧪 Test Cost: ₹{response['pricing_summary']['test_cost']:,.0f}")
        print(f"💎 GRAND TOTAL: ₹{response['pricing_summary']['grand_total']:,.0f}")
        print(f"\n✅ Status: {response['status']}")
        print("=" * 80)

# Test runner
if __name__ == "__main__":
    main = MainAgent()
    result = main.run_full_workflow()
