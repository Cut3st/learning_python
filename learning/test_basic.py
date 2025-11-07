import random
import csv

STEM_SCHOOLS = ["CCDS", "CCEB", "CoE", "EEE", "MAE", "SPMS", "SBS", "MSE", "CEE"]


def calculate_ratio(students, team_size):
    #Calculate max allowed per gender and STEM category with 10% tolerance
    male, female = count_gender(students)
    stem, nonstem = count_stem(students)
    total = male + female
    
    if total == 0:
        default_max = max(1, (team_size + 1) // 2)
        return {
            'male_max': default_max,
            'female_max': default_max,
            'stem_max': default_max,
            'nonstem_max': default_max
        }
    
    tolerance = 0.1
    male_max = int(team_size * min(male / total + tolerance, 1) + 0.5)
    female_max = int(team_size * min(female / total + tolerance, 1) + 0.5)
    stem_max = int(team_size * min(stem / total + tolerance, 1) + 0.5)
    nonstem_max = int(team_size * min(nonstem / total + tolerance, 1) + 0.5)
    
    return {
        'male_max': max(1, male_max),
        'female_max': max(1, female_max),
        'stem_max': max(1, stem_max),
        'nonstem_max': max(1, nonstem_max)
    }

def count_gender(team):
    #Count males and females in a team
    male = female = 0
    for student in team:
        if student['gender'].upper() in ['M', 'MALE']:
            male += 1
        elif student['gender'].upper() in ['F', 'FEMALE']:
            female += 1
    return male, female

def count_stem(team):
    #Count STEM and non-STEM students in a team.
    stem = nonstem = 0
    for student in team:
        if student['school'] in STEM_SCHOOLS:
            stem += 1
        elif student['school']:  # Only count if school is not empty
            nonstem += 1
    return stem, nonstem

def check_balanced(team, student, team_size, ratio):
    if len(team) >= team_size:
        return False
    
    # Temporarily add to check
    temp_team = team + [student]
    male, female = count_gender(temp_team)
    stem, nonstem = count_stem(temp_team)
    
    return (
        male <= ratio['male_max'] and
        female <= ratio['female_max'] and
        stem <= ratio['stem_max'] and
        nonstem <= ratio['nonstem_max']
    )

def read_file(filename):
    #Read student data from CSV
    students = []
    with open(filename, 'r', newline='') as file:
        reader = csv.DictReader(file, fieldnames=['tutorial', 'id', 'name', 'school', 'gender', 'cgpa'])
        next(reader)  # Skip header row
        
        for row in reader:
            if not any(row.values()):
                continue
            
            try:
                row['cgpa'] = float(row['cgpa'])
                row['team'] = 0  # Default team number
                students.append(row)
            except ValueError:
                print(f"Warning: Invalid CGPA for ID {row['id']}")
                continue
    
    print(f"Loaded {len(students)} students")
    return students

def group_by_tutorial(students):
    #Group students by tutorial
    tutorials = {}
    for student in students:
        tut = student['tutorial']
        if tut not in tutorials:
            tutorials[tut] = []
        tutorials[tut].append(student)
    
    print(f"Found {len(tutorials)} tutorial groups")
    return tutorials

def sort_cgpa(students):
    #Sort students by CGPA descending using in-place insertion sort
    for i in range(1, len(students)):
        key = students[i]
        j = i - 1
        while j >= 0 and students[j]['cgpa'] < key['cgpa']:
            students[j + 1] = students[j]
            j -= 1
        students[j + 1] = key
    return students

def form_teams(students, team_size):
    #Form diverse teams using round-robin placement
    if not students:
        return []
    
    thresholds = calculate_ratio(students, team_size)
    n = len(students)
    num_teams = (n + team_size - 1) // team_size
    
    # Team size targets (some teams may be +1)
    base_size = n // num_teams
    extra = n % num_teams
    team_targets = [base_size + 1] * extra + [base_size] * (num_teams - extra)
    
    teams = [[] for _ in range(num_teams)]
    placed_ids = set()  # Track placed student IDs (O(1) lookup)

    # --- Split students ---
    stem_students = []
    nonstem_students = []
    males = []
    females = []
    
    for s in students:
        if s['school'] in STEM_SCHOOLS:
            stem_students.append(s)
        elif s['school']:
            nonstem_students.append(s)
        
        if s['gender'].upper() in ['M', 'MALE']:
            males.append(s)
        elif s['gender'].upper() in ['F', 'FEMALE']:
            females.append(s)
    
    # Sort each group manually
    stem_sorted = sort_cgpa(stem_students)
    nonstem_sorted = sort_cgpa(nonstem_students)
    males_sorted = sort_cgpa(males)
    females_sorted = sort_cgpa(females)
    
    # Determine minorities
    if len(stem_sorted) <= len(nonstem_sorted):
        stem_minority, stem_majority = stem_sorted, nonstem_sorted
    else:
        stem_minority, stem_majority = nonstem_sorted, stem_sorted
    
    if len(males_sorted) <= len(females_sorted):
        minority, majority = males_sorted, females_sorted
    else:
        minority, majority = females_sorted, males_sorted
    
    random.shuffle(majority)
    random.shuffle(stem_majority)

    #Distribute STEM minority evenly
    for i, s in enumerate(stem_minority):
        if s['id'] not in placed_ids:
            idx = i % num_teams
            teams[idx].append(s)
            placed_ids.add(s['id'])

    #Distribute gender minority evenly
    for i, s in enumerate(minority):
        if s['id'] not in placed_ids:
            idx = i % num_teams
            teams[idx].append(s)
            placed_ids.add(s['id'])

    #Fill with gender majority
    current_team = 0
    for student in majority:
        if student['id'] in placed_ids:
            continue
        
        placed = False
        for attempt in range(num_teams):
            idx = (current_team + attempt) % num_teams
            if len(teams[idx]) < team_targets[idx] and check_balanced(teams[idx], student, team_targets[idx], thresholds):
                teams[idx].append(student)
                placed_ids.add(student['id'])
                placed = True
                current_team = (idx + 1) % num_teams
                break
        
        if not placed:
            # Fallback: team with most space
            best_idx = 0
            most_space = team_targets[0] - len(teams[0])
            for t in range(1, num_teams):
                space = team_targets[t] - len(teams[t])
                if space > most_space:
                    most_space = space
                    best_idx = t
            
            teams[best_idx].append(student)
            placed_ids.add(student['id'])
            current_team = (best_idx + 1) % num_teams

    #Fill remaining STEM majority
    for student in stem_majority:
        if student['id'] in placed_ids:
            continue
        
        placed = False
        for attempt in range(num_teams):
            idx = (current_team + attempt) % num_teams
            if len(teams[idx]) < team_targets[idx] and check_balanced(teams[idx], student, team_targets[idx], thresholds):
                teams[idx].append(student)
                placed_ids.add(student['id'])
                placed = True
                current_team = (idx + 1) % num_teams
                break
        
        if not placed:
            best_idx = 0
            most_space = team_targets[0] - len(teams[0])
            for t in range(1, num_teams):
                space = team_targets[t] - len(teams[t])
                if space > most_space:
                    most_space = space
                    best_idx = t
            
            teams[best_idx].append(student)
            placed_ids.add(student['id'])
            current_team = (best_idx + 1) % num_teams
    
    return teams

def write_csv(all_students, filename):
    # Write students sorted by tutorial and team using bucket approach
    # Bucket students: tutorial -> team -> list
    buckets = {}
    for student in all_students:
        tut = student['tutorial']
        team = student['team']
        if tut not in buckets:
            buckets[tut] = {}
        if team not in buckets[tut]:
            buckets[tut][team] = []
        buckets[tut][team].append(student)
    
    # Simple insertion sort for small lists
    def simple_sort(arr):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr
    
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['tutorial', 'id', 'school', 'name', 'gender', 'cgpa', 'team'])
        writer.writeheader()
        
        # Write in order: sorted tutorials, then sorted teams
        for tut in simple_sort(list(buckets.keys())):
            for team_num in simple_sort(list(buckets[tut].keys())):
                writer.writerows(buckets[tut][team_num])
    
    print(f"Saved to {filename}")

def main():
    print("Team Allocation (STEM/NON-STEM):")
    team_size = 5
    print(f"Team Size: {team_size}")
    
    all_students = read_file('records.csv')
    tutorials = group_by_tutorial(all_students)
    
    team_number = 1
    for tut_students in tutorials.values():
        teams = form_teams(tut_students, team_size)
        
        for team in teams:
            for student in team:
                student['team'] = team_number
            team_number += 1
    
    write_csv(all_students, 'FCS1_Team2_Joshua.csv')
    print("DONE! Check the output CSV file.")

if __name__ == "__main__":
    main()