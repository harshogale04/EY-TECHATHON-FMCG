import pandas as pd
from typing import List, Dict

class PricingAgent:

    """Calculates costs"""

    def __init__(self, product_prices_csv: str, test_prices_csv: str):
        self.name = "Pricing Agent"
        self.product_prices = pd.read_csv(product_prices_csv)
        self.test_prices = pd.read_csv(test_prices_csv)
        print(f"[{self.name}] Loaded pricing tables")

    def calculate_material_cost(self, sku: str, quantity: float) -> float:
        """Calculate material cost"""
        # Find unit price
        row = self.product_prices[self.product_prices["product_sku"] == sku]
        if not row.empty:
            unit_price = float(row.iloc[0]["unit_price_per_meter"])  # Fixed iloc usage
            return unit_price * quantity
        return 0

    def calculate_test_cost(self, quantity: float) -> Dict:
        """Calculate test costs"""
        # Mandatory tests
        mandatory_tests = self.test_prices[self.test_prices["mandatory"] == "Yes"]

        test_breakdown = {}
        total_test_cost = 0

        for _, test_row in mandatory_tests.iterrows():
            test_type = test_row["test_type"]
            test_cost = float(test_row["unit_cost_rupees"])
            test_breakdown[test_type] = test_cost
            total_test_cost += test_cost

        return {
            "itemized": test_breakdown,
            "total": total_test_cost
        }

    def execute(self, technical_recommendations: Dict) -> Dict:
        """Main workflow"""
        print(f"\n[{self.name}] ════════════════════════════════════════")
        print(f"[{self.name}] STARTING PRICING AGENT")
        print(f"[{self.name}] ════════════════════════════════════════")

        detailed_pricing = []
        total_material_cost = 0

        # Calculate test costs once (shared across all products)
        test_costs = self.calculate_test_cost(quantity=1)  # quantity not needed here for test, kept for signature
        total_test_cost = test_costs["total"]

        for product_name, rec in technical_recommendations["recommendations"].items():
            sku = rec["selected_sku"]
            quantity = rec["rfp_spec"]["quantity"]
            # Calculate material cost
            material_cost = self.calculate_material_cost(sku, quantity)
            total_material_cost += material_cost

            unit_price = self.product_prices[self.product_prices["product_sku"] == sku]
            unit_price = float(unit_price.iloc[0]["unit_price_per_meter"]) if not unit_price.empty else 0

            detailed_pricing.append({
                "product": product_name,
                "sku": sku,
                "quantity": quantity,
                "unit_price": unit_price,
                "material_cost": material_cost
            })

            print(f"[{self.name}] {product_name}")
            print(f"[{self.name}] SKU: {sku}")
            print(f"[{self.name}] Quantity: {quantity}m")
            print(f"[{self.name}] Material Cost: ₹{material_cost:,.0f}")

        grand_total = total_material_cost + total_test_cost

        print(f"\n[{self.name}] ════════════════════════════════════════")
        print(f"[{self.name}] COST SUMMARY:")
        print(f"[{self.name}] Material Cost: ₹{total_material_cost:,.0f}")
        print(f"[{self.name}] Test Cost: ₹{total_test_cost:,.0f}")
        print(f"[{self.name}] GRAND TOTAL: ₹{grand_total:,.0f}")
        print(f"[{self.name}] ════════════════════════════════════════")

        return {
            "detailed_pricing": detailed_pricing,
            "material_cost": total_material_cost,
            "test_cost": total_test_cost,
            "test_breakdown": test_costs,
            "grand_total": grand_total
        }
