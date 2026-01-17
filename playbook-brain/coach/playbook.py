PLAYBOOK = {
    # --- GROUP 1: PICK AND ROLL VARIATIONS (1-10) ---
    
    "PNR_TOP_CENTRAL": {
        "name": "Central Pick and Roll",
        "description": "פיק אנד רול מרכזי קלאסי בראש הקשת. הסנטר עולה לחסום, הרכז חודר.",
        "steps": [
            [ # Step 1: Alignment & Screen
                {"id": "team1-pg", "x": 400, "y": 420}, {"id": "team1-sg", "x": 700, "y": 100},
                {"id": "team1-sf", "x": 100, "y": 100}, {"id": "team1-pf", "x": 600, "y": 100},
                {"id": "team1-c", "x": 420, "y": 400},  {"id": "ball", "x": 400, "y": 420}
            ],
            [ # Step 2: Drive and Roll
                {"id": "team1-pg", "x": 350, "y": 200}, {"id": "team1-sg", "x": 720, "y": 80},
                {"id": "team1-sf", "x": 80, "y": 80},   {"id": "team1-pf", "x": 600, "y": 100},
                {"id": "team1-c", "x": 400, "y": 100},  {"id": "ball", "x": 350, "y": 200}
            ]
        ]
    },
    "PNR_WING_RIGHT": {
        "name": "Wing PNR Right",
        "description": "פיק אנד רול בכנף ימין. מרווח את הצד החלש לקליעה.",
        "steps": [
            [ # Step 1: Set Screen on Wing
                {"id": "team1-pg", "x": 650, "y": 350}, {"id": "team1-c", "x": 670, "y": 340},
                {"id": "team1-sg", "x": 150, "y": 300}, {"id": "team1-sf", "x": 100, "y": 100},
                {"id": "team1-pf", "x": 400, "y": 100}, {"id": "ball", "x": 650, "y": 350}
            ],
            [ # Step 2: Drive Middle
                {"id": "team1-pg", "x": 500, "y": 200}, {"id": "team1-c", "x": 550, "y": 100},
                {"id": "team1-sg", "x": 150, "y": 300}, {"id": "team1-sf", "x": 100, "y": 100},
                {"id": "team1-pf", "x": 250, "y": 100}, {"id": "ball", "x": 500, "y": 200}
            ]
        ]
    },
    "PNR_WING_LEFT": {
        "name": "Wing PNR Left",
        "description": "פיק אנד רול בכנף שמאל. הסנטר חוסם לכיוון האמצע.",
        "steps": [
            [ # Step 1: Set Screen
                {"id": "team1-pg", "x": 150, "y": 350}, {"id": "team1-c", "x": 130, "y": 340},
                {"id": "team1-sg", "x": 650, "y": 300}, {"id": "team1-sf", "x": 700, "y": 100},
                {"id": "team1-pf", "x": 400, "y": 100}, {"id": "ball", "x": 150, "y": 350}
            ],
            [ # Step 2: Execution
                {"id": "team1-pg", "x": 300, "y": 200}, {"id": "team1-c", "x": 250, "y": 100},
                {"id": "team1-sg", "x": 650, "y": 300}, {"id": "team1-sf", "x": 700, "y": 100},
                {"id": "team1-pf", "x": 550, "y": 100}, {"id": "ball", "x": 300, "y": 200}
            ]
        ]
    },
    "PNR_SPANISH": {
        "name": "Spanish Pick and Roll",
        "description": "מהלך ספרדי: חסימה לרכז, ואז חסימה גבית לחוסם המתגלגל.",
        "steps": [
            [ # Step 1: High Screen
                {"id": "team1-pg", "x": 400, "y": 400}, {"id": "team1-c", "x": 420, "y": 380},
                {"id": "team1-sg", "x": 400, "y": 250}, {"id": "team1-sf", "x": 100, "y": 100},
                {"id": "team1-pf", "x": 700, "y": 100}, {"id": "ball", "x": 400, "y": 400}
            ],
            [ # Step 2: Roll and Back Screen
                {"id": "team1-pg", "x": 350, "y": 250}, {"id": "team1-c", "x": 400, "y": 150},
                {"id": "team1-sg", "x": 410, "y": 200}, {"id": "team1-sf", "x": 100, "y": 100},
                {"id": "team1-pf", "x": 700, "y": 100}, {"id": "ball", "x": 350, "y": 250}
            ]
        ]
    },
    "PNR_DOUBLE_DRAG": {
        "name": "Double Drag Screens",
        "description": "שתי חסימות מדורגות במעבר להתקפה.",
        "steps": [
            [ # Step 1: Transition Screens
                {"id": "team1-pg", "x": 500, "y": 450}, {"id": "team1-c", "x": 480, "y": 400},
                {"id": "team1-pf", "x": 450, "y": 380}, {"id": "team1-sg", "x": 100, "y": 100},
                {"id": "team1-sf", "x": 700, "y": 100}, {"id": "ball", "x": 500, "y": 450}
            ],
            [ # Step 2: Attack
                {"id": "team1-pg", "x": 300, "y": 250}, {"id": "team1-c", "x": 400, "y": 50},
                {"id": "team1-pf", "x": 400, "y": 400}, {"id": "team1-sg", "x": 100, "y": 100},
                {"id": "team1-sf", "x": 700, "y": 100}, {"id": "ball", "x": 300, "y": 250}
            ]
        ]
    },
    "PNR_CORNER_STEP_UP": {
        "name": "Corner Step-Up PNR",
        "description": "חסימה בגב ההגנה ליד הפינה כדי לאפשר חדירה על קו הבסיס.",
        "steps": [
            [ # Step 1: Step Up
                {"id": "team1-pg", "x": 700, "y": 100}, {"id": "team1-c", "x": 680, "y": 120},
                {"id": "team1-sg", "x": 400, "y": 400}, {"id": "team1-sf", "x": 100, "y": 300},
                {"id": "team1-pf", "x": 100, "y": 100}, {"id": "ball", "x": 700, "y": 100}
            ],
            [ # Step 2: Baseline Drive
                {"id": "team1-pg", "x": 550, "y": 60},  {"id": "team1-c", "x": 600, "y": 200},
                {"id": "team1-sg", "x": 450, "y": 350}, {"id": "team1-sf", "x": 100, "y": 300},
                {"id": "team1-pf", "x": 200, "y": 100}, {"id": "ball", "x": 550, "y": 60}
            ]
        ]
    },
    "PNR_GHOST_SCREEN": {
        "name": "Ghost Screen PNR",
        "description": "חסימה מדומה בה החוסם בורח החוצה לקליעה לפני המגע.",
        "steps": [
            [ # Step 1: Approach
                {"id": "team1-pg", "x": 400, "y": 400}, {"id": "team1-sg", "x": 300, "y": 350},
                {"id": "team1-c", "x": 400, "y": 100},  {"id": "team1-sf", "x": 700, "y": 100},
                {"id": "team1-pf", "x": 100, "y": 100}, {"id": "ball", "x": 400, "y": 400}
            ],
            [ # Step 2: Slip/Ghost
                {"id": "team1-pg", "x": 500, "y": 300}, {"id": "team1-sg", "x": 200, "y": 380},
                {"id": "team1-c", "x": 400, "y": 100},  {"id": "team1-sf", "x": 700, "y": 100},
                {"id": "team1-pf", "x": 100, "y": 100}, {"id": "ball", "x": 500, "y": 300}
            ]
        ]
    },
    "PNR_PISTOL_ACTION": {
        "name": "Pistol / 21 Action",
        "description": "מסירה ידנית (DHO) בכנף שהופכת לחסימה.",
        "steps": [
            [ # Step 1: Dribble Hand Off
                {"id": "team1-pg", "x": 600, "y": 350}, {"id": "team1-sg", "x": 650, "y": 300},
                {"id": "team1-c", "x": 400, "y": 100},  {"id": "team1-sf", "x": 100, "y": 300},
                {"id": "team1-pf", "x": 100, "y": 100}, {"id": "ball", "x": 600, "y": 350}
            ],
            [ # Step 2: Drive off DHO
                {"id": "team1-pg", "x": 620, "y": 320}, {"id": "team1-sg", "x": 500, "y": 250},
                {"id": "team1-c", "x": 400, "y": 100},  {"id": "team1-sf", "x": 100, "y": 300},
                {"id": "team1-pf", "x": 100, "y": 100}, {"id": "ball", "x": 500, "y": 250}
            ]
        ]
    },
    "PNR_SPREAD_HIGH": {
        "name": "Spread High PNR",
        "description": "פיק אנד רול גבוה כאשר כל שאר השחקנים מרווחים על קשת השלוש.",
        "steps": [
            [ # Step 1: Spacing
                {"id": "team1-pg", "x": 400, "y": 420}, {"id": "team1-c", "x": 420, "y": 400},
                {"id": "team1-sg", "x": 750, "y": 50},  {"id": "team1-sf", "x": 50, "y": 50},
                {"id": "team1-pf", "x": 700, "y": 300}, {"id": "ball", "x": 400, "y": 420}
            ],
            [ # Step 2: Downhill Drive
                {"id": "team1-pg", "x": 400, "y": 150}, {"id": "team1-c", "x": 400, "y": 350},
                {"id": "team1-sg", "x": 750, "y": 50},  {"id": "team1-sf", "x": 50, "y": 50},
                {"id": "team1-pf", "x": 700, "y": 300}, {"id": "ball", "x": 400, "y": 150}
            ]
        ]
    },
    "PNR_REJECT": {
        "name": "Reject Screen PNR",
        "description": "הרכז מסרב לקחת את החסימה וחותך לצד השני.",
        "steps": [
            [ # Step 1: Setup Screen
                {"id": "team1-pg", "x": 400, "y": 400}, {"id": "team1-c", "x": 420, "y": 390},
                {"id": "team1-sg", "x": 700, "y": 100}, {"id": "team1-sf", "x": 100, "y": 300},
                {"id": "team1-pf", "x": 100, "y": 100}, {"id": "ball", "x": 400, "y": 400}
            ],
            [ # Step 2: Reject
                {"id": "team1-pg", "x": 300, "y": 200}, {"id": "team1-c", "x": 420, "y": 390},
                {"id": "team1-sg", "x": 700, "y": 100}, {"id": "team1-sf", "x": 100, "y": 300},
                {"id": "team1-pf", "x": 100, "y": 100}, {"id": "ball", "x": 300, "y": 200}
            ]
        ]
    },

    # --- GROUP 2: MOTION & OFF-BALL SCREENS (11-20) ---
    
    "MOTION_FLARE": {
        "name": "Flare Screen",
        "description": "חסימה רחוקה מהכדור לשחרור קלע בכנף הנגדית.",
        "steps": [
            [ # Step 1: Pass and Screen
                {"id": "team1-pg", "x": 400, "y": 400}, {"id": "team1-sg", "x": 200, "y": 350},
                {"id": "team1-sf", "x": 600, "y": 350}, {"id": "team1-c", "x": 500, "y": 350},
                {"id": "team1-pf", "x": 100, "y": 100}, {"id": "ball", "x": 200, "y": 350}
            ],
            [ # Step 2: Fade to Corner/Wing
                {"id": "team1-pg", "x": 400, "y": 400}, {"id": "team1-sg", "x": 200, "y": 350},
                {"id": "team1-sf", "x": 750, "y": 200}, {"id": "team1-c", "x": 650, "y": 300},
                {"id": "team1-pf", "x": 100, "y": 100}, {"id": "ball", "x": 200, "y": 350}
            ]
        ]
    },
    "MOTION_PIN_DOWN": {
        "name": "Pin Down Screen",
        "description": "חסימה לכיוון קו הבסיס כדי לשחרר שחקן לקבלת כדור למעלה.",
        "steps": [
            [ # Step 1: Set Pin Down
                {"id": "team1-pg", "x": 400, "y": 400}, {"id": "team1-sg", "x": 100, "y": 50},
                {"id": "team1-c", "x": 100, "y": 150},  {"id": "team1-sf", "x": 700, "y": 300},
                {"id": "team1-pf", "x": 700, "y": 100}, {"id": "ball", "x": 400, "y": 400}
            ],
            [ # Step 2: Curl Up
                {"id": "team1-pg", "x": 300, "y": 350}, {"id": "team1-sg", "x": 150, "y": 300},
                {"id": "team1-c", "x": 100, "y": 100},  {"id": "team1-sf", "x": 700, "y": 300},
                {"id": "team1-pf", "x": 700, "y": 100}, {"id": "ball", "x": 300, "y": 350}
            ]
        ]
    },
    "MOTION_BACKDOOR": {
        "name": "Backdoor Cut",
        "description": "הטעיה החוצה וחיתוך מהיר לסל מאחורי הגב של המגן.",
        "steps": [
            [ # Step 1: Fake High
                {"id": "team1-pg", "x": 300, "y": 350}, {"id": "team1-sg", "x": 700, "y": 300},
                {"id": "team1-c", "x": 550, "y": 250},  {"id": "team1-sf", "x": 100, "y": 100},
                {"id": "team1-pf", "x": 400, "y": 100}, {"id": "ball", "x": 300, "y": 350}
            ],
            [ # Step 2: Cut to Rim
                {"id": "team1-pg", "x": 300, "y": 350}, {"id": "team1-sg", "x": 550, "y": 50},
                {"id": "team1-c", "x": 550, "y": 250},  {"id": "team1-sf", "x": 100, "y": 100},
                {"id": "team1-pf", "x": 400, "y": 100}, {"id": "ball", "x": 550, "y": 50}
            ]
        ]
    },
    "MOTION_PRINCETON_CHIN": {
        "name": "Princeton Chin Cut",
        "description": "חיתוך צ'ין מסורתי על חסימה גבית בפוסט הגבוה.",
        "steps": [
            [ # Step 1: Dribble at Wing
                {"id": "team1-pg", "x": 400, "y": 400}, {"id": "team1-sg", "x": 650, "y": 350},
                {"id": "team1-c", "x": 550, "y": 250},  {"id": "team1-sf", "x": 100, "y": 300},
                {"id": "team1-pf", "x": 100, "y": 100}, {"id": "ball", "x": 400, "y": 400}
            ],
            [ # Step 2: Back Screen and Cut
                {"id": "team1-pg", "x": 400, "y": 100}, {"id": "team1-sg", "x": 600, "y": 300},
                {"id": "team1-c", "x": 550, "y": 250},  {"id": "team1-sf", "x": 100, "y": 300},
                {"id": "team1-pf", "x": 100, "y": 100}, {"id": "ball", "x": 600, "y": 300}
            ]
        ]
    },
    "MOTION_UCLA_CUT": {
        "name": "UCLA Cut",
        "description": "מסירה לכנף וחיתוך על חסימה של הפוסט הגבוה.",
        "steps": [
            [ # Step 1: Pass to Wing
                {"id": "team1-pg", "x": 400, "y": 400}, {"id": "team1-sg", "x": 650, "y": 350},
                {"id": "team1-c", "x": 500, "y": 250},  {"id": "team1-sf", "x": 100, "y": 300},
                {"id": "team1-pf", "x": 200, "y": 100}, {"id": "ball", "x": 650, "y": 350}
            ],
            [ # Step 2: UCLA Screen
                {"id": "team1-pg", "x": 500, "y": 100}, {"id": "team1-sg", "x": 650, "y": 350},
                {"id": "team1-c", "x": 500, "y": 250},  {"id": "team1-sf", "x": 100, "y": 300},
                {"id": "team1-pf", "x": 200, "y": 100}, {"id": "ball", "x": 650, "y": 350}
            ]
        ]
    },
    "MOTION_IVERSON_CUT": {
        "name": "Iverson Cut",
        "description": "חיתוך רוחבי מקצה לקצה מעל קו העונשין.",
        "steps": [
            [ # Step 1: Setup
                {"id": "team1-pg", "x": 400, "y": 420}, {"id": "team1-sg", "x": 100, "y": 300},
                {"id": "team1-c", "x": 250, "y": 250},  {"id": "team1-pf", "x": 550, "y": 250},
                {"id": "team1-sf", "x": 750, "y": 100}, {"id": "ball", "x": 400, "y": 420}
            ],
            [ # Step 2: The Cut
                {"id": "team1-pg", "x": 400, "y": 420}, {"id": "team1-sg", "x": 700, "y": 300},
                {"id": "team1-c", "x": 250, "y": 250},  {"id": "team1-pf", "x": 550, "y": 250},
                {"id": "team1-sf", "x": 750, "y": 100}, {"id": "ball", "x": 400, "y": 420}
            ]
        ]
    },
    "MOTION_STAGGER": {
        "name": "Staggered Screens",
        "description": "שתי חסימות עוקבות לשחקן אחד כדי לשחרר אותו לקליעה.",
        "steps": [
            [ # Step 1: Screens Set
                {"id": "team1-pg", "x": 500, "y": 400}, {"id": "team1-sg", "x": 100, "y": 100},
                {"id": "team1-sf", "x": 200, "y": 200}, {"id": "team1-c", "x": 300, "y": 300},
                {"id": "team1-pf", "x": 700, "y": 100}, {"id": "ball", "x": 500, "y": 400}
            ],
            [ # Step 2: Runner
                {"id": "team1-pg", "x": 500, "y": 400}, {"id": "team1-sg", "x": 400, "y": 420},
                {"id": "team1-sf", "x": 200, "y": 200}, {"id": "team1-c", "x": 300, "y": 300},
                {"id": "team1-pf", "x": 700, "y": 100}, {"id": "ball", "x": 400, "y": 420}
            ]
        ]
    },
    "MOTION_FLEX": {
        "name": "Flex Action",
        "description": "חסימת רוחב בקו הבסיס ואז חסימה מדורגת (Down Screen).",
        "steps": [
            [ # Step 1: Flex Screen
                {"id": "team1-pg", "x": 400, "y": 420}, {"id": "team1-sg", "x": 700, "y": 100},
                {"id": "team1-sf", "x": 100, "y": 100}, {"id": "team1-c", "x": 250, "y": 100},
                {"id": "team1-pf", "x": 400, "y": 400}, {"id": "ball", "x": 400, "y": 420}
            ],
            [ # Step 2: Cut
                {"id": "team1-pg", "x": 400, "y": 420}, {"id": "team1-sg", "x": 250, "y": 100},
                {"id": "team1-sf", "x": 100, "y": 100}, {"id": "team1-c", "x": 250, "y": 100},
                {"id": "team1-pf", "x": 400, "y": 400}, {"id": "ball", "x": 250, "y": 100}
            ]
        ]
    },
    "MOTION_ZIPPER": {
        "name": "Zipper Cut",
        "description": "חיתוך אנכי מלמטה למעלה דרך הצבע לקבלת כדור.",
        "steps": [
            [ # Step 1: Down Screen
                {"id": "team1-pg", "x": 600, "y": 350}, {"id": "team1-sg", "x": 200, "y": 50},
                {"id": "team1-c", "x": 200, "y": 200},  {"id": "team1-sf", "x": 700, "y": 100},
                {"id": "team1-pf", "x": 400, "y": 100}, {"id": "ball", "x": 600, "y": 350}
            ],
            [ # Step 2: Zip Up
                {"id": "team1-pg", "x": 600, "y": 350}, {"id": "team1-sg", "x": 200, "y": 380},
                {"id": "team1-c", "x": 200, "y": 200},  {"id": "team1-sf", "x": 700, "y": 100},
                {"id": "team1-pf", "x": 400, "y": 100}, {"id": "ball", "x": 200, "y": 380}
            ]
        ]
    },
    "MOTION_ELEVATOR": {
        "name": "Elevator / Doors",
        "description": "קלע רץ בין שני חוסמים שסוגרים את המרווח מיד אחריו.",
        "steps": [
            [ # Step 1: Run Through
                {"id": "team1-pg", "x": 400, "y": 420}, {"id": "team1-sg", "x": 400, "y": 50},
                {"id": "team1-c", "x": 350, "y": 250},  {"id": "team1-pf", "x": 450, "y": 250},
                {"id": "team1-sf", "x": 700, "y": 100}, {"id": "ball", "x": 400, "y": 420}
            ],
            [ # Step 2: Close Doors
                {"id": "team1-pg", "x": 400, "y": 420}, {"id": "team1-sg", "x": 400, "y": 380},
                {"id": "team1-c", "x": 380, "y": 250},  {"id": "team1-pf", "x": 420, "y": 250},
                {"id": "team1-sf", "x": 700, "y": 100}, {"id": "ball", "x": 400, "y": 380}
            ]
        ]
    },

    # --- GROUP 3: ZONE OVERLOAD & SPECIAL SETS (21-30) ---
    
    "ZONE_OVERLOAD_RIGHT": {
        "name": "Zone Overload Right",
        "description": "העמסת צד ימין נגד הגנה אזורית ליצירת יתרון מספרי.",
        "steps": [
            [ # Step 1: Setup Overload
                {"id": "team1-pg", "x": 500, "y": 380}, {"id": "team1-sg", "x": 700, "y": 300},
                {"id": "team1-sf", "x": 750, "y": 50},  {"id": "team1-pf", "x": 550, "y": 100},
                {"id": "team1-c", "x": 200, "y": 300},  {"id": "ball", "x": 500, "y": 380}
            ]
        ]
    },
    "SET_TRIANGLE_POST": {
        "name": "Triangle Post Entry",
        "description": "כניסה להתקפת המשולש עם מסירה לפוסט.",
        "steps": [
            [ # Step 1: Form Triangle
                {"id": "team1-pg", "x": 600, "y": 350}, {"id": "team1-sg", "x": 750, "y": 50},
                {"id": "team1-c", "x": 650, "y": 100},  {"id": "team1-sf", "x": 200, "y": 300},
                {"id": "team1-pf", "x": 300, "y": 400}, {"id": "ball", "x": 600, "y": 350}
            ],
            [ # Step 2: Entry Pass
                {"id": "team1-pg", "x": 650, "y": 250}, {"id": "team1-sg", "x": 750, "y": 50},
                {"id": "team1-c", "x": 650, "y": 100},  {"id": "team1-sf", "x": 200, "y": 300},
                {"id": "team1-pf", "x": 300, "y": 400}, {"id": "ball", "x": 650, "y": 100}
            ]
        ]
    },
    "SET_BOX_CROSS": {
        "name": "Box Set Cross Screen",
        "description": "מערך קופסא עם חסימות אלכסוניות לגבוהים.",
        "steps": [
            [ # Step 1: Box Formation
                {"id": "team1-pg", "x": 400, "y": 400}, {"id": "team1-sg", "x": 250, "y": 100},
                {"id": "team1-sf", "x": 550, "y": 100}, {"id": "team1-pf", "x": 250, "y": 250},
                {"id": "team1-c", "x": 550, "y": 250},  {"id": "ball", "x": 400, "y": 400}
            ],
            [ # Step 2: Cross Screen
                {"id": "team1-pg", "x": 400, "y": 400}, {"id": "team1-sg", "x": 550, "y": 100},
                {"id": "team1-sf", "x": 250, "y": 100}, {"id": "team1-pf", "x": 250, "y": 250},
                {"id": "team1-c", "x": 550, "y": 250},  {"id": "ball", "x": 400, "y": 400}
            ]
        ]
    },
    "SET_HORNS_MAIN": {
        "name": "Horns Set",
        "description": "מערך קרניים: שני גבוהים בפוסט הגבוה, קלעים בפינות.",
        "steps": [
            [ # Step 1: Setup
                {"id": "team1-pg", "x": 400, "y": 420}, {"id": "team1-c", "x": 300, "y": 350},
                {"id": "team1-pf", "x": 500, "y": 350}, {"id": "team1-sg", "x": 750, "y": 50},
                {"id": "team1-sf", "x": 50, "y": 50},   {"id": "ball", "x": 400, "y": 420}
            ]
        ]
    },
    "SET_HORNS_TWIST": {
        "name": "Horns Twist",
        "description": "חסימה לצד אחד, שינוי כיוון וחסימה חוזרת מהגבוה השני.",
        "steps": [
            [ # Step 1: First Screen Left
                {"id": "team1-pg", "x": 350, "y": 400}, {"id": "team1-c", "x": 320, "y": 380},
                {"id": "team1-pf", "x": 500, "y": 350}, {"id": "team1-sg", "x": 750, "y": 50},
                {"id": "team1-sf", "x": 50, "y": 50},   {"id": "ball", "x": 350, "y": 400}
            ],
            [ # Step 2: Twist Right
                {"id": "team1-pg", "x": 450, "y": 300}, {"id": "team1-c", "x": 300, "y": 350},
                {"id": "team1-pf", "x": 480, "y": 320}, {"id": "team1-sg", "x": 750, "y": 50},
                {"id": "team1-sf", "x": 50, "y": 50},   {"id": "ball", "x": 450, "y": 300}
            ]
        ]
    },
    "SET_ISO_TOP": {
        "name": "Isolation Top",
        "description": "בידוד לרכז בראש הקשת, כולם משכו למטה ורחוק.",
        "steps": [
            [ # Step 1: Clear Out
                {"id": "team1-pg", "x": 400, "y": 400}, {"id": "team1-sg", "x": 750, "y": 50},
                {"id": "team1-sf", "x": 50, "y": 50},   {"id": "team1-pf", "x": 700, "y": 150},
                {"id": "team1-c", "x": 100, "y": 150},  {"id": "ball", "x": 400, "y": 400}
            ]
        ]
    },
    "SET_HAWK": {
        "name": "Hawk Offense",
        "description": "התקפת הוק: חיתוך מעל פוסט גבוה בצד החזק.",
        "steps": [
            [ # Step 1: Dribble Entry
                {"id": "team1-pg", "x": 550, "y": 350}, {"id": "team1-sg", "x": 200, "y": 300},
                {"id": "team1-c", "x": 550, "y": 250},  {"id": "team1-pf", "x": 400, "y": 100},
                {"id": "team1-sf", "x": 100, "y": 100}, {"id": "ball", "x": 550, "y": 350}
            ]
        ]
    },
    "BLOB_STACK": {
        "name": "Baseline Out of Bounds Stack",
        "description": "הוצאת חוץ מתחת לסל: ערימה (Stack) מול המוסר.",
        "steps": [
            [ # Step 1: Stack Formation
                {"id": "team1-pg", "x": 450, "y": 20},  {"id": "team1-sg", "x": 400, "y": 100},
                {"id": "team1-sf", "x": 400, "y": 130}, {"id": "team1-pf", "x": 400, "y": 160},
                {"id": "team1-c", "x": 400, "y": 190},  {"id": "ball", "x": 450, "y": 20}
            ],
            [ # Step 2: Break Stack
                {"id": "team1-pg", "x": 450, "y": 20},  {"id": "team1-sg", "x": 700, "y": 50},
                {"id": "team1-sf", "x": 100, "y": 50},  {"id": "team1-pf", "x": 450, "y": 100},
                {"id": "team1-c", "x": 400, "y": 250},  {"id": "ball", "x": 450, "y": 100}
            ]
        ]
    },
    "SLOB_ZIPPER": {
        "name": "Sideline OB Zipper",
        "description": "הוצאת חוץ מהצד: חיתוך זיפר לקבלת הכדור.",
        "steps": [
            [ # Step 1: Inbound Setup
                {"id": "team1-pg", "x": 800, "y": 350}, {"id": "team1-sg", "x": 400, "y": 100},
                {"id": "team1-c", "x": 400, "y": 250},  {"id": "team1-sf", "x": 100, "y": 300},
                {"id": "team1-pf", "x": 200, "y": 100}, {"id": "ball", "x": 800, "y": 350}
            ],
            [ # Step 2: Receive Ball
                {"id": "team1-pg", "x": 800, "y": 350}, {"id": "team1-sg", "x": 400, "y": 350},
                {"id": "team1-c", "x": 400, "y": 250},  {"id": "team1-sf", "x": 100, "y": 300},
                {"id": "team1-pf", "x": 200, "y": 100}, {"id": "ball", "x": 400, "y": 350}
            ]
        ]
    },
    "SET_5_OUT": {
        "name": "5 Out Pass & Cut",
        "description": "התקפה ללא גבוהים בצבע. כולם בחוץ, מסירה וחיתוך.",
        "steps": [
            [ # Step 1: 5 Out Spacing
                {"id": "team1-pg", "x": 400, "y": 420}, {"id": "team1-sg", "x": 700, "y": 300},
                {"id": "team1-sf", "x": 100, "y": 300}, {"id": "team1-pf", "x": 750, "y": 50},
                {"id": "team1-c", "x": 50, "y": 50},    {"id": "ball", "x": 400, "y": 420}
            ],
            [ # Step 2: Pass and Cut
                {"id": "team1-pg", "x": 400, "y": 50},  {"id": "team1-sg", "x": 700, "y": 300},
                {"id": "team1-sf", "x": 100, "y": 300}, {"id": "team1-pf", "x": 750, "y": 50},
                {"id": "team1-c", "x": 50, "y": 50},    {"id": "ball", "x": 700, "y": 300}
            ]
        ]
    }
}