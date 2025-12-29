import json
import re

def normalize(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

target_exercises = [
    "Wall Sit",
    "Pushup",
    "Russian Twists",
    "Plank",
    "Jumping Jacks",
    "Lunges",
    "Squats",
    "Burpees",
    "High Knees",
    "Mountain Climbers",
    "Leg Raises",
    "Bicycle Crunches",
    "Tricep Dips",
    "Step-Ups",
    "Calf Raises",
    "Side Plank",
    "Arm Circles",
    "Glute Bridges",
    "Flutter Kicks",
    "Superman",
    "Sit-Ups",
    "Jump Squats",
    "Inchworm",
    "Butt Kicks",
    "Side Lunges"
]

# Load data
with open('/Users/pasmllr/Code/ski-workout-plan/exercises_data.json', 'r') as f:
    data = json.load(f)

# Create a mapping of normalized title to item
db_map = {}
for item in data:
    norm_title = normalize(item['title'])
    db_map[norm_title] = item

results = {}

for target in target_exercises:
    norm_target = normalize(target)
    
    match = None
    
    # 1. Exact normalized match
    if norm_target in db_map:
        match = db_map[norm_target]
    
    # 2. Try singular/plural variations
    if not match:
        if norm_target.endswith('s') and norm_target[:-1] in db_map:
            match = db_map[norm_target[:-1]]
        elif (norm_target + 's') in db_map:
            match = db_map[norm_target + 's']

    # 3. Search for substring matches if no exact match
    if not match:
        candidates = []
        for item in data:
            item_norm = normalize(item['title'])
            # Check if target is in item title (e.g. "Squat" in "Bodyweight Squat")
            # OR item title is in target (e.g. "Push-up" in "Pushups")
            if norm_target in item_norm: 
                candidates.append(item)
            elif item_norm in norm_target:
                candidates.append(item)
        
        if candidates:
            # Sort by length of title to find the most specific match
            # e.g. prefer "Squat" over "Dumbbell Squat"
            candidates.sort(key=lambda x: len(x['title']))
            match = candidates[0]

    if match:
        results[target] = match['src']
    else:
        results[target] = None

print(json.dumps(results, indent=2))
