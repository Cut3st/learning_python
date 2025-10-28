"""
Team Allocation - BASIC ALGORITHM (Team Size 5)
Implements adaptive gender balance with perfect team formation for size 5
"""

import random

# ============================================================================
# ADAPTIVE BALANCE FUNCTIONS
# ============================================================================

def calculate_adaptive_threshold(students, team_size):
    # Count male and female
    male = 0
    female = 0
    for s in students:
        if s['gender'].upper() in ['M', 'MALE']:
            male += 1
        else:
            female += 1
    total = male + female
    if total == 0:
        return {'male_max': 3, 'female_max': 3}
    # Simple ratio with 20% tolerance
    male_ratio = male / total
    female_ratio = female / total
    tolerance = 0.2
    male_max = int(team_size * min(male_ratio + tolerance, 1) + 0.5)
    female_max = int(team_size * min(female_ratio + tolerance, 1) + 0.5)
    return {'male_max': max(1, male_max), 'female_max': max(1, female_max)}

def is_gender_balanced(team, thresholds):
    male, female = count_gender(team)
    return male <= thresholds['male_max'] and female <= thresholds['female_max']

def is_school_balanced(team):
    if len(team) == 0:
        return True
    max_allowed = (len(team) // 2) + 1
    schools = count_schools(team)
    for count in schools.values():
        if count > max_allowed:
            return False
    return True

def can_add_to_team(team, student, max_size, thresholds):
    if len(team) >= max_size:
        return False
    temp_team = team + [student]
    return is_gender_balanced(temp_team, thresholds) and is_school_balanced(temp_team)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def count_gender(team):
    male = 0
    female = 0
    for student in team:
        if student['gender'].upper() in ['M', 'MALE']:
            male += 1
        else:
            female += 1
    return male, female

def count_schools(team):
    schools = {}
    for student in team:
        school = student['school']
        if school not in schools:
            schools[school] = 0
        schools[school] += 1
    return schools

def read_csv_file(filename):
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
    tutorials = {}
    for student in students:
        tut = student['tutorial']
        if tut not in tutorials:
            tutorials[tut] = []
        tutorials[tut].append(student)
    print("Found", len(tutorials), "tutorial groups")
    return tutorials

def select_high_cgpa(students):
    # Simple insertion sort descending
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
# TEAM FORMATION FOR SIZE 5
# ============================================================================

def form_teams_adaptive(students, team_size):
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

    # Split by gender
    males = [s for s in students if s['gender'].upper() in ['M', 'MALE']]
    females = [s for s in students if s['gender'].upper() not in ['M', 'MALE']]

    males_sorted = select_high_cgpa(males)
    females_sorted = select_high_cgpa(females)

    # Determine minority and majority
    if len(males_sorted) <= len(females_sorted):
        minority, majority = males_sorted, females_sorted
    else:
        minority, majority = females_sorted, males_sorted

    # PHASE 1: distribute minority evenly
    for i, s in enumerate(minority):
        idx = i % num_teams
        teams[idx].append(s)

    # PHASE 2: fill majority
    team_idx = 0
    for student in majority:
        placed = False
        for attempt in range(num_teams):
            idx = (team_idx + attempt) % num_teams
            if len(teams[idx]) < team_targets[idx] and can_add_to_team(teams[idx], student, team_targets[idx], thresholds):
                teams[idx].append(student)
                placed = True
                team_idx = (idx + 1) % num_teams
                break
        if not placed:
            # fallback: team with most space
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
# OUTPUT AND STATS
# ============================================================================

def save_to_csv(all_students, filename):
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

def print_team_stats(teams):
    print("\n--- TEAM STATISTICS ---")
    for i, team in enumerate(teams):
        if len(team) == 0:
            continue
        male_count, female_count = count_gender(team)
        school_count = count_schools(team)
        print(f"Team {i + 1} - Size: {len(team)}")
        print(f"  Gender: M={male_count}, F={female_count}")
        print(f"  Schools: {school_count}")
        total_cgpa = sum(s['cgpa'] for s in team)
        avg_cgpa = total_cgpa / len(team) if len(team) > 0 else 0
        print(f"  Average CGPA: {avg_cgpa:.2f}\n")

# ============================================================================
# MAIN PROGRAM - BASIC VERSION (TEAM SIZE 5 ONLY)
# ============================================================================

def main():
    print("=" * 50)
    print("Team Allocation - BASIC (Size 5)")
    print("=" * 50)
    
    # HARDCODED: Team size is always 5 for basic requirement
    team_size = 5
    
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
        print_team_stats(teams)
    save_to_csv(all_students, 'FDBA_Team1_JohnSmith.csv')
    print("\n" + "=" * 50)
    print("DONE! Check the output CSV file.")
    print("=" * 50)

main()