"""
Team Allocation - ENHANCED ALGORITHM (Team Sizes 4-10)
Implements adaptive gender + STEM balance with flexible team sizes
"""

import random

# ============================================================================
# STEM SCHOOL CONFIGURATION
# ============================================================================
STEM_SCHOOLS = [
    "CCDS",
    "CCEB",
    "CoE",
    "EEE",
    "MAE",
    "SPMS",
    "SBS",
    "MSE",
    "CEE"
]

# ============================================================================
# ADAPTIVE BALANCE FUNCTIONS
# ============================================================================

def calculate_adaptive_threshold(students, team_size):
    """Calculate adaptive thresholds for gender and STEM balance."""
    male = 0
    female = 0
    stem = 0
    nonstem = 0
    
    for s in students:
        if s['gender'].upper() in ['M', 'MALE']:
            male += 1
        else:
            female += 1
        
        if s['school'] in STEM_SCHOOLS:
            stem += 1
        else:
            nonstem += 1
    
    total = male + female
    if total == 0:
        return {'male_max': 3, 'female_max': 3, 'stem_max': 3, 'nonstem_max': 3}
    
    # Stricter ratio (10% tolerance)
    tolerance = 0.1
    male_ratio = male / total
    female_ratio = female / total
    stem_ratio = stem / total
    nonstem_ratio = nonstem / total
    
    male_max = int(team_size * min(male_ratio + tolerance, 1) + 0.5)
    female_max = int(team_size * min(female_ratio + tolerance, 1) + 0.5)
    stem_max = int(team_size * min(stem_ratio + tolerance, 1) + 0.5)
    nonstem_max = int(team_size * min(nonstem_ratio + tolerance, 1) + 0.5)
    
    return {
        'male_max': max(1, male_max),
        'female_max': max(1, female_max),
        'stem_max': max(1, stem_max),
        'nonstem_max': max(1, nonstem_max)
    }

def is_gender_balanced(team, thresholds):
    """Check if team meets gender balance criteria."""
    male, female = count_gender(team)
    return male <= thresholds['male_max'] and female <= thresholds['female_max']

def is_stem_balanced(team, thresholds):
    """Check if team meets STEM/non-STEM balance criteria."""
    stem, nonstem = count_stem(team)
    return stem <= thresholds['stem_max'] and nonstem <= thresholds['nonstem_max']

def can_add_to_team(team, student, max_size, thresholds):
    """Check if student can be added without violating constraints."""
    if len(team) >= max_size:
        return False
    temp_team = team + [student]
    return (
        is_gender_balanced(temp_team, thresholds)
        and is_stem_balanced(temp_team, thresholds)
    )

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def count_gender(team):
    """Count males and females in a team."""
    male = 0
    female = 0
    for student in team:
        if student['gender'].upper() in ['M', 'MALE']:
            male += 1
        else:
            female += 1
    return male, female

def count_stem(team):
    """Count STEM and non-STEM students in a team."""
    stem = 0
    nonstem = 0
    for student in team:
        if student['school'] in STEM_SCHOOLS:
            stem += 1
        else:
            nonstem += 1
    return stem, nonstem

def read_csv_file(filename):
    """Read student records from CSV file."""
    students = []
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()
    
    for i in range(1, len(lines)):
        line = lines[i].strip()
        if not line:
            continue
        parts = line.split(',')
        student = {
            'tutorial': parts[0],
            'id': parts[1],
            'name': parts[2],
            'school': parts[3],
            'gender': parts[4],
            'cgpa': float(parts[5]),
            'team': 0
        }
        students.append(student)
    
    print("Loaded", len(students), "students")
    return students

def group_by_tutorial(students):
    """Group students by tutorial."""
    tutorials = {}
    for student in students:
        tut = student['tutorial']
        if tut not in tutorials:
            tutorials[tut] = []
        tutorials[tut].append(student)
    
    print("Found", len(tutorials), "tutorial groups")
    return tutorials

def select_high_cgpa(students):
    """Sort students by CGPA in descending order using insertion sort."""
    sorted_list = []
    for s in students:
        inserted = False
        for i in range(len(sorted_list)):
            if s['cgpa'] > sorted_list[i]['cgpa']:
                sorted_list = sorted_list[:i] + [s] + sorted_list[i:]
                inserted = True
                break
        if not inserted:
            sorted_list.append(s)
    return sorted_list

# ============================================================================
# TEAM FORMATION
# ============================================================================

def form_teams_adaptive(students, team_size):
    """
    Form teams with adaptive gender and STEM balance.
    
    Algorithm:
    1. Calculate adaptive thresholds for tutorial demographics
    2. Distribute STEM minority evenly first
    3. Distribute gender minority evenly
    4. Fill remaining spots with majority groups
    """
    if len(students) == 0:
        return []
    
    thresholds = calculate_adaptive_threshold(students, team_size)
    n = len(students)
    
    # Calculate number of teams
    num_teams = (n + team_size - 1) // team_size
    base_size = n // num_teams
    extra = n % num_teams
    
    team_targets = []
    for i in range(num_teams):
        if i < extra:
            team_targets.append(base_size + 1)
        else:
            team_targets.append(base_size)
    
    # Initialize empty teams
    teams = [[] for _ in range(num_teams)]
    
    # Split by STEM category
    stem_students = [s for s in students if s['school'] in STEM_SCHOOLS]
    nonstem_students = [s for s in students if s['school'] not in STEM_SCHOOLS]
    
    stem_sorted = select_high_cgpa(stem_students)
    nonstem_sorted = select_high_cgpa(nonstem_students)
    
    # Determine STEM minority and majority
    if len(stem_sorted) <= len(nonstem_sorted):
        stem_minority, stem_majority = stem_sorted, nonstem_sorted
    else:
        stem_minority, stem_majority = nonstem_sorted, stem_sorted
    
    # PHASE 0: Distribute STEM minority evenly
    for i, s in enumerate(stem_minority):
        idx = i % num_teams
        teams[idx].append(s)
    
    # Split by gender
    males = [s for s in students if s['gender'].upper() in ['M', 'MALE']]
    females = [s for s in students if s['gender'].upper() not in ['M', 'MALE']]
    
    males_sorted = select_high_cgpa(males)
    females_sorted = select_high_cgpa(females)
    
    # Determine gender minority and majority
    if len(males_sorted) <= len(females_sorted):
        minority, majority = males_sorted, females_sorted
    else:
        minority, majority = females_sorted, males_sorted
    
    # Randomization for diversity
    random.shuffle(majority)
    random.shuffle(stem_majority)
    
    # PHASE 1: Distribute gender minority evenly
    for i, s in enumerate(minority):
        idx = i % num_teams
        if s not in teams[idx]:  # Avoid duplicates
            teams[idx].append(s)
    
    # PHASE 2: Fill remaining spots with majority
    team_idx = 0
    for student in majority:
        # Skip if already placed
        already_placed = False
        for team in teams:
            if student in team:
                already_placed = True
                break
        if already_placed:
            continue
        
        placed = False
        for attempt in range(num_teams):
            idx = (team_idx + attempt) % num_teams
            if len(teams[idx]) < team_targets[idx] and can_add_to_team(teams[idx], student, team_targets[idx], thresholds):
                teams[idx].append(student)
                placed = True
                team_idx = (idx + 1) % num_teams
                break
        
        if not placed:
            # Fallback: team with most space
            best_idx = 0
            best_space = team_targets[0] - len(teams[0])
            for t in range(1, num_teams):
                space = team_targets[t] - len(teams[t])
                if space > best_space:
                    best_space = space
                    best_idx = t
            teams[best_idx].append(student)
            team_idx = (best_idx + 1) % num_teams
    
    # PHASE 3: Place any remaining STEM majority
    for student in stem_majority:
        # Skip if already placed
        already_placed = False
        for team in teams:
            if student in team:
                already_placed = True
                break
        if already_placed:
            continue
        
        placed = False
        for attempt in range(num_teams):
            idx = (team_idx + attempt) % num_teams
            if len(teams[idx]) < team_targets[idx] and can_add_to_team(teams[idx], student, team_targets[idx], thresholds):
                teams[idx].append(student)
                placed = True
                team_idx = (idx + 1) % num_teams
                break
        
        if not placed:
            # Fallback
            best_idx = 0
            best_space = team_targets[0] - len(teams[0])
            for t in range(1, num_teams):
                space = team_targets[t] - len(teams[t])
                if space > best_space:
                    best_space = space
                    best_idx = t
            teams[best_idx].append(student)
            team_idx = (best_idx + 1) % num_teams
    
    return teams

# ============================================================================
# OUTPUT
# ============================================================================

def save_to_csv(all_students, filename):
    """Save team assignments to CSV file."""
    # Sort by tutorial then by team
    for i in range(len(all_students)):
        for j in range(i + 1, len(all_students)):
            if all_students[i]['tutorial'] > all_students[j]['tutorial']:
                all_students[i], all_students[j] = all_students[j], all_students[i]
            elif all_students[i]['tutorial'] == all_students[j]['tutorial']:
                if all_students[i]['team'] > all_students[j]['team']:
                    all_students[i], all_students[j] = all_students[j], all_students[i]
    
    file = open(filename, 'w')
    file.write("Tutorial Group,Student ID,School,Name,Gender,CGPA,Team Assigned\n")
    for student in all_students:
        line = f"{student['tutorial']},{student['id']},{student['school']},{student['name']},{student['gender']},{student['cgpa']},{student['team']}\n"
        file.write(line)
    file.close()
    print("Saved to", filename, "(sorted by Tutorial and Team)")

# ============================================================================
# MAIN PROGRAM
# ============================================================================

def main():
    print("=" * 50)
    print("Team Allocation - ENHANCED (Sizes 4-10, STEM Balanced)")
    print("=" * 50)
    
    while True:
        try:
            team_size = int(input("\nEnter desired team size (4-10): "))
            if 4 <= team_size <= 10:
                break
            print("Please enter a number between 4 and 10")
        except:
            print("Invalid input. Please enter a number.")
    
    print(f"\nUsing team size: {team_size}")
    print("=" * 50)
    
    all_students = read_csv_file('records.csv')
    tutorials = group_by_tutorial(all_students)
    
    team_number = 1
    for tutorial_name in tutorials:
        print(f"\nProcessing Tutorial: {tutorial_name}")
        tutorial_students = tutorials[tutorial_name]
        teams = form_teams_adaptive(tutorial_students, team_size)
        
        for team in teams:
            for student in team:
                student['team'] = team_number
            team_number += 1
    
    save_to_csv(all_students, 'FDBA_Team1_JohnSmith.csv')
    print("\n" + "=" * 50)
    print("DONE! Check the output CSV file.")
    print("=" * 50)

main()
