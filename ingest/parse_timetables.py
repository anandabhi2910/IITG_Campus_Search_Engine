"""
parse_timetables.py
Parses TIMETABLE_JULY_NOV26.pdf (CSE dept) and 1st_year_undergraduate_timetable_classroom.pdf
Outputs: one doc per course, one doc per slot, one summary per programme
"""

import os

OUT_DIR = "/home/claude/search_engine/data/real"
DATE = "2026-07-23"

def write_doc(filepath, source, date, title, body):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(f"SOURCE: {source}\n")
        f.write(f"DATE: {date}\n")
        f.write(f"TITLE: {title}\n")
        f.write(f"BODY: {body}\n")

# Slot → Day+Time mapping (from timetable grid)
SLOT_MAP = {
    "A":  "Monday 7:55-8:50, Tuesday 9:00-9:55, Wednesday 10:00-10:55, Thursday 11:00-11:55",
    "B":  "Monday 9:00-9:55, Tuesday -, Wednesday -, Thursday -, Friday 7:55-8:50",
    "C":  "Monday 10:00-10:55, Tuesday -, Wednesday -, Thursday 7:55-8:50, Friday 9:00-9:55",
    "D":  "Monday 11:00-11:55, Tuesday -, Wednesday 7:55-8:50, Thursday 9:00-9:55, Friday 10:00-10:55",
    "E":  "Tuesday 7:55-8:50, Wednesday 9:00-9:55, Thursday 10:00-10:55",
    "F":  "Monday 12:00-12:55, Tuesday 12:00-12:55, Wednesday 12:00-12:55, Thursday -, Friday 12:00-12:55",
    "G":  "Wednesday 12:00-12:55, Thursday 12:00-12:55, Friday 12:00-12:55",
    "A1": "Monday 4:00-4:55, Tuesday 3:00-3:55, Wednesday 3:00-3:55, Thursday 2:00-2:55",
    "B1": "Monday 3:00-3:55, Wednesday -, Thursday -, Friday 4:00-4:55",
    "C1": "Monday 2:00-2:55, Tuesday 2:00-2:55, Wednesday -, Thursday -",
    "D1": "Monday 2:00-2:55 (alt), Tuesday -, Wednesday -, Friday 3:00-3:55",
    "E1": "Tuesday 4:00-4:55, Wednesday 4:00-4:55, Thursday 3:00-3:55, Friday 5:00-5:55",
    "F1": "Monday 1:00-1:55, Tuesday 1:00-1:55, Thursday -, Friday 2:00-2:55",
    "G1": "Wednesday 1:00-1:55, Thursday 1:00-1:55, Friday 1:00-1:55",
    "ML1": "Monday 9:00-11:55 (lab)",
    "ML2": "Tuesday 9:00-11:55 (lab)",
    "ML3": "Wednesday 9:00-11:55 (lab)",
    "ML4": "Thursday 9:00-11:55 (lab)",
    "ML5": "Friday 9:00-11:55 (lab)",
    "AL1": "Monday 2:00-5:00 (lab)",
    "AL2": "Tuesday 2:00-5:00 (lab)",
    "AL3": "Wednesday 2:00-5:00 (lab)",
    "AL4": "Thursday 2:00-5:00 (lab)",
    "AL5": "Friday 2:00-5:00 (lab)",
}

def slot_time(slot):
    return SLOT_MAP.get(slot.strip(), slot)

def parse():
    # ── MTech CSE 1st Sem Courses ──────────────────────────────────────────────
    mtech_1st = [
        ("CS5001", "Design and Analysis of Algorithms", "3-0-0-6", "Sushanta Karmakar", "B", "B1", "5G4"),
        ("CS5002L", "Data Structures Lab", "0-2-2-6", "R Inkulu", "ML5", "B (Friday)", "5101"),
        ("CS5003", "Mathematics for Computer Science", "3-0-0-6", "P. Bhaduri", "A", "A1", "5403"),
    ]

    for code, name, structure, instructor, exam_slot, class_slot, room in mtech_1st:
        body = (
            f"Course Code: {code}. Course Name: {name}. "
            f"Structure: {structure} (Lecture-Tutorial-Practical-Credits). "
            f"Instructor: {instructor}. "
            f"Class Slot: {class_slot} ({slot_time(class_slot)}). "
            f"Exam Slot: {exam_slot}. Classroom: {room}. "
            f"Programme: M.Tech CSE 1st Semester. "
            f"Semester: July-November 2026. IIT Guwahati."
        )
        write_doc(f"{OUT_DIR}/timetable_mtech_{code}.txt", "TIMETABLE", DATE,
                  f"{code} {name} - MTech CSE Sem 1", body)

    # MTech 1st sem summary
    write_doc(f"{OUT_DIR}/timetable_mtech_1st_summary.txt", "TIMETABLE", DATE,
              "M.Tech CSE 1st Semester Timetable Summary",
              "M.Tech CSE 1st Semester courses July-November 2026 at IIT Guwahati. "
              "CS5001 Design and Analysis of Algorithms by Sushanta Karmakar slot B room 5G4. "
              "CS5002L Data Structures Lab by R Inkulu slot ML5 Friday lab room 5101. "
              "CS5003 Mathematics for Computer Science by P Bhaduri slot A room 5403. "
              "Elective slots available: Elective 1 and Elective 2.")

    # ── MTech CSE 3rd Sem Courses ──────────────────────────────────────────────
    mtech_3rd = [
        ("CS6902P", "Project - I", "0-0-24-24", "CSE Department", "-", "-", "-"),
    ]
    write_doc(f"{OUT_DIR}/timetable_mtech_3rd_summary.txt", "TIMETABLE", DATE,
              "M.Tech CSE 3rd Semester Timetable Summary",
              "M.Tech CSE 3rd Semester July-November 2026 IIT Guwahati. "
              "CS6902P Project I is the main course worth 24 credits. "
              "Students are engaged in thesis or project work under supervisor.")

    # ── BTech CSE Courses (3rd sem) ────────────────────────────────────────────
    btec_3rd = [
        ("CS2001", "Optimization Methods", "3-0-0-6", "Sukanta Bhattacharjee", "A", "A", "5G4"),
        ("CS2002", "Design and Analysis of Algorithms", "3-0-0-6", "Sriram Bhyravarapu", "D", "D", "5101"),
        ("CS2003", "Formal Languages and Automata Theory", "3-0-0-6", "Diganta Goswami", "E", "E", "5101"),
        ("CS2201", "Computer Organization and Architecture", "3-0-0-6", "John Jose", "C", "C", "5101"),
        ("CS2202L", "Hardware Lab", "0-1-3-5", "Lokesh Sidhu", "AL2", "D (Wednesday)", "5101"),
        ("CS2101L", "System Software Lab", "0-1-3-5", "Sanasam Ranbir Singh", "AL1", "A (Monday)", "5101"),
        ("CS2091M", "Data Structures and Algorithms", "3-0-0-6", "S V Rao", "F", "F", "5101"),
    ]

    for code, name, structure, instructor, exam_slot, class_slot, room in btec_3rd:
        body = (
            f"Course Code: {code}. Course Name: {name}. "
            f"Structure: {structure}. Instructor: {instructor}. "
            f"Class Slot: {class_slot} ({slot_time(class_slot)}). "
            f"Exam Slot: {exam_slot}. Classroom: {room}. "
            f"Programme: BTech CSE 3rd Semester. Semester: July-November 2026. IIT Guwahati."
        )
        write_doc(f"{OUT_DIR}/timetable_btechcse3_{code}.txt", "TIMETABLE", DATE,
                  f"{code} {name} - BTech CSE Sem 3", body)

    # ── BTech CSE 5th sem key courses ─────────────────────────────────────────
    btec_5th = [
        ("CS3103", "Computer Networks", "3-0-0-6", "Sukumar Nandi", "B1", "B1", "5G4"),
        ("CS3104L", "Computer Networks Laboratory", "0-0-4-4", "Manas Khatua", "ML1", "-", "-"),
        ("CS3105", "Operating Systems", "3-0-0-6", "Satyajit Das", "C1", "C1", "5G4"),
        ("CS3106L", "Operating Systems Laboratory", "0-0-4-4", "Satyajit Das", "ML2", "E1 (Tuesday)", "5101"),
        ("CS3201M", "Digital Logic and Computer Architecture", "3-0-0-6", "Aryabartta Sahu", "E1", "E1", "5G4"),
        ("MA321", "Optimization", "3-0-0-6", "Mathematics Dept", "D1", "D1", "-"),
    ]

    for code, name, structure, instructor, exam_slot, class_slot, room in btec_5th:
        body = (
            f"Course Code: {code}. Course Name: {name}. "
            f"Structure: {structure}. Instructor: {instructor}. "
            f"Class Slot: {class_slot} ({slot_time(class_slot)}). "
            f"Exam Slot: {exam_slot}. Classroom: {room}. "
            f"Programme: BTech CSE 5th Semester. Semester: July-November 2026. IIT Guwahati."
        )
        write_doc(f"{OUT_DIR}/timetable_btechcse5_{code}.txt", "TIMETABLE", DATE,
                  f"{code} {name} - BTech CSE Sem 5", body)

    # ── Departmental Electives (open to MTech + senior UG) ─────────────────────
    electives = [
        ("CS3001", "OOPs and Data Structures", "V Saradhi", "F1", "5406", "3rd year+"),
        ("CS4101", "IoT App Development", "Manas Khatua", "F", "5406", "3rd year+"),
        ("CS5099", "Parallel Algorithms", "G Sajith", "F1", "5101", "3rd year+"),
        ("CS5097", "Randomized Algorithms", "Pinaki Mitra", "G", "5405", "3rd year+"),
        ("CS5191", "Virtual and Augmented Reality", "Samit Bhattacharya", "D1", "5G4", "all"),
        ("CS5187", "Software Analysis", "Bernard Nongpoh", "A1", "5G4", "3rd year+"),
        ("CS5290", "Memory-centric Computing Architectures", "Phrangboklang Lyngton Thangkhiew", "A1", "5405", "3rd year+"),
        ("CS5393", "Generative AI for Computer Vision", "Arijit Sur", "E", "5G4", "all"),
        ("CS5399", "Topics and Tools in Social Media Data Mining", "Sanasam Ranbir Singh", "F1", "5G4", "all"),
        ("CS5396", "Speech Processing", "P K Das", "G1", "5405", "all"),
        ("CS6398", "Nature-inspired Computing", "S B Nair", "B1", "5101", "all"),
        ("CS6399", "Mathematics for ML", "Ashish Anand", "G", "5101", "all"),
        ("CS6198", "Internet Engineering and Operations", "T Venkatesh", "A1", "5101", "all"),
        ("CS5291", "C-based VLSI Design", "C Karfa", "F1", "5405", "3rd year+"),
        ("CS4302M", "Machine Intelligence", "Amit Awekar", "A", "5101", "BTech 7th sem"),
    ]

    for code, name, instructor, slot, room, eligibility in electives:
        body = (
            f"Course Code: {code}. Course Name: {name}. "
            f"Instructor: {instructor}. "
            f"Class Slot: {slot} ({slot_time(slot)}). "
            f"Classroom: {room}. Eligibility: {eligibility}. "
            f"Type: Departmental Elective or Open Elective. "
            f"Semester: July-November 2026. IIT Guwahati CSE Department."
        )
        write_doc(f"{OUT_DIR}/timetable_elective_{code}.txt", "TIMETABLE", DATE,
                  f"{code} {name} (Elective)", body)

    # ── UG 1st Year CSE Timetable ──────────────────────────────────────────────
    ug1_cse = [
        ("CS1113", "Introduction to Programming", "Deepanjan Kesh", "D1", "A", "5405"),
        ("CS1115", "Discrete Mathematics", "Khushraj Madnani", "A1", "E", "5405"),
        ("CS1116H", "Introduction to Computer Systems (pre-midsem)", "T Venkatesh", "C1", "C", "5405"),
        ("EE1101H", "Electric Circuits (pre-midsem)", "deb.sikdar", "F1", "D", "5405"),
        ("EE1105H", "Digital and Analog Electronics (post-midsem)", "deb.sikdar", "F1", "D", "5405"),
        ("MA1301H", "Single Variable Calculus (pre-midsem)", "pati", "B1", "B", "5405"),
        ("MA1501H", "Multi Variable Calculus (post-midsem)", "pati", "B1", "B", "5405"),
        ("CS1114L", "Programming Lab", "Deepanjan Kesh", "-", "MON 2-5PM", "5G4"),
        ("EE1109L", "Basic Electronics Lab", "sonkar", "-", "FRI 2-5PM", "-"),
    ]

    for code, name, instructor, exam_slot, class_slot, room in ug1_cse:
        body = (
            f"Course Code: {code}. Course Name: {name}. "
            f"Instructor: {instructor}. "
            f"Class Slot: {class_slot} ({slot_time(class_slot)}). "
            f"Exam Slot: {exam_slot}. Classroom: {room}. "
            f"Programme: BTech CSE 1st Year 1st Semester. "
            f"Semester: July-November 2026. IIT Guwahati."
        )
        write_doc(f"{OUT_DIR}/timetable_ug1cse_{code}.txt", "TIMETABLE", DATE,
                  f"{code} {name} - BTech CSE Year 1", body)

    # Slot guide doc — very useful for search
    slot_guide = " ".join([f"Slot {k}: {v}." for k, v in SLOT_MAP.items()])
    write_doc(f"{OUT_DIR}/timetable_slot_guide.txt", "TIMETABLE", DATE,
              "Class Slot Time Guide - IIT Guwahati CSE July-November 2026",
              f"IIT Guwahati CSE Department class slot to day and time mapping. "
              f"July-November 2026 semester. {slot_guide}")

    print(f"[TIMETABLE] Written {3 + 7 + 6 + len(electives) + len(ug1_cse) + 3} timetable docs")

if __name__ == "__main__":
    parse()
