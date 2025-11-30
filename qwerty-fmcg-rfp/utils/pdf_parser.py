import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def parse_rfp_scope(text):
    # Simple heuristic: look for "Scope of Supply", "Quantity", "Description"
    lines = text.split("\n")
    scope_lines = []
    in_scope = False
    for line in lines:
        line = line.strip().lower()
        if "scope of supply" in line or "quantity" in line:
            in_scope = True
        if in_scope and line:
            scope_lines.append(line)
        if "technical specifications" in line or "test requirements" in line:
            break
    return "\n".join(scope_lines)

def parse_test_requirements(text):
    lines = text.split("\n")
    test_lines = []
    in_tests = False
    for line in lines:
        line = line.strip().lower()
        if "test requirements" in line or "acceptance tests" in line:
            in_tests = True
        if in_tests and line:
            test_lines.append(line)
        if "pricing" in line or "cost" in line:
            break
    return "\n".join(test_lines)
