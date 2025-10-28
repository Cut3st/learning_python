"""
Team Allocation - UNIVERSAL SOLUTION FOR ALL TEAM SIZES
Works optimally for team sizes 4-10 with minimal issues
"""

import random

# ============================================================================
# ADAPTIVE BALANCE FUNCTIONS
# ============================================================================

def calculate_adaptive_threshold(tutorial_students, team_size):
    male_count = 0
    female_count = 0
    for s in tutorial_students:
        gender = s['gender'].upper()
        if gender == 'M' or gender == 'MALE':
            male_count += 1
        else:
            female_count += 1
    total = male_count + female_count
    if total == 0:
        return {'male_max': 3, 'female_max': 3}
    male_ratio = male_count / total
    female_ratio = female_count / total
    tolerance = 0.20
    male_max_ratio = min(male_ratio + tolerance, 1.0)
    female_max_ratio = min(female_ratio + tolerance, 1.0)
    male_max_allowed = int(team_size * male_max_ratio) + (1 if (team_size * male_max_ratio) % 1 >= 0.5 else 0)
    female_max_allowed = int(team_size * female_max_ratio) + (1 if (team_size * female_max_ratio) % 1 >= 0.5 else 0)
    min_minority = 1 if min(male_count, female_count) >= 1 else 0
    return {
        'male_max': max(male_max_allowed, min_minority),
        'female_max': max(female_max_allowed, min_minority),
        'male_ratio': male_ratio,
        'female_ratio': female_ratio
    }

def is_gender_balanced_adaptive(team, thresholds):
    male_count, female_count = count_gender(team)
    return male_count <= thresholds['male_max'] and female_count <= thresholds['female_max']

def is_school_balanced(team):
    if len(team) == 0:
        return True
    max_allowed = (len(team) // 2) + 1
    school_count = count_schools(team)
    for count in school_count.values():
        if count > max_allowed:
            return False
    return True

def can_add_to_team_adaptive(team, student, max_size, thresholds):
    if len(team) >= max_size:
        return False
    temp_team = team + [student]
    return is_gender_balanced_adaptive(temp_team, thresholds) and is_school_balanced(temp_team)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def count_gender(team):
    male_count = 0
    female_count = 0
    for student in team:
        if student['gender'].upper() in ['M', 'MALE']:
            male_count += 1
        else:
            female_count += 1
    return male_count, female_count

def count_schools(team):
    school_count = {}
    for student in team:
        school = student['school']
        if school not in school_count:
            school_count[school] = 0
        school_count[school] += 1
    return school_count

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

def select_high_cgpa(original):
    """Manual insertion sort by CGPA descending (no .sort())."""
    arr = []
    for student in original:
        inserted = False
        for i in range(len(arr)):
            if student['cgpa'] > arr[i]['cgpa']:
                arr = arr[:i] + [student] + arr[i:]
                inserted = True
                break
        if not inserted:
            arr.append(student)
    return arr

# ============================================================================
# UNIVERSAL TEAM FORMATION - WORKS FOR ALL SIZES 4-10
# ============================================================================

def form_teams_adaptive(students, team_size):
    if not students:
        return []

    n = len(students)

    # Calculate thresholds for adaptive checks
    thresholds = calculate_adaptive_threshold(students, team_size)  # <-- MUST be here

    # Calculate number of teams (always round up)
    num_teams = (n + team_size - 1) // team_size

    # Determine target size for each team
    base_size = n // num_teams
    extra = n % num_teams
    team_targets = [base_size + 1 if i < extra else base_size for i in range(num_teams)]
    print(f"Creating {num_teams} teams with sizes: {team_targets}")

    # Initialize empty teams
    teams = [[] for _ in range(num_teams)]

    # Split students by gender and sort by CGPA
    males = [s for s in students if s['gender'].upper() in ['M', 'MALE']]
    females = [s for s in students if s['gender'].upper() in ['F', 'FEMALE']]
    
    males_sorted = select_high_cgpa(males)
    females_sorted = select_high_cgpa(females)

    # Determine minority and majority gender
    if len(males_sorted) <= len(females_sorted):
        minority, majority = males_sorted, females_sorted
    else:
        minority, majority = females_sorted, males_sorted

    # Phase 1: Distribute minority in round-robin
    for i, student in enumerate(minority):
        idx = i % num_teams
        teams[idx].append(student)

    # Phase 2: Fill remaining slots with majority
    team_idx = 0
    for student in majority:
        placed = False
        for _ in range(num_teams):
            idx = team_idx % num_teams
            if len(teams[idx]) < team_targets[idx] and can_add_to_team_adaptive(teams[idx], student, team_targets[idx], thresholds):
                teams[idx].append(student)
                placed = True
                team_idx = (idx + 1) % num_teams
                break
            team_idx += 1

        # Fallback: add to team with most space
        if not placed:
            best_idx = max(range(num_teams), key=lambda t: team_targets[t] - len(teams[t]))
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
# MAIN PROGRAM
# ============================================================================

def main():
    print("=" * 50)
    print("Team Allocation (UNIVERSAL 4-10)")
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
        print_team_stats(teams)
    save_to_csv(all_students, 'FDBA_Team1_JohnSmith.csv')
    print("\n" + "=" * 50)
    print("DONE! Check the output CSV file.")
    print("=" * 50)

main()
