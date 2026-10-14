import os

use_cases_dir = r"c:\Users\user\Documents\KenyaConsult\use_cases"
files = [f for f in os.listdir(use_cases_dir) if f.startswith("UC-")]
files.sort()

index_file = os.path.join(use_cases_dir, "INDEX.md")
brain_artifact_file = r"C:\Users\user\.gemini\antigravity\brain\e0785799-9ab0-47a7-a3f9-bcc5223b70ff\PHASE_2_USE_CASE_ANALYSIS_AND_EVENT_TABLE.md"

# Read current content and replace links
with open(index_file, "r", encoding="utf-8") as f:
    text = f.read()

# Build mapping of UC-ID to actual filename
mapping = {}
for f in files:
    ucid = f.split("_")[0]
    mapping[ucid] = f

# Replace table links in markdown
lines = text.split("\n")
new_lines = []
for line in lines:
    if line.startswith("| **UC-") and "[`UC-" in line:
        ucid = line.split("**")[1]
        if ucid in mapping:
            actual_f = mapping[ucid]
            # Replace markdown link
            # format: | **UC-01** | [`filename`](file:///c:/Users/user/Documents/KenyaConsult/use_cases/filename) | ...
            parts = line.split("|")
            parts[2] = f" [`{actual_f}`](file:///c:/Users/user/Documents/KenyaConsult/use_cases/{actual_f}) "
            new_lines.append("|".join(parts))
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

updated_content = "\n".join(new_lines)
with open(index_file, "w", encoding="utf-8") as f:
    f.write(updated_content)

with open(brain_artifact_file, "w", encoding="utf-8") as f:
    f.write(updated_content)

print(f"Updated index links for {len(mapping)} use cases.")
