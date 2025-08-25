import os
import json
import requests
from datetime import datetime

RAW_MD_BASE = "https://raw.githubusercontent.com/fmhy/edit/main/docs/"
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

MASTER_JSON = "master.json"
SNAPSHOT_DIR = "snapshots"

os.makedirs(SNAPSHOT_DIR, exist_ok=True)

def fetch_md(filename):
    url = RAW_MD_BASE + filename
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        print(f"Failed to fetch {filename}: {r.status_code}")
        return ""

def split_blocks(content):
    blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
    sections = []
    for i, block in enumerate(blocks):
        sections.append({"id": f"sec{i+1}", "content": block})
    return sections

def load_master():
    if os.path.exists(MASTER_JSON):
        with open(MASTER_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {"files": []}

def save_master(master):
    with open(MASTER_JSON, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=2)

def update_master():
    master = load_master()
    master_files = {f["filename"]: f for f in master["files"]}

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M")

    for md in MD_FILES:
        content = fetch_md(md)
        sections = split_blocks(content)
        if md in master_files:
            master_files[md]["sections"] = sections
            master_files[md]["last_updated"] = now
        else:
            master_files[md] = {
                "filename": md,
                "last_updated": now,
                "sections": sections
            }

    master["files"] = list(master_files.values())
    save_master(master)

def save_snapshot():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    snapshot_file = os.path.join(SNAPSHOT_DIR, f"{today}.json")
    with open(MASTER_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(snapshot_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    update_master()
    save_snapshot()
