import os
import json
import requests
from datetime import datetime

# Configuration
RAW_DIR = "raw"
SNAPSHOT_DIR = "snapshots"
MASTER_JSON = "master.json"

# List of target Markdown files
MD_FILES = [
    "adblockvpnguide.md", "ai.md", "android-iosguide.md", "audiopiracyguide.md",
    "beginners-guide.md", "devtools.md", "downloadpiracyguide.md", "edupiracyguide.md",
    "feedback.md", "file-tools.md", "gaming-tools.md", "gamingpiracyguide.md",
    "img-tools.md", "index.md", "internet-tools.md", "linuxguide.md", "miscguide.md",
    "non-english.md", "posts.md", "readingpiracyguide.md", "sandbox.md",
    "social-media-tools.md", "startpage.md", "storage.md", "system-tools.md",
    "text-tools.md", "torrentpiracyguide.md", "unsafesites.md", "video-tools.md",
    "videopiracyguide.md"
]

# Base raw URL for public repo raw files
RAW_BASE_URL = "https://raw.githubusercontent.com/fmhy/edit/main/docs/"

# Ensure folders exist
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# Load existing master.json if exists
if os.path.exists(MASTER_JSON):
    with open(MASTER_JSON, "r", encoding="utf-8") as f:
        master_data = json.load(f)
else:
    master_data = {"files": []}

# Helper to find a file in master_data
def find_file(filename):
    for file_obj in master_data["files"]:
        if file_obj["filename"] == filename:
            return file_obj
    return None

# Fetch each Markdown file
for md_file in MD_FILES:
    url = RAW_BASE_URL + md_file
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {md_file}")
        continue

    content = response.text.strip()
    blocks = [b for b in content.split("\n\n") if b.strip()]

    # Update or create file entry
    file_entry = find_file(md_file)
    if not file_entry:
        file_entry = {"filename": md_file, "last_updated": "", "sections": []}
        master_data["files"].append(file_entry)

    # Reuse existing section IDs if possible
    new_sections = []
    for i, block in enumerate(blocks, start=1):
        if i <= len(file_entry["sections"]):
            section_id = file_entry["sections"][i-1]["id"]
        else:
            section_id = f"sec{i}"
        new_sections.append({"id": section_id, "content": block})

    file_entry["sections"] = new_sections
    file_entry["last_updated"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M")

# Save master.json
with open(MASTER_JSON, "w", encoding="utf-8") as f:
    json.dump(master_data, f, indent=2, ensure_ascii=False)

# Daily snapshot
today = datetime.utcnow().strftime("%Y-%m-%d")
snapshot_file = os.path.join(SNAPSHOT_DIR, f"{today}.json")
with open(snapshot_file, "w", encoding="utf-8") as f:
    json.dump(master_data, f, indent=2, ensure_ascii=False)

print(f"Updated master.json and snapshot {snapshot_file}")