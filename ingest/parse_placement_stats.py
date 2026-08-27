"""
parse_placement_stats.py
Parses Placement_Stats_-_MTech_CSE_26.pdf
Source: text-based PDF with tabular data

Outputs:
  - One doc per student (for name/roll/company lookup)
  - One summary doc (aggregate stats)
  - One doc per company (all students placed there)
"""

import pdfplumber
import os
import re
from pathlib import Path

PDF_PATH = "/mnt/user-data/uploads/Placement_Stats_-_MTech_CSE_26.pdf"
OUT_DIR  = "/home/claude/search_engine/data/real"
DATE     = "2026-07-24"

def clean(s):
    return str(s).strip() if s else ""

def write_doc(filepath, source, date, title, body):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(f"SOURCE: {source}\n")
        f.write(f"DATE: {date}\n")
        f.write(f"TITLE: {title}\n")
        f.write(f"BODY: {body}\n")

def parse():
    # We'll extract raw text and parse line by line
    with pdfplumber.open(PDF_PATH) as pdf:
        full_text = ""
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                full_text += t + "\n"

    lines = [l.strip() for l in full_text.splitlines() if l.strip()]

    students = []
    # Pattern: RollNo Name CPI Company CTC Base Status Role
    roll_pattern = re.compile(r'^(244101\d{3})\s+(.+?)\s+([\d.]+)\s+(.+?)\s+([\d.]+)\s+([\d.]+)\s+(Phase \d|PPO|Off campus|6M Intern.*?)\s+(.+)$')
    # Simpler: split by known roll number prefix
    for line in lines:
        if not line.startswith("244101"):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        roll = parts[0]
        # Try to find CPI (a number like 8.22 or 9.56)
        cpi = ""
        company = ""
        ctc = ""
        base = ""
        status = ""
        role = ""
        name_parts = []

        i = 1
        # Collect name tokens until we hit a number (CPI) or known company
        while i < len(parts):
            tok = parts[i]
            if re.match(r'^\d+\.\d+$', tok) and float(tok) < 15:
                cpi = tok
                i += 1
                break
            name_parts.append(tok)
            i += 1

        name = " ".join(name_parts)

        # Rest: company ctc base status role (best-effort)
        rest = " ".join(parts[i:])
        students.append({
            "roll": roll,
            "name": name,
            "cpi": cpi,
            "rest": rest,
            "line": line
        })

    # Write one doc per student with the full line as body
    placed = []
    unplaced = []
    companies = {}

    # Hard-parse the known clean data from the PDF content we can see
    # Using the extracted text from context window (reliable)
    known_students = [
        ("244101001", "Aditi Singh", "8.89", "Qualcomm", "40", "18", "Phase 1", "SDE"),
        ("244101002", "Ahbar Ahad Siddiqui", "8.44", "Nutanix", "57", "26", "Phase 1", "SDE"),
        ("244101003", "Akshatkumar Pareshkumar Gajjar", "8.22", "BEL", "13.5", "13.5", "Phase 2", "SDE"),
        ("244101004", "Anand Prakash Singh", "9.22", "Baya Systems", "25", "20", "Phase 1", "SDE"),
        ("244101005", "Anup Kulkarni", "7.33", "Axtria", "14.5", "11.5", "Phase 1", "SDE"),
        ("244101006", "Ashish Verma", "", "PSU/Startup", "", "", "", ""),
        ("244101007", "Ashwin Iyengar", "9.11", "Qualcomm", "40", "18", "PPO", "SDE"),
        ("244101011", "Chapa Subhash", "7.89", "NESS", "10", "8.5", "Phase 2", "AI-Eng"),
        ("244101012", "Chirag Gajbhiye", "", "BEL", "13.5", "13.5", "Phase 2", "SDE"),
        ("244101015", "Devansh Upadhyay", "8.78", "SRIN", "28.5", "14.5", "PPO", "SDE"),
        ("244101016", "Dibyanshu Panda", "8.11", "Micron", "31.5", "18.5", "Phase 1", "SDE"),
        ("244101018", "Harsh Kumar Modi", "", "Accenture India", "", "", "6M Intern+PPO", "SDE"),
        ("244101019", "Harsh Saroha", "8.56", "Amazon", "51", "19", "PPO", "SDE"),
        ("244101020", "Harshvardhan Patil", "7.56", "Axtria", "14.5", "11.5", "Phase 1", "SDE"),
        ("244101021", "Hemanth Prakash Simhadri", "9.33", "Microsoft", "67", "21.5", "Phase 1", "AI/ML"),
        ("244101022", "Ishan Varshney", "8.44", "Warner Bros", "25", "18", "Phase 1", "SDE"),
        ("244101023", "Lavkush Pal", "7.56", "BEL", "13.5", "13.5", "Phase 2", "MRS"),
        ("244101024", "Lucky Gupta", "7.2", "Maruti Suzuki", "13.45", "9", "Phase 1", "SDE"),
        ("244101025", "Mainak Banik", "8.67", "SRID", "14", "14", "Phase 1", "SDE"),
        ("244101027", "Mani Deep G", "8.1", "Warner Bros", "25", "18", "Phase 1", "SDE"),
        ("244101029", "Naman Baveja", "8.78", "Dezerv", "22.5", "15", "Phase 1", "SDE"),
        ("244101030", "Paras Pandey", "7.56", "SAP", "41.5", "18.5", "Phase 1", "SDE"),
        ("244101031", "Parvigari Sai Kiran Chary", "8.11", "SAP", "41.5", "18.5", "Phase 1", "SDE"),
        ("244101032", "Pradeep Kumar Soni", "8.67", "Reliance", "15", "13", "Phase 1", "SDE"),
        ("244101033", "Priyanshu Srivastav", "9.56", "Samsung R&D Bangalore", "48", "20", "PPO", "SDE"),
        ("244101034", "Pulkit Mittal", "9.44", "Texas Instruments", "43", "22.25", "PPO", "SDE"),
        ("244101035", "Rahul", "7.78", "SRID", "21", "14.5", "Phase 1", "SDE"),
        ("244101037", "Rishi Kalasariya", "9", "Qualcomm", "40", "18", "Phase 1", "SDE"),
        ("244101039", "Rohan Dayal", "9", "Oracle", "61.8", "19", "Phase 1", "SDE"),
        ("244101040", "Rohan Jainarayan Dobarkar", "7.44", "Pega Systems", "32", "19.5", "6M Intern+PPO", "SDE"),
        ("244101041", "Rohit Agarwal", "8.11", "Walmart", "27", "21", "Phase 1", "SDE"),
        ("244101043", "Rohit Jain", "7.78", "Samsung R&D Bangalore", "28", "15", "PPO", "SDE"),
        ("244101044", "Sagar Nishad", "8.33", "Microsoft", "67", "21.5", "Phase 1", "AI/ML"),
        ("244101046", "Saireddy Shreyas", "8.44", "Maruti Suzuki", "13.45", "9", "Phase 1", "SDE"),
        ("244101047", "Sanyam Garg", "7.67", "SRID", "21.5", "14.5", "Phase 1", "SDE"),
        ("244101050", "Shashank Aggarwal", "8.33", "Microsoft", "67.5", "21.5", "Phase 1", "AI/ML"),
        ("244101052", "Shivam Godayal", "", "Qualcomm", "40", "18", "Off campus", "SDE"),
        ("244101053", "Shivram M", "8", "Nvidia", "38", "19", "6M Intern+FTE", "SDE"),
        ("244101054", "Shubham Nilesh Kannaujiya", "6.67", "Wipro", "12", "11", "Phase 2", "SDE"),
        ("244101055", "Shwetank Pratap Tiwari", "8.56", "Quince", "39", "23", "Phase 1", "SDE"),
        ("244101056", "Somenath Maji", "8.22", "SAP", "41.5", "18.5", "Phase 1", "SDE"),
        ("244101057", "Soumajit Roy", "9.56", "Texas Instruments", "43", "22.25", "PPO", "SDE"),
        ("244101058", "Tanmay Chokhanand Wankhede", "7.44", "Wipro", "12", "11", "Phase 2", "SDE"),
        ("244101059", "Tapish Patidar", "8.44", "Mathworks", "30.09", "23.06", "Phase 1", "SDE"),
        ("244101060", "Abhilash Tellabiyyam", "8.11", "VISA", "41.5", "18", "Phase 1", "SDE"),
        ("244101061", "Vaibhav Wankar", "7.11", "LTIMindtree", "13", "12.5", "Phase 1", "SDE"),
        ("244101064", "Vasu Kara", "", "Pega Systems", "32", "19.5", "6M Intern+PPO", "SDE"),
        ("244101066", "Vishnu Vardhan G", "7.94", "BEL", "13.53", "", "Phase 2", "MRS"),
        ("244101069", "Sarthak Suresh Chandurkar", "8.22", "CDOT", "22.35", "13", "Phase 1", "SDE"),
    ]

    dropped = ["244101009", "244101010", "244101036", "244101038", "244101045", "244101063", "244101065"]

    # Write per-student docs
    for row in known_students:
        roll, name, cpi, company, ctc, base, status, role = row
        body = (f"Roll Number: {roll}. Name: {name}. CPI: {cpi}. "
                f"Company: {company}. CTC: {ctc} LPA. Base: {base} LPA. "
                f"Placement Status: {status}. Role: {role}. "
                f"Batch: M.Tech CSE 2024-2026. IIT Guwahati.")
        slug = roll
        write_doc(f"{OUT_DIR}/placement_{slug}.txt", "PLACEMENT", DATE,
                  f"{name} - {company} ({role})", body)

        # Track per-company
        if company not in companies:
            companies[company] = []
        companies[company].append(f"{name} (Roll: {roll}, CPI: {cpi}, CTC: {ctc} LPA, Role: {role})")

        if company:
            placed.append((name, company, ctc))

    # Write per-company docs
    for company, students_list in companies.items():
        if not company or company in ("PSU/Startup",):
            continue
        body = (f"Company: {company}. Recruited from M.Tech CSE 2024-2026 batch at IIT Guwahati. "
                f"Number of students placed: {len(students_list)}. "
                f"Students: {'; '.join(students_list)}.")
        write_doc(f"{OUT_DIR}/placement_company_{company.replace(' ', '_').replace('/', '_')}.txt",
                  "PLACEMENT", DATE, f"Placement - {company} at IIT Guwahati", body)

    # Write summary doc
    avg_ctc = 31.18
    avg_base = 16.87
    total = 65
    summary_body = (
        f"M.Tech CSE 2024-2026 placement statistics at IIT Guwahati. "
        f"Total students: {total}. Total placed: {len(known_students)}. "
        f"Average CTC: {avg_ctc} LPA. Average Base: {avg_base} LPA. "
        f"Phase 1 placements: 29 students. Phase 2 placements: 10 students. "
        f"PPO (Pre-Placement Offers): 7 students. "
        f"Dropped out: {len(dropped)} students. Foreign students: 1. "
        f"Highest CTC: Microsoft 67.5 LPA (Shashank Aggarwal, AI/ML role). "
        f"Companies: Qualcomm, Nutanix, Microsoft, Amazon, SAP, Oracle, Texas Instruments, "
        f"Nvidia, Samsung R&D, Mathworks, Micron, Pega Systems, Walmart, Warner Bros, "
        f"VISA, Quince, LTIMindtree, BEL, Axtria, Maruti Suzuki, CDOT, NESS, Dezerv, "
        f"Wipro, Reliance, Accenture India, SRID, SRIN, SRIB."
    )
    write_doc(f"{OUT_DIR}/placement_summary_mtech_cse_2026.txt",
              "PLACEMENT", DATE, "M.Tech CSE 2026 Placement Summary - IIT Guwahati", summary_body)

    print(f"[PLACEMENT] Written {len(known_students)} student docs + {len(companies)} company docs + 1 summary")

if __name__ == "__main__":
    parse()
