import argparse
import os
import requests
import time

# Load .env from script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")
if os.path.exists(ENV_PATH):
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip("'\"")

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
EMAIL_TO = os.environ.get("RESEND_EMAIL_TO", "")

# Section codes to watch for WL opening (n/a → number)
WATCH_CODES = {"34330", "34331", "34332"}

params = {
    "year": "2026",
    "quarter": "Spring",
    "department": "COMPSCI",
    "courseNumber": "175",
}

def fetch_sections():
    r = requests.get("https://anteaterapi.com/v2/rest/websoc", params=params)
    data = r.json()
    sections = []
    for school in data.get("data", {}).get("schools", []):
        for dept in school.get("departments", []):
            for course in dept.get("courses", []):
                for sec in course.get("sections", []):
                    sections.append(sec)
    return sections

def is_wl_numeric(val):
    if val is None or val == "" or str(val).lower() == "n/a":
        return False
    try:
        int(val)
        return True
    except (ValueError, TypeError):
        return False

def send_email(subject: str, body: str):
    if not RESEND_API_KEY or not EMAIL_TO:
        print("(Set RESEND_API_KEY and RESEND_EMAIL_TO in .env to enable email alerts)")
        return False
    try:
        r = requests.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {RESEND_API_KEY}"},
            json={
                "from": "onboarding@resend.dev",
                "to": EMAIL_TO,
                "subject": subject,
                "text": body,
            },
        )
        if r.status_code == 200:
            print("(Email sent)")
            return True
        print(f"(Email failed {r.status_code}: {r.text})")
        return False
    except Exception as e:
        print(f"(Email failed: {e})")
        return False

def main(args):
    prev_wl = {c: None for c in WATCH_CODES}
    while True:
        sections = fetch_sections()
        for sec in sections:
            sc = sec.get("sectionCode")
            if sc not in WATCH_CODES:
                continue
            wl = sec.get("numOnWaitlist")
            was_numeric = is_wl_numeric(prev_wl.get(sc))
            now_numeric = is_wl_numeric(wl)
            if not was_numeric and now_numeric:
                msg = f"COMPSCI 175 section {sec.get('sectionNum')} (code {sc}) waitlist opened: WL = {wl}"
                print(f"\n*** {msg} ***\n")
                send_email("COMPSCI 175: Waitlist opened", msg)
            prev_wl[sc] = wl

        # Print current state (no Req) with section codes, sorted by section
        print("\nCOMPSCI 175")
        for sec in sorted(sections, key=lambda s: (s.get("sectionNum", ""), s.get("sectionCode", ""))):
            enrolled = sec.get("numCurrentlyEnrolled", {}).get("totalEnrolled", "-")
            wl_val = sec.get("numOnWaitlist") or "-"
            code = sec.get("sectionCode", "")
            print(f"  {sec.get('sectionNum', ''):4} ({code:5}) | Max:{sec.get('maxCapacity', '-'):>3} Enr:{enrolled:>3} WL:{wl_val:>3} | {sec.get('status', '-')}")

        if args.once:
            break
        time.sleep(60)  # poll every 60 seconds

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run once, no polling")
    args = parser.parse_args()
    main(args)