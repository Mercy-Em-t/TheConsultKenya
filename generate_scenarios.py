import os
import re

source_path = r"C:\Users\user\.gemini\antigravity\brain\e0785799-9ab0-47a7-a3f9-bcc5223b70ff\PHASE_8_REQUIREMENTS_SPECS_ASSUMPTIONS_SCENARIOS.md"
with open(source_path, "r", encoding="utf-8") as f:
    text = f.read()

sections = re.findall(r'(### (UC-\d\d):[^\n]+.*?)(?=\n### UC-|\n## Master Scenario|\Z)', text, re.DOTALL)
print(f"Found {len(sections)} UC sections.")

os.makedirs("scenarios", exist_ok=True)
for sec_text, uc_id in sections:
    clean_id = uc_id.replace("-", "")
    fname = os.path.join("scenarios", f"SC_{clean_id}.md")
    with open(fname, "w", encoding="utf-8") as sf:
        sf.write(f"# Scenario & Jackson-Zave Specification: {uc_id}\n\n" + sec_text.strip() + "\n")

print(f"Successfully generated {len(sections)} scenario files.")

# Generate index for scenarios
index_path = os.path.join("scenarios", "INDEX.md")
with open(index_path, "w", encoding="utf-8") as idxf:
    idxf.write("# Master Scenario Directory Index\n\n")
    idxf.write("Contains all 22 Jackson-Zave triadic specifications and realistic narrative scenarios.\n\n")
    idxf.write("| Use Case ID | Scenario File | Persona | Focus |\n| :--- | :--- | :--- | :--- |\n")
    for sec_text, uc_id in sections:
        clean_id = uc_id.replace("-", "")
        # Extract persona from scenario line
        p_match = re.search(r'\*Context:\*\s*([^,]+)', sec_text)
        persona = p_match.group(1).strip() if p_match else "Stakeholder"
        idxf.write(f"| **{uc_id}** | [`SC_{clean_id}.md`](file:///c:/Users/user/Documents/KenyaConsult/scenarios/SC_{clean_id}.md) | {persona} | Jackson-Zave Triad & Operational Scenario |\n")

print("Created scenarios/INDEX.md successfully.")
