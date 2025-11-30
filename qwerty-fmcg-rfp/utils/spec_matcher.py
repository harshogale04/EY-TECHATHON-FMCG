import pandas as pd
from typing import List, Dict, Tuple
from difflib import SequenceMatcher

class SpecMatcher:
    """Matches RFP specs to OEM product catalog"""
    
    def __init__(self, catalog_csv_path: str):
        self.catalog = pd.read_csv(catalog_csv_path)
        print(f"[SpecMatcher] Loaded {len(self.catalog)} products from catalog")
    
    def calculate_exact_match(self, rfp_spec: Dict, product_row) -> Tuple[float, Dict]:
        """
        Calculate spec match using weighted scoring:
        - Mandatory (40%): voltage, conductor_size, material, insulation
        - Performance (30%): core_count, armoring, temperature
        - Certifications (20%): BIS certified (assume all have)
        - Cost (10%): within budget
        """
        
        score = 0.0
        match_details = {
            "voltage_match": False,
            "conductor_size_match": False,
            "material_match": False,
            "insulation_match": False,
            "core_count_match": False,
            "details": {}
        }
        
        # ===== MANDATORY SPECS (40% weight) =====
        mandatory_fields = [
            ("voltage_rating_kv", rfp_spec.get("voltage_rating"), float(product_row["voltage_rating_kv"])),
            ("conductor_size_mm2", rfp_spec.get("conductor_size"), float(product_row["conductor_size_mm2"])),
            ("material", rfp_spec.get("material"), product_row["material"]),
            ("insulation_type", rfp_spec.get("insulation_type"), product_row["insulation_type"]),
        ]
        
        mandatory_matches = 0
        for field_name, rfp_val, prod_val in mandatory_fields:
            if str(rfp_val).lower() == str(prod_val).lower():
                mandatory_matches += 1
                match_details["details"][field_name] = "✓ Match"
            else:
                match_details["details"][field_name] = f"✗ RFP: {rfp_val}, OEM: {prod_val}"
        
        mandatory_score = (mandatory_matches / 4) * 100
        score += 0.40 * mandatory_score
        
        # ===== PERFORMANCE SPECS (30% weight) =====
        performance_score = 85.0
        
        # Check core count (flexible matching)
        rfp_core = float(rfp_spec.get("core_count", 0))
        prod_core = float(product_row["core_count"])
        if rfp_core == prod_core:
            performance_score = 100.0
            match_details["core_count_match"] = True
        elif rfp_core > 0 and prod_core > 0:
            performance_score = 80.0  # Close match
            match_details["details"]["core_count"] = f"Close match (RFP: {rfp_core}, OEM: {prod_core})"
        
        score += 0.30 * performance_score
        
        # ===== CERTIFICATIONS (20% weight) =====
        cert_score = 100.0 if product_row["bis_certified"] == "Yes" else 70.0
        score += 0.20 * cert_score
        
        # ===== COST (10% weight) =====
        cost_score = 100.0  # Assume within budget
        score += 0.10 * cost_score
        
        return round(score, 1), match_details
    
    def find_top_matches(self, rfp_product: Dict, top_k: int = 3) -> List[Tuple]:
        """Find top-K matching SKUs from catalog"""
        
        matches = []
        
        for idx, product_row in self.catalog.iterrows():
            match_score, details = self.calculate_exact_match(rfp_product, product_row)
            
            matches.append({
                "rank": None,  # Will be set later
                "sku": product_row["product_sku"],
                "match_score": match_score,
                "details": details,
                "unit_price": float(product_row["unit_price_per_meter"]),
                "lead_time": int(product_row["lead_time_days"]),
                "voltage": float(product_row["voltage_rating_kv"]),
                "conductor_size": float(product_row["conductor_size_mm2"]),
                "material": product_row["material"],
                "insulation": product_row["insulation_type"],
                "temperature": int(product_row["temperature_rating_celsius"]),
            })
        
        # Sort by match score
        matches = sorted(matches, key=lambda x: x["match_score"], reverse=True)
        
        # Assign ranks
        for i, match in enumerate(matches[:top_k]):
            match["rank"] = i + 1
        
        return matches[:top_k]
    
    def generate_comparison_table(self, rfp_product: Dict, top_matches: List[Dict]) -> str:
        """Generate comparison table for display"""
        
        table = "\n┌─────────┬──────────────────────┬────────────┬─────────────────┐\n"
        table += "│ Rank    │ OEM SKU              │ SPEC MATCH │ Key Specs       │\n"
        table += "├─────────┼──────────────────────┼────────────┼─────────────────┤\n"
        
        for match in top_matches:
            specs_str = f"{match['voltage']}kV, {match['conductor_size']}mm²"
            rank_mark = "✓" if match["rank"] == 1 else " "
            table += f"│ {match['rank']} {rank_mark}      │ {match['sku'][:20]:20} │ {match['match_score']:6.1f}%  │ {specs_str:15} │\n"
        
        table += "└─────────┴──────────────────────┴────────────┴─────────────────┘\n"
        return table
