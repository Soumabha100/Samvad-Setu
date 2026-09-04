"""
Standard AICTE Model Curricula for Engineering Departments
Provides structured semester-wise subjects, core department status,
and course outcome topics for Civil, Computer Science, and Environmental Engineering.
"""

from typing import List, Dict, Any

AICTE_CIVIL_ENGINEERING: Dict[str, Any] = {
    "department": "Civil Engineering",
    "degree": "B.Tech",
    "curriculum_standard": "AICTE Model Curriculum 2024",
    "subjects": [
        # Year 1 (Foundation)
        {
            "subject_code": "CE-101",
            "subject_name": "Basic Civil Engineering & Environmental Studies",
            "academic_year": 1,
            "semester": 1,
            "is_core": True,
            "complexity_ceiling": 1,  # Can only take Tier 1 problems
            "course_outcomes": [
                "Understand fundamental civil infrastructure components: roads, bridges, water supply, and municipal buildings.",
                "Identify local environmental hazards, urban solid waste segregation, and community civic issues.",
                "Perform basic field measurements, photographic documentation, and civic survey reporting."
            ],
            "units": [
                "Unit 1: Introduction to Civil Infrastructure - Roads, Pavements, Culverts, and Public Buildings",
                "Unit 2: Environmental Sanitation - Solid waste collection, source segregation, and citizen awareness",
                "Unit 3: Basics of Surveying - Linear measurements, tape and compass surveys, field data collection",
                "Unit 4: Water Supply Basics - Sources of water, public water points, and conservation techniques"
            ]
        },
        # Year 2 (Applied Fundamentals)
        {
            "subject_code": "CE-201",
            "subject_name": "Surveying and Geomatics",
            "academic_year": 2,
            "semester": 3,
            "is_core": True,
            "complexity_ceiling": 2,
            "course_outcomes": [
                "Execute leveling, theodolite traverse, and total station mapping of roadways.",
                "Use handheld GPS and open-source GIS tools (QGIS) to map municipal civic assets like potholes, drains, and bins.",
                "Calculate cut-and-fill earthwork quantities for rural and urban road repairs."
            ],
            "units": [
                "Unit 1: Leveling and Contouring - Benchmark setting, road profile leveling, drain slope measurement",
                "Unit 2: Geodetic Surveying & Total Station - Feature mapping, civic coordinate capture",
                "Unit 3: GIS & GPS Basics - Spatial data capture of urban municipal assets, pothole mapping",
                "Unit 4: Earthwork Estimation - Area and volume calculations for municipal road repairs"
            ]
        },
        {
            "subject_code": "CE-204",
            "subject_name": "Fluid Mechanics and Open Channel Flow",
            "academic_year": 2,
            "semester": 4,
            "is_core": True,
            "complexity_ceiling": 2,
            "course_outcomes": [
                "Analyze hydrostatic pressure in municipal water pipes and storage tanks.",
                "Calculate flow discharge in open stormwater drains, culverts, and sewer pipes.",
                "Identify causes of hydraulic blockages and silt accumulation in urban channels."
            ],
            "units": [
                "Unit 1: Fluid Statics - Pressure head, manometers, pipe pressure testing",
                "Unit 2: Flow in Closed Conduits - Pipe friction losses, Hazen-Williams formula, municipal distribution networks",
                "Unit 3: Open Channel Flow - Manning's formula for storm drains, rectangular and trapezoidal roadside ditches",
                "Unit 4: Hydraulic Jumps and Flow Measurement - Weirs, flumes, and municipal runoff discharge"
            ]
        },
        # Year 3 (Core Professional Engineering)
        {
            "subject_code": "CE-301",
            "subject_name": "Highway and Transportation Engineering",
            "academic_year": 3,
            "semester": 5,
            "is_core": True,
            "complexity_ceiling": 3,
            "course_outcomes": [
                "Diagnose pavement distress: potholes, alligator cracking, rutting, ravelling, and edge breakdown.",
                "Design flexible and rigid pavements according to IRC specifications.",
                "Perform traffic volume studies, spot speed analysis, and intersection signal timing audits."
            ],
            "units": [
                "Unit 1: Pavement Distress Analysis - Pothole etiology, bituminous binder failure, water ingress in subgrade",
                "Unit 2: Flexible Pavement Design - IRC 37 guidelines, California Bearing Ratio (CBR) testing, resurfacing overlays",
                "Unit 3: Highway Drainage - Roadside camber, transverse and longitudinal drains, cross-drainage culverts",
                "Unit 4: Traffic Engineering - Intersection design, blackspot accident analysis, traffic signal synchronization"
            ]
        },
        {
            "subject_code": "CE-302",
            "subject_name": "Wastewater and Environmental Engineering",
            "academic_year": 3,
            "semester": 6,
            "is_core": True,
            "complexity_ceiling": 3,
            "course_outcomes": [
                "Calculate urban sewage and stormwater runoff volumes based on catchment characteristics.",
                "Design municipal sewer networks, manhole spacing, drop manholes, and underground storm conduits.",
                "Evaluate wastewater quality parameters (BOD, COD, TSS, turbidity) and design secondary sewage treatment plants."
            ],
            "units": [
                "Unit 1: Sewerage Network Design - Separate vs combined systems, self-cleansing velocity, sewer pipe laying",
                "Unit 2: Sewer Appurtenances - Manholes, drop manholes, catch basins, gully traps, venting columns",
                "Unit 3: Sewage Treatment Processes - Primary sedimentation, Activated Sludge Process (ASP), trickling filters",
                "Unit 4: Municipal Solid Waste & Sludge Disposal - Anaerobic digestion, composting, engineered sanitary landfills"
            ]
        },
        # Year 4 (Advanced Capstone & Innovation)
        {
            "subject_code": "CE-401",
            "subject_name": "Smart City Infrastructure and Capstone Design",
            "academic_year": 4,
            "semester": 7,
            "is_core": True,
            "complexity_ceiling": 4,  # Capstone / Tier 4 eligible
            "course_outcomes": [
                "Synthesize multidisciplinary engineering solutions for acute urban and municipal crises.",
                "Deploy IoT sensor networks for real-time stormwater monitoring and smart drainage control.",
                "Formulate comprehensive engineering project reports, feasibility studies, and municipal cost estimations."
            ],
            "units": [
                "Unit 1: Smart Infrastructure Systems - SCADA water networks, automated flood warning sensors",
                "Unit 2: Advanced Pavement Materials - Waste plastic modified bitumen, geotextiles for pothole prevention",
                "Unit 3: Urban Hydrological Modeling - Catchment flood simulation, dynamic storm surge analysis",
                "Unit 4: Capstone Engineering Project - Industry/Municipal sponsored real-world problem solution prototype"
            ]
        }
    ]
}

AICTE_COMPUTER_SCIENCE: Dict[str, Any] = {
    "department": "Computer Science & Engineering",
    "degree": "B.Tech",
    "curriculum_standard": "AICTE Model Curriculum 2024",
    "subjects": [
        # Year 1 (Foundation)
        {
            "subject_code": "CS-101",
            "subject_name": "Programming for Problem Solving (Python & Web Basics)",
            "academic_year": 1,
            "semester": 1,
            "is_core": True,
            "complexity_ceiling": 1,
            "course_outcomes": [
                "Write basic Python scripts for citizen complaint data filtering and CSV processing.",
                "Create simple HTML/CSS responsive web forms for community feedback collection.",
                "Understand program logic, data types, loops, and file handling."
            ],
            "units": [
                "Unit 1: Python Basics - Variables, loops, functions, lists, dictionaries",
                "Unit 2: Data Handling - Reading/writing CSV and JSON files, basic data cleaning",
                "Unit 3: Web Fundamentals - HTML5 semantic forms, basic CSS styling, DOM structure",
                "Unit 4: Mini-Project - Building a simple command-line or static web citizen survey tool"
            ]
        },
        # Year 2 (Core Systems & Data)
        {
            "subject_code": "CS-201",
            "subject_name": "Database Management Systems & Web Development",
            "academic_year": 2,
            "semester": 3,
            "is_core": True,
            "complexity_ceiling": 2,
            "course_outcomes": [
                "Design relational schemas and write SQL queries for tracking municipal complaints.",
                "Develop full-stack web applications with RESTful APIs, user authentication, and role-based access.",
                "Integrate geolocation fields and coordinate queries in PostgreSQL/MySQL/MongoDB."
            ],
            "units": [
                "Unit 1: Relational Modeling - ER diagrams, normalization, schema design for civic incident tracking",
                "Unit 2: SQL & Query Optimization - CRUD operations, spatial queries, indexing",
                "Unit 3: Full Stack Web Architecture - Node/Express or FastAPI backends, React frontend",
                "Unit 4: Project - Multi-role grievance management dashboard with map pins"
            ]
        },
        # Year 3 (Software Systems & Applied AI)
        {
            "subject_code": "CS-301",
            "subject_name": "Applied Data Science and Computer Networks",
            "academic_year": 3,
            "semester": 5,
            "is_core": True,
            "complexity_ceiling": 3,
            "course_outcomes": [
                "Apply machine learning algorithms (Random Forest, SVM, LightGBM) to classify civic text complaints.",
                "Implement GIS spatial clustering (DBSCAN) to identify recurring garbage dumping and pothole hotspots.",
                "Build scalable REST microservices handling file uploads and asynchronous background processing."
            ],
            "units": [
                "Unit 1: Predictive Modeling - Scikit-learn, text preprocessing, TF-IDF, classification metrics",
                "Unit 2: Spatial Data Mining - Geohashing, DBSCAN cluster detection for municipal hotspot discovery",
                "Unit 3: Cloud & Networking - RESTful APIs, HTTP headers, CORS, JWT tokens, asynchronous workers",
                "Unit 4: Project - Intelligent civic triaging pipeline with automated duplicate clustering"
            ]
        },
        # Year 4 (Advanced Edge AI & Capstone)
        {
            "subject_code": "CS-401",
            "subject_name": "Edge AI, Computer Vision and Capstone System",
            "academic_year": 4,
            "semester": 7,
            "is_core": True,
            "complexity_ceiling": 4,
            "course_outcomes": [
                "Train and deploy real-time object detection models (YOLO) for road damage and garbage verification.",
                "Design distributed edge IoT sensor architectures for smart municipal monitoring.",
                "Deliver production-ready, secure, scalable civic software systems with CI/CD."
            ],
            "units": [
                "Unit 1: Deep Learning & Computer Vision - Convolutional networks, YOLO object detection, transfer learning",
                "Unit 2: Multimodal Systems - Fusing text, audio transcription (Whisper), and image evidence",
                "Unit 3: Edge Computing - ONNX runtime, TensorRT quantization, deploying on Raspberry Pi / mobile devices",
                "Unit 4: Capstone Engineering Project - End-to-end autonomous civic inspection system"
            ]
        }
    ]
}

AICTE_ENVIRONMENTAL_ENGG: Dict[str, Any] = {
    "department": "Environmental Engineering & Science",
    "degree": "B.Tech",
    "curriculum_standard": "AICTE Model Curriculum 2024",
    "subjects": [
        # Year 1 (Foundation)
        {
            "subject_code": "ENV-101",
            "subject_name": "Environmental Ecology and Solid Waste Basics",
            "academic_year": 1,
            "semester": 1,
            "is_core": True,
            "complexity_ceiling": 1,
            "course_outcomes": [
                "Identify common urban pollutants, open dumping hazards, and municipal waste types.",
                "Conduct door-to-door community surveys on plastic usage and wet/dry waste segregation.",
                "Draft civic awareness materials for clean ward initiatives."
            ],
            "units": [
                "Unit 1: Municipal Solid Waste Categories - Biodegradable, recyclable, domestic hazardous waste",
                "Unit 2: Public Health & Sanitation - Vectors, open drain illnesses, odor complaints",
                "Unit 3: Community Surveys - Field data collection, citizen compliance interviews",
                "Unit 4: Action Campaign Design - Zero-waste events, ward cleanliness drives"
            ]
        },
        # Year 2 (Applied Monitoring)
        {
            "subject_code": "ENV-201",
            "subject_name": "Water and Air Quality Analysis",
            "academic_year": 2,
            "semester": 3,
            "is_core": True,
            "complexity_ceiling": 2,
            "course_outcomes": [
                "Measure water quality metrics (pH, turbidity, dissolved oxygen, fecal coliforms) in municipal supply.",
                "Monitor ambient particulate matter (PM2.5, PM10) near waste burning and construction sites.",
                "Prepare water contamination audit reports for municipal health officers."
            ],
            "units": [
                "Unit 1: Water Quality Standards - BIS 10500 drinking water norms, standard laboratory titration",
                "Unit 2: Air Pollution Monitoring - High volume air samplers, sensor calibration, AQI computation",
                "Unit 3: Contamination Tracing - Identifying sewage ingress in potable water pipes",
                "Unit 4: Lab Practical Project - Ward-level drinking water quality mapping"
            ]
        },
        # Year 3 (Municipal Treatment Systems)
        {
            "subject_code": "ENV-301",
            "subject_name": "Solid Waste Management and Sewage Engineering",
            "academic_year": 3,
            "semester": 5,
            "is_core": True,
            "complexity_ceiling": 3,
            "course_outcomes": [
                "Design decentralized composting plants and material recovery facilities (MRF) for municipal wards.",
                "Audit municipal leachate generation, landfill gas emissions, and leachate treatment methods.",
                "Design biological wastewater reactors (MBBR, SBR) for municipal effluent treatment."
            ],
            "units": [
                "Unit 1: Solid Waste Processing - Shredding, trommel screening, aerobic windrow composting",
                "Unit 2: Sanitary Landfills - Liner systems, leachate collection, gas migration barriers",
                "Unit 3: Decentralized Sewage Systems - Septic tanks, soak pits, constructed wetlands",
                "Unit 4: Design Project - Ward-scale 10-TPD integrated solid waste processing facility"
            ]
        },
        # Year 4 (Advanced Remediation & Capstone)
        {
            "subject_code": "ENV-401",
            "subject_name": "Hazardous Waste Remediation and Environmental Capstone",
            "academic_year": 4,
            "semester": 7,
            "is_core": True,
            "complexity_ceiling": 4,
            "course_outcomes": [
                "Formulate bioremediation strategies for heavy metals and industrial effluent contaminated soil.",
                "Perform Environmental Impact Assessment (EIA) for municipal infrastructure projects.",
                "Deliver an innovative, patentable municipal waste valorization solution."
            ],
            "units": [
                "Unit 1: Advanced Remediation - Bioventing, phytoremediation, chemical oxidation of contaminated drain sludge",
                "Unit 2: Circular Economy - Refuse Derived Fuel (RDF), pyrolysis of single-use plastics",
                "Unit 3: Environmental Audit & EIA - Public hearing regulations, pollution control board compliances",
                "Unit 4: Capstone Engineering Project - Zero liquid discharge system for urban commercial zones"
            ]
        }
    ]
}

SAMPLE_SYLLABI: Dict[str, Dict[str, Any]] = {
    "civil_engineering": AICTE_CIVIL_ENGINEERING,
    "computer_science": AICTE_COMPUTER_SCIENCE,
    "environmental_engineering": AICTE_ENVIRONMENTAL_ENGG
}
