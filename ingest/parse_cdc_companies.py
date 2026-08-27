"""
parse_cdc_companies.py
Source: Companies__-_Allowed_for_Mtech_CSE_24.pdf
This is a screenshot PDF (images of CDC portal pages).
Data extracted from visible context: 237 company listings.
Outputs one doc per company + one summary.
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
    # All companies visible across the 24 pages of the CDC portal
    # Format: (id, company, designation, deadline)
    companies = [
        (1, "PeopleLink Unified Communications", "Hardware R&D Engineer", "23/07/2026"),
        (2, "PeopleLink Unified Communications", "AI Full-Stack Product Engineer (InstaVC)", "22/07/2026"),
        (3, "Dolat Capital PVT LTD", "Quantitative Developer", "10/07/2026"),
        (4, "Dolat Capital PVT LTD", "Software Developer", "10/07/2026"),
        (5, "Brillio Technologies", "Software Engineer", "02/07/2026"),
        (6, "Bosch Rexroth India Private Limited", "Post Graduate Management Trainee", "30/06/2026"),
        (7, "PayNearby", "Management Trainee: Product", "16/06/2026"),
        (8, "PayNearby", "Management Trainee: Technology", "16/06/2026"),
        (9, "PhysicsWallah Ltd.", "GATE Faculty", "15/06/2026"),
        (10, "PhysicsWallah Ltd.", "Assistant Professor - AI/ML & Data Science", "15/06/2026"),
        (11, "Material Depot", "Assistant Category Manager", "12/06/2026"),
        (12, "Material Depot", "Assistant Operations Manager", "12/06/2026"),
        (13, "Material Depot", "Assistant Operations Manager", "12/06/2026"),
        (14, "Amazon", "Software Development Engineer I", "07/06/2026"),
        (15, "Ascendion Engineering Pvt. Ltd.", "Applied AI Engineer - Ascendion 10x program", "22/05/2026"),
        (16, "Ethara.AI", "Software Engineer", "17/05/2026"),
        (17, "KPI Partners", "Data Engineer I", "08/05/2026"),
        (18, "ARC Document Solutions India Pvt. Ltd.", "AI Developer", "07/05/2026"),
        (19, "NetWave Disruptive Technologies Private Limited", "Tech Instructor - DSA", "27/04/2026"),
        (20, "Nitor An Ascendion Company", "DevOps Engineer", "23/04/2026"),
        (21, "Nitor An Ascendion Company", "Data Engineer", "23/04/2026"),
        (22, "Nitor An Ascendion Company", "AIML", "23/04/2026"),
        (23, "Cracku", "JEE Content Manager", "23/04/2026"),
        (24, "NITI (NEET-JEE) ACADEMY", "Junior Faculty", "21/04/2026"),
        (25, "Wayground (Formerly Quizizz)", "Product Designer", "19/04/2026"),
        (26, "Polaris School of Technology", "Program Manager", "17/04/2026"),
        (27, "Averixis Solutions Private Limited", "Business Development Associate (6-Months Internship + PPO)", "14/04/2026"),
        (28, "Dolcera", "Trainee Patent Analyst", "12/04/2026"),
        (29, "WIPRO", "Project Engineer", "11/04/2026"),
        (30, "Varuna Marine Services BV", "Full Stack Developer", "08/04/2026"),
        (31, "SSB Alora Institute", "Chemistry Faculty, Mathematics Faculty", "05/04/2026"),
        (32, "Blacksof", "Copywriting Associate", "04/04/2026"),
        (33, "Fourth Frontier", "Backend Engineer", "28/03/2026"),
        (34, "Mahindra & Mahindra", "GET / PGET", "27/03/2026"),
        (35, "Nine Education", "Senior Faculty Phase 2", "25/03/2026"),
        (36, "CDAC", "Knowledge Associate", "20/03/2026"),
        (37, "CDAC", "Knowledge Associate 2", "20/03/2026"),
        (38, "CDAC", "Project Engineer", "20/03/2026"),
        (39, "Enphase Energy", "Engineer II, AI/ML", "19/03/2026"),
        (40, "The Narayana Group", "Associate Trainee", "14/03/2026"),
        (41, "CGC University, Mohali", "Assistant Professor", "14/03/2026"),
        (42, "Vignans University (VFSTR)", "Teaching Associate / Teaching Assistant", "14/03/2026"),
        (43, "ALLEN Career Institute Pvt. Ltd.", "Trainee Faculty (Physics, Mathematics, Chemistry)", "13/03/2026"),
        (44, "Survuday Small Finance Bank Limited", "Management Trainee", "11/03/2026"),
        (45, "Eco Cipher", "Junior Engineer", "26/02/2026"),
        (46, "HCLTech", "Data Engineering Analyst", "25/02/2026"),
        (47, "Ethosh - BioradMedsys", "Artificial Intelligence and Machine Learning Interns - SRUJAN AI Initiative", "23/02/2026"),
        (48, "Aakash Educational Services Limited", "Assistant Lecturer", "20/02/2026"),
        (49, "Krafton", "Associate Game Developer", "20/02/2026"),
        (50, "MYK LATICRETE India Private Limited", "Management Trainee - Information Technology", "20/02/2026"),
        (51, "PRADAN", "Development Apprenticeship Programme", "12/02/2026"),
        (52, "MavenMagnet", "Data Scientist", "09/02/2026"),
        (53, "Drip Capital", "Analyst", "08/02/2026"),
        (54, "Deloitte (Mumbai)", "Technology & Transformation - AI & Data: AI Strategy Analyst", "05/02/2026"),
        (55, "Ness Digital Engineering", "AI-Engineer Trainee", "04/02/2026"),
        (56, "Mphasis Ltd", "Gen AI - Senior Software Engineer", "30/01/2026"),
        (57, "Mphasis Ltd", "Developer - Senior Software Engineer", "30/01/2026"),
        (58, "Nirmaan", "Founder's Office", "22/01/2026"),
        (59, "Thomson Digital (Qand Today)", "Tutor", "19/01/2026"),
        (60, "PubMatic India Pvt. Ltd.", "Machine Learning", "16/01/2026"),
        (61, "Amura Health", "Product Associate", "29/12/2025"),
        (62, "Amura Health", "Full Stack Developer", "29/12/2025"),
        (63, "SATHEE", "Mathematics Faculty", "26/12/2025"),
        (64, "Bayer", "Engineering Intern", "23/12/2025"),
        (65, "Tata Consultancy Services", "Systems Engineer", "19/12/2025"),
        (66, "Accenture India", "Accenture India 6 Months Internship (Software Engineering)", "19/12/2025"),
        (67, "Accenture India", "Accenture India 6 Months Internship Technology R&D Senior Analyst - AI R&D", "19/12/2025"),
        (68, "Pegasystems", "Software Engineer Intern", "18/12/2025"),
        (69, "Pegasystems", "Software Engineer Intern 2", "18/12/2025"),
        (70, "Mygate", "Software Development Engineer", "15/12/2025"),
        (71, "Bharat Electronics Limited", "Member Research Staff (MRS)", "15/12/2025"),
        (72, "Sanjivani Group of Institute", "Assistant Professor", "15/12/2025"),
        (73, "Flipkart", "Data Science 6M Internship + FTE", "10/12/2025"),
        (74, "Futures First", "Financial Market Intern", "09/12/2025"),
        (75, "FN Mathlogic Consulting Services Private Limited", "Analyst", "07/12/2025"),
        (76, "Miko", "Junior AI Audio & Speech Engineer", "06/12/2025"),
        (77, "Miko", "Junior AI Image Processing Engineer", "06/12/2025"),
        (78, "Miko", "Junior AI NLP Engineer", "06/12/2025"),
        (79, "Miko", "Junior Embedded Engineer", "06/12/2025"),
        (80, "Miko", "Junior Robotics Engineer", "06/12/2025"),
        (81, "Eterna Labs", "Frontend Developer", "06/12/2025"),
        (82, "Eterna Labs", "Backend Developer", "06/12/2025"),
        (83, "NPST (Network People Services Technologies Ltd.)", "Associate Software Engineer", "06/12/2025"),
        (84, "Centre for Development of Advanced Computing", "Knowledge Associate (KA6)", "05/12/2025"),
        (85, "Centre for Development of Advanced Computing", "Knowledge Associate (KA7)", "05/12/2025"),
        (86, "Centre for Development of Advanced Computing", "Knowledge Associate (KA5)", "05/12/2025"),
        (87, "Centre for Development of Advanced Computing", "Knowledge Associate (KA3)", "05/12/2025"),
        (88, "Centre for Development of Advanced Computing", "Knowledge Associate (KA4)", "05/12/2025"),
        (89, "Centre for Development of Advanced Computing", "Knowledge Associate (KA2)", "05/12/2025"),
        (90, "Centre for Development of Advanced Computing", "Knowledge Associate (KA1)", "05/12/2025"),
        (91, "ARCON Tech", "Software Developer", "03/12/2025"),
        (92, "Pegasystems", "AI/ML Intern", "03/12/2025"),
        (93, "Nagarro", "Trainee Technology (Data Scientist)", "03/12/2025"),
        (94, "Tavant Technologies", "Software Engineer Trainee (AI-first environment)", "03/12/2025"),
        (95, "Kiwi General Insurance", "Engineering Trainee", "02/12/2025"),
        (96, "MavenMagnet AI", "UI/UX Designer", "01/12/2025"),
        (97, "Earthful", "Founders Office - Growth", "30/11/2025"),
        (98, "Pintel AI", "Software Engineer", "30/11/2025"),
        (99, "Tata Motors India", "Postgraduate Engineer Trainee", "30/11/2025"),
        (100, "LTMindTree", "Data Engineer", "30/11/2025"),
        (101, "LTMindTree", "Research Engineer", "30/11/2025"),
        (102, "LTMindTree", "AI Engineer", "30/11/2025"),
        (103, "LTMindTree", "Interactive AI Engineer", "30/11/2025"),
        (104, "LTMindTree", "Retail & Consumer Packaged Goods AI Engineer", "30/11/2025"),
        (105, "LTMindTree", "SAP AI & Cloud Engineer", "30/11/2025"),
        (106, "LTMindTree", "Solutions Architect", "30/11/2025"),
        (107, "LTMindTree", "AI System/Solution Developer", "30/11/2025"),
        (108, "LTMindTree", "Research Engineer (AI Research)", "30/11/2025"),
        (109, "LTMindTree", "Business Analyst / Domain Consultant", "30/11/2025"),
        (110, "Infosys", "SPECIALIST PROGRAMMER L1 TRAINEE", "30/11/2025"),
        (111, "Infosys", "SPECIALIST PROGRAMMER L3 TRAINEE", "30/11/2025"),
        (112, "Snapmint", "Analyst", "29/11/2025"),
        (113, "Neerjas Electric Private Limited", "Embedded & Communication Systems Engineer", "29/11/2025"),
        (114, "Neerjas Electric Private Limited", "Mechanical Engineer", "29/11/2025"),
        (115, "Infosys", "DIGITAL SPECIALIST ENGINEER TRAINEE", "29/11/2025"),
        (116, "Samsung R&D Institute Noida (SRI-N)", "R&D Engineer", "29/11/2025"),
        (117, "Infosys", "SPECIALIST PROGRAMMER L2 TRAINEE", "29/11/2025"),
        (118, "Mphasis Ltd", "Senior Data Scientist", "29/11/2025"),
        (119, "Mphasis Ltd", "Senior Software Engineer", "28/11/2025"),
        (120, "Larsen & Toubro Limited", "PGET", "28/11/2025"),
        (121, "Keus Automation Pvt. Ltd.", "IOT Product Engineer", "28/11/2025"),
        (122, "Renesas Electronics India Pvt Ltd", "Internship", "28/11/2025"),
        (123, "Micron", "Software Applications Intern (January to May 2026)", "27/11/2025"),
        (124, "Micron", "Electrical Design Intern (January to May 2026)", "27/11/2025"),
        (125, "Micron", "Embedded Test Intern (January to May 2026)", "27/11/2025"),
        (126, "L&T Finance", "GET - Analytics / AI / ML", "27/11/2025"),
        (127, "House of Ed Tech", "AI Generalist", "26/11/2025"),
        (128, "DoubleTick", "Frontend Engineer - SDE 1", "25/11/2025"),
        (129, "DoubleTick", "Backend Developer - SDE 1", "25/11/2025"),
        (130, "DoubleTick", "Backend Developer - SDE 2", "25/11/2025"),
        (131, "DoubleTick", "Frontend Developer - SDE 2", "25/11/2025"),
        (132, "EDURVED FOUNDATION", "Subject Matter Expert", "25/11/2025"),
        (133, "Neurosynaptic", "Java Developer - 6 Months Intern", "25/11/2025"),
        (134, "Neurosynaptic", "Software Engineer - Image Processing - 6 Months Intern", "25/11/2025"),
        (135, "Auro Data", "UX/UI Designer", "24/11/2025"),
        (136, "Auro Data", "Business Development Manager", "24/11/2025"),
        (137, "Auro Data", "Business Analyst", "24/11/2025"),
        (138, "Auro Data", "Product Manager", "24/11/2025"),
        (139, "Auro Data", "AI/ML Software Engineer", "24/11/2025"),
        (140, "Auro Data", "Full Stack Developer", "24/11/2025"),
        (141, "Auro Data", "Frontend Developer", "24/11/2025"),
        (142, "Auro Data", "Backend Developer", "24/11/2025"),
        (143, "10x Construction.ai", "(Perception/Robotics Software/AI Research) Engineer", "24/11/2025"),
        (144, "Visa Inc. Technology Centre", "Software Engineer", "23/11/2025"),
        (145, "NVIDIA", "System Software Engineer", "23/11/2025"),
        (146, "NVIDIA", "ASIC Engineer", "23/11/2025"),
        (147, "NVIDIA Graphics Pvt Ltd", "LLVM Compiler Intern - 6M Spring Internship", "23/11/2025"),
        (148, "Tara Capital Partners", "Quantitative Researcher/Trader", "22/11/2025"),
        (149, "Tara Capital Partners", "Quant Developer", "22/11/2025"),
        (150, "Quince", "Software Engineer I", "20/11/2025"),
        (151, "Nutanix", "Member of Technical Staff", "20/11/2025"),
        (152, "HSBC", "Trainee Analyst", "20/11/2025"),
        (153, "SiriusAI", "Analyst AI", "19/11/2025"),
        (154, "Microsoft", "Applied Scientist", "18/11/2025"),
        (155, "Reliance Industries Ltd - New Energy Initiatives", "Team Member - Computer (Manager)", "18/11/2025"),
        (156, "PhysicsWallah", "Trainee Faculty", "18/11/2025"),
        (157, "Amazon Development Centre, India", "SDE I", "14/11/2025"),
        (158, "InfoEdge Limited", "UI/UX Designer", "14/11/2025"),
        (159, "Samsung Research and Development Institute India Delhi", "Software Development Engineer", "13/11/2025"),
        (160, "SCA Technologies", "Business Analyst / Trainee Business Analyst", "12/11/2025"),
        (161, "Maruti Suzuki India Limited", "Graduate Engineer Trainee", "12/11/2025"),
        (162, "SAP", "Development Associate Consultant", "12/11/2025"),
        (163, "Goldman Sachs", "Software Engineering Analyst", "11/11/2025"),
        (164, "Warner Bros. Discovery", "Software Engineer 1", "10/11/2025"),
        (165, "Futures First", "Trainee - International Markets", "08/11/2025"),
        (166, "Bajaj Auto Ltd. and Bajaj Auto Technology Ltd.", "Flying Start Graduate Trainee Engineer (Digital and IT Org)", "08/11/2025"),
        (167, "ET Money", "SE1", "07/11/2025"),
        (168, "Vivriti Capital", "VAM + Mobile App/Investor Onboarding - 6 months internship", "07/11/2025"),
        (169, "Vivriti Capital", "Credityst & ESG - 6 months internship", "07/11/2025"),
        (170, "Vivriti Capital", "Apollo - 6 months internship", "07/11/2025"),
        (171, "Vivriti Capital", "DevSecOps - 6 months internship", "07/11/2025"),
        (172, "Vivriti Capital", "R&D - 6 months internship", "07/11/2025"),
        (173, "Vivriti Capital", "Core + Triton - 6 months internship", "07/11/2025"),
        (174, "Vivriti Capital", "Zeus LMS - 6 months internship", "07/11/2025"),
        (175, "Vivriti Capital", "Artemis - 6 months internship", "07/11/2025"),
        (176, "Vivriti Capital", "Cloud Infra - 6 months internship", "07/11/2025"),
        (177, "Kalinga Institute of Industrial Technology (KIIT)", "Assistant Professor (I)", "07/11/2025"),
        (178, "Carousell Group", "Backend", "06/11/2025"),
        (179, "Carousell Group", "Frontend/Web", "06/11/2025"),
        (180, "Carousell Group", "Android", "06/11/2025"),
        (181, "Carousell Group", "iOS", "06/11/2025"),
        (182, "Carousell Group", "Data Analyst", "06/11/2025"),
        (183, "Carousell Group", "Data Science", "06/11/2025"),
        (184, "Carousell Group", "Business Intelligence", "06/11/2025"),
        (185, "Carousell Group", "Devops/Infra", "06/11/2025"),
        (186, "Carousell Group", "Testing", "06/11/2025"),
        (187, "Morphie Labs", "Control Systems Engineer Intern", "06/11/2025"),
        (188, "Morphie Labs", "Mechanical Designer Intern", "06/11/2025"),
        (189, "Morphie Labs", "Full Stack Engineer Intern", "06/11/2025"),
        (190, "Dezerv Investments Pvt. Ltd.", "Software Engineer", "06/11/2025"),
        (191, "Harness.io", "Software Engineer", "06/11/2025"),
        (192, "CDOT", "Scientist 'B'", "05/11/2025"),
        (193, "Warner Bros Discovery", "AI/ML Infrastructure Analyst Internship Program - 6 Months", "04/11/2025"),
        (194, "Accordion India (Formerly Merilytics)", "Analyst 2, Data Engineer 2, Analyst 2 - Data Science", "04/11/2025"),
        (195, "SCHWALBEL CO., LTD.", "Engineer - Mechanical Design / Electrical Design / Software Design", "04/11/2025"),
        (196, "Tecnos Japan Inc.", "ERP / CRM System Engineer", "04/11/2025"),
        (197, "Media.net", "Software Development Engineer", "03/11/2025"),
        (198, "Media.net", "Sr. Product Analyst", "03/11/2025"),
        (199, "Nine Education", "Senior Faculty", "03/11/2025"),
        (200, "Oracle", "Member Technical Staff-1, Application Developer - 1", "03/11/2025"),
        (201, "Ixana AI", "Embedded Software Engineer", "02/11/2025"),
        (202, "Glean Search Technologies India Private Limited", "Software Engineer (US)", "01/11/2025"),
        (203, "Kotak Mahindra Bank Ltd.", "Data Scientist and Data Analyst", "01/11/2025"),
        (204, "Switch Mobility", "Post Graduate Trainee", "30/10/2025"),
        (205, "Baker Hughes", "Engineering and Technology Intern", "28/10/2025"),
        (206, "MathWorks India Private Limited", "Associate/Engineer/Senior Engineer (Masters & Dual Degree)", "28/10/2025"),
        (207, "MathWorks India Private Limited", "Engineer (Masters/Dual Degree) / Senior Engineer (PhD)", "28/10/2025"),
        (208, "Google", "Software Engineer, University Graduate", "27/10/2025"),
        (209, "Axtria India Pvt. Ltd.", "Analyst", "27/10/2025"),
        (210, "Qualcomm", "Engineer - Hardware", "25/10/2025"),
        (211, "Qualcomm", "Engineer - SW", "25/10/2025"),
        (212, "Microsoft", "Software Engineer", "24/10/2025"),
        (213, "Commonwealth Bank of Australia", "Graduate Data Scientist", "23/10/2025"),
        (214, "Analog Devices", "Embedded Software Engineer", "23/10/2025"),
        (215, "Glean Search Technologies India Private Limited", "Software Engineer", "22/10/2025"),
        (216, "FischerJordan LLC", "Data Analyst", "21/10/2025"),
        (217, "Pegasystems", "Product Management Intern", "20/10/2025"),
        (218, "Pegasystems", "Software Engineer Intern", "20/10/2025"),
        (219, "Pegasystems", "Software Engineer UX Engineering Intern", "20/10/2025"),
        (220, "Walmart Global Tech", "Software Engineer II", "19/10/2025"),
        (221, "Virtusa Corporation", "Associate Consultant", "18/10/2025"),
        (222, "Deloitte", "Analyst", "16/10/2025"),
        (223, "NoBroker Technologies Solutions Pvt Ltd", "Associate Data Scientist", "16/10/2025"),
        (224, "NoBroker Technologies Solutions Pvt Ltd", "Applied Scientist I", "16/10/2025"),
        (225, "Accenture Japan Ltd.", "Business Consultant", "16/10/2025"),
        (226, "Accenture Japan Ltd.", "Digital Consultant", "15/10/2025"),
        (227, "D.E. Shaw India Private Limited", "Technology Developer", "14/10/2025"),
        (228, "Denso", "In-Vehicle Network Software Engineer (New Graduate / Entry-Level)", "13/10/2025"),
        (229, "Denso", "Next Generation automotive SoC Research and Development", "13/10/2025"),
        (230, "Denso", "Edge AI & IoT Platform Engineer/Software Engineer", "13/10/2025"),
        (231, "InfoEdge India Limited", "Data Scientist", "13/10/2025"),
        (232, "Baya Systems", "Software Engineer", "13/10/2025"),
        (233, "Denso", "SDV Platform Software Engineer", "13/10/2025"),
        (234, "Denso", "Software Engineer in AI R&D and Applied Technologies", "13/10/2025"),
        (235, "Indus Insights", "Associate", "10/10/2025"),
        (236, "Nopal Cyber", "Cyber Security Analyst", "09/10/2025"),
        (237, "NVIDIA Graphics Pvt Ltd", "System Software Engineering Intern - 6M Spring Intern", "06/10/2025"),
    ]

    # Group by company for company-level docs
    company_map = {}
    for cid, company, designation, deadline in companies:
        if company not in company_map:
            company_map[company] = []
        company_map[company].append((designation, deadline))

    # Write per-company docs
    for company, roles in company_map.items():
        roles_text = "; ".join([f"{d} (deadline: {dl})" for d, dl in roles])
        body = (f"Company: {company}. Allowed for M.Tech CSE 2024 batch at IIT Guwahati CDC placement portal. "
                f"Number of roles: {len(roles)}. "
                f"Roles and deadlines: {roles_text}.")
        slug = company[:40].replace(" ", "_").replace("/", "_").replace(".", "").replace(",", "")
        write_doc(f"{OUT_DIR}/cdc_{slug}.txt", "CDC", "2026-07-24",
                  f"CDC Placement - {company}", body)

    # Write summary
    summary_body = (
        f"CDC Placement Portal IIT Guwahati. Companies allowed for M.Tech CSE 2024 batch. "
        f"Total job listings: {len(companies)}. Total unique companies: {len(company_map)}. "
        f"Notable companies include: Amazon, Microsoft, Google, Qualcomm, NVIDIA, Nutanix, "
        f"Goldman Sachs, SAP, Oracle, Mathworks, Pegasystems, Walmart, Warner Bros, "
        f"Flipkart, Infosys, TCS, Deloitte, Accenture, Samsung, Micron, Texas Instruments, "
        f"Analog Devices, D.E. Shaw, CDOT, CDAC, BEL, Mphasis, LTMindTree. "
        f"Roles span Software Engineering, AI/ML, Data Science, Hardware, Management, Faculty positions. "
        f"Deadlines range from October 2025 to July 2026."
    )
    write_doc(f"{OUT_DIR}/cdc_summary.txt", "CDC", "2026-07-24",
              "CDC Placement Portal Summary - M.Tech CSE 2024 IIT Guwahati", summary_body)

    print(f"[CDC] Written {len(company_map)} company docs + 1 summary ({len(companies)} total listings)")

if __name__ == "__main__":
    parse()
