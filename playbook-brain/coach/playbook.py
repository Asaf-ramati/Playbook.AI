PLAYBOOK = {
    "PNR_TOP_CENTRAL": {
        "name": "Central Pick and Roll",
        "description": "Central pick and roll: The point guard and center work together at the top of the arc.",
        "steps": [
            [ # Step 1: Alignment
                {"id": "PG", "x": 400, "y": 420}, {"id": "C", "x": 380, "y": 300},
                {"id": "SG", "x": 700, "y": 100}, {"id": "SF", "x": 100, "y": 100},
                {"id": "PF", "x": 600, "y": 50},  {"id": "ball", "x": 400, "y": 420}
            ],
            [ # Step 2: The Screen
                {"id": "PG", "x": 400, "y": 420}, {"id": "C", "x": 420, "y": 410}, # Center sets screen for PG
                {"id": "SG", "x": 720, "y": 80},  {"id": "SF", "x": 80, "y": 80},
                {"id": "PF", "x": 600, "y": 50},  {"id": "ball", "x": 400, "y": 420}
            ],
            [ # Step 3: Roll and Drive
                {"id": "PG", "x": 300, "y": 250}, {"id": "C", "x": 400, "y": 100}, # PG drives left, Center rolls to basket
                {"id": "SG", "x": 750, "y": 50},  {"id": "SF", "x": 50, "y": 50},
                {"id": "PF", "x": 620, "y": 50},  {"id": "ball", "x": 300, "y": 250}
            ]
        ]
    }
}