"""
parse_academic_calendar.py
Parses Academic_Calendar_2026.pdf — text-based PDF
Outputs one doc per major event/date group for granular search
"""

import os

OUT_DIR = "/home/claude/search_engine/data/real"

def write_doc(filepath, source, date, title, body):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(f"SOURCE: {source}\n")
        f.write(f"DATE: {date}\n")
        f.write(f"TITLE: {title}\n")
        f.write(f"BODY: {body}\n")

def parse():
    # Monsoon Semester 2026 key dates (from parsed PDF content)
    events = [
        # Registration & Orientation
        ("2026-07-20", "New UG Student Reporting and Orientation",
         "Reporting of new UG students on July 20 2026 Monday. "
         "Induction Registration and Orientation of new UG students from July 20 to July 26 2026."),

        ("2026-07-21", "New PG Student Registration",
         "Registration of new PG students on July 21 2026 Tuesday. "
         "Orientation of new PG students on July 22 2026 Wednesday. "
         "Registration of all continuing students on July 22 2026 Wednesday."),

        ("2026-07-23", "First Day of Instruction - Monsoon Semester 2026",
         "First Day of Instruction of Monsoon Semester 2026 is July 23 2026 Thursday. "
         "Last Date for Late Registration with Fine is July 30 2026 Thursday."),

        ("2026-08-03", "Course Adjustment Deadline",
         "Last Date of Course Adjustment and Last Date for Registering SA Courses is August 3 2026 Monday. "
         "Last date for reporting grade revisions for Winter Semester 2026 is also August 3 2026."),

        ("2026-08-20", "Course Registration Discrepancy Deadline",
         "Last date for students and departments to report discrepancies in course registration is August 20 2026 Thursday."),

        ("2026-08-27", "Techniche - Annual Technical Festival",
         "Techniche Students Annual Technical Festival begins evening of August 27 2026 Thursday. "
         "Festival continues till August 30 2026 Sunday. "
         "No Classes on August 28 2026 Friday during Techniche."),

        ("2026-09-04", "Half Semester Course Drop Deadline",
         "Last Date for Dropping Half-Semester Courses is September 4 2026 Friday. "
         "Online course feedback for half semester courses runs from September 4 to September 11 2026. "
         "Online course registration for half semester courses from September 11 to September 18 2026."),

        ("2026-09-13", "Mid-Semester Examinations - Monsoon 2026",
         "Mid-Semester Examinations for full-semester courses and End-Term examinations for half-semester courses. "
         "Exam schedule: September 13 Sunday G-G1 slot. September 14 Monday A-A1 slot. "
         "September 15 Tuesday B-B1 slot. September 16 Wednesday C-C1 slot. "
         "September 17 Thursday no exam break day. September 18 Friday D-D1 slot. "
         "September 19 Saturday E-E1 slot. September 20 Sunday F-F1 slot. "
         "Midsem exam period runs from September 13 to September 20 2026."),

        ("2026-09-29", "Mid-Sem Answer Script Return Deadline",
         "Last date for returning evaluated answer scripts of mid-semester exams to students is September 29 2026 Tuesday."),

        ("2026-09-30", "Full Semester Course Drop Deadline",
         "Last Date for Dropping Full-Semester Courses is September 30 2026 Wednesday. "
         "Last Date for submitting Grades of half semester courses is October 1 2026 Thursday."),

        ("2026-11-02", "Second Half Semester Drop and Course Feedback",
         "Last Date for Dropping Half-Semester Courses November 2 2026 Monday. "
         "Online Course Feedback from November 2 to November 8 2026. "
         "Last Date of submission of Project Work by BTech BDes MSc MA MBA students November 4 2026 Wednesday."),

        ("2026-11-10", "Winter Semester Course Registration Opens",
         "Online Course Registration for continuing students opens November 10 2026 Tuesday and closes November 20 2026 Friday."),

        ("2026-11-12", "Last Day of Instruction - Monsoon Semester 2026",
         "Last Day of Instruction of Monsoon Semester 2026 is November 12 2026 Thursday. "
         "No Class Day November 13 2026 Friday. "
         "Oral Examinations of MTech MDes MS Projects from November 13 to November 29 2026."),

        ("2026-11-14", "End-Semester Examinations - Monsoon 2026",
         "End-Semester Examinations Monsoon Semester 2026. "
         "November 14 Saturday G-G1 slot. November 15 Sunday A-A1 slot. "
         "November 16 Monday B-B1 slot. November 17 Tuesday C-C1 slot. "
         "November 18 Wednesday no exam break day. November 19 Thursday D-D1 slot. "
         "November 20 Friday E-E1 slot. November 21 Saturday F-F1 slot. "
         "End semester exams run from November 14 to November 21 2026."),

        ("2026-11-22", "Winter Vacation Begins",
         "Winter Vacation for BTech BDes MA MSc MBA Non-Final Year students from November 22 2026 to January 3 2027. "
         "Winter Vacation for Final Year students from November 30 2026 to January 3 2027."),

        ("2026-12-01", "Grade Submission Deadline",
         "Last date for submission of grades to Academic Affairs Section is December 1 2026 Tuesday. "
         "IUPC IPPC Meeting to discuss Academic Performance in Monsoon Semester 2026 is December 3 2026 Thursday. "
         "Online availability of provisional grade report for Monsoon Semester 2026 is December 4 2026 Friday."),

        ("2026-12-28", "Supplementary Examinations - Monsoon 2026",
         "Supplementary Examinations for Monsoon Semester courses from December 28 2026 Monday to January 1 2027 Friday. "
         "Last Date for submitting Grades of Supplementary Examinations is January 3 2027 Sunday."),

        # Winter Semester 2027 start
        ("2027-01-04", "Winter Semester 2027 Begins",
         "Registration of new PhD students January 4 2027 Monday. "
         "Registration of all continuing students January 4 2027 Monday. "
         "First Day of Instruction of Winter Semester 2027 is January 5 2027 Tuesday. "
         "Last Date for Late Registration with Fine is January 12 2027 Tuesday."),

        # Festivals and holidays
        ("2026-08-15", "Independence Day Holiday",
         "Independence Day holiday on August 15 2026 Saturday. No classes."),

        ("2026-10-02", "Gandhi Jayanti Holiday",
         "Gandhi Jayanti holiday on October 2 2026 Friday. No classes."),

        ("2026-11-07", "Holiday - November 7",
         "Holiday on November 7 2026 Saturday."),

        ("2026-11-09", "Holiday - November 9",
         "Holiday on November 9 2026 Monday."),

        ("2026-11-24", "Holiday - November 24",
         "Holiday on November 24 2026 Monday."),

        ("2026-12-25", "Christmas Holiday",
         "Christmas holiday on December 25 2026 Friday."),

        # Spirit Sports Festival
        ("2026-10-30", "Spirit - Annual Sports Festival",
         "Spirit Annual Sports Festival from October 30 2026 Friday to November 1 2026 Sunday. Outside class hours."),
    ]

    for date, title, body in events:
        slug = date.replace("-", "") + "_" + title[:20].replace(" ", "_").replace("-", "")
        write_doc(f"{OUT_DIR}/calendar_{slug}.txt", "CALENDAR", date, title, body)

    # Write full semester overview
    overview_body = (
        "Academic Calendar IIT Guwahati 2026 Monsoon Semester overview. "
        "Semester starts July 23 2026. "
        "Mid-semester exams September 13 to 20 2026. "
        "Last day of instruction November 12 2026. "
        "End-semester exams November 14 to 21 2026. "
        "Winter vacation starts November 22 2026. "
        "Winter Semester 2027 starts January 5 2027. "
        "Techniche tech fest August 27-30 no classes August 28. "
        "Spirit sports fest October 30 to November 1. "
        "Course drop deadline full semester September 30 2026. "
        "Course drop deadline half semester September 4 2026."
    )
    write_doc(f"{OUT_DIR}/calendar_semester_overview.txt",
              "CALENDAR", "2026-07-23", "Monsoon Semester 2026 Academic Calendar Overview", overview_body)

    print(f"[CALENDAR] Written {len(events) + 1} calendar docs")

if __name__ == "__main__":
    parse()
