from typing import List, Dict

from utils.spec_matcher import SpecMatcher

class TechnicalAgent:

    """Matches RFP specs to OEM products"""

    def __init__(self, catalog_csv_path: str):
        self.name = "Technical Agent"
        self.matcher = SpecMatcher(catalog_csv_path)

    def extract_scope_from_rfp(self, rfp_text: str) -> List[Dict]:
        """Extract products from RFP scope (mocked for now)"""
        scope = [
            {
                "product_name": "1.1kV Cable 240mm²",
                "quantity": 1000,
                "voltage_rating": 1.1,
                "conductor_size": 240,
                "material": "Copper",
                "insulation_type": "XLPE",
                "core_count": 4,
                "armoring": "Steel Tape",
            },
            {
                "product_name": "0.6kV Cable 185mm²",
                "quantity": 500,
                "voltage_rating": 0.6,
                "conductor_size": 185,
                "material": "Copper",
                "insulation_type": "XLPE",
                "core_count": 3,
                "armoring": "Steel Wire",
            },
            {
                "product_name": "0.4kV Cable 50mm²",
                "quantity": 2000,
                "voltage_rating": 0.4,
                "conductor_size": 50,
                "material": "Copper",
                "insulation_type": "PVC",
                "core_count": 2,
                "armoring": "None",
            },
        ]
        return scope

    def execute(self, rfp_text: str) -> Dict:
        """Main workflow"""
        print(f"\n[{self.name}] ════════════════════════════════════════")
        print(f"[{self.name}] STARTING TECHNICAL AGENT")
        print(f"[{self.name}] ════════════════════════════════════════")

        scope = self.extract_scope_from_rfp(rfp_text)
        print(f"[{self.name}] Extracted {len(scope)} products from RFP scope")

        recommendations: Dict[str, Dict] = {}
        comparison_tables: Dict[str, str] = {}

        for product in scope:
            print(f"\n[{self.name}] Processing: {product['product_name']}")
            # Find top 3 matches
            top_matches = self.matcher.find_top_matches(product, top_k=3)
            print(f"[{self.name}] Top 3 matches found:")
            for match in top_matches:
                print(
                    f"[{self.name}] {match['rank']}. {match['sku']}: "
                    f"{match['match_score']:.1f}% match"
                )

            recommendations[product["product_name"]] = {
                "rfp_spec": product,
                "matches": top_matches,
                "selected_sku": top_matches[0]["sku"],
                "selected_match_score": top_matches[0]["match_score"],
            }

            # Generate comparison table
            table = self.matcher.generate_comparison_table(product, top_matches)
            comparison_tables[product["product_name"]] = table

        return {
            "recommendations": recommendations,
            "comparison_tables": comparison_tables,
            "total_products": len(scope),
        }
