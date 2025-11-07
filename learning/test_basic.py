import random
import csv

STEM_SCHOOLS = [
    "CCDS","CCEB","CoE","EEE","MAE","SPMS","SBS","MSE","CEE"
]

def calculate_ratio(students, team_size):
    #Calculate ratio for gender and STEM balance.
    male, female = count_gender(students)
    stem, nonstem = count_stem(students)
    
    total = male + female
    #If there are no students,returns default max is half the size or +1 if odd
    if total == 0:
        default_max = max(1, (team_size + 1) // 2)
        return {
            'male_max': default_max,
            'female_max': default_max,
            'stem_max': default_max,
            'nonstem_max': default_max
        }
    
    #Ratio with 10% tolerance
    tolerance = 0.1
    male_ratio = male / total
    female_ratio = female / total
    stem_ratio = stem / total
    nonstem_ratio = nonstem / total
    #Max scales by team size, with ratio tolerance, +0.5 is used to round to the nearest integer preferably something higher since its max
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

def count_gender(team):
    #Count males and females in a team
    male = 0
    female = 0
    for student in team:
        if student['gender'].upper() in ['M', 'MALE']:
            male += 1
        elif student['gender'].upper() in ['F', 'FEMALE']:
            female += 1
    return male, female

def count_stem(team):
    #Count STEM and non-STEM students in a team
    stem = 0
    nonstem = 0
    for student in team:
        if student['school'] in STEM_SCHOOLS:
            stem += 1
        elif student['school']:
            nonstem += 1
    return stem, nonstem

def check_balanced(team,student,team_size, ratio):
    if len(team) >= team_size:
        return False
    temp_team = team + [student]
    #Check if the genders are balanced
    male, female = count_gender(temp_team)
    #Check if the schools are balanced
    stem, nonstem = count_stem(temp_team)

    return (
        male <= ratio['male_max'] 
        and female <= ratio['female_max']
        and stem <= ratio['stem_max'] 
        and nonstem <= ratio['nonstem_max']
    )
def read_file(filename):
    # Reads student data from a CSV file using csv.DictReader.
    students = []
    # Use 'with open' for secure and automatic file closure
    with open(filename, 'r', newline='') as file:
        # csv.DictReader uses the header row (first line) as dictionary keys
        reader = csv.DictReader(file, fieldnames=['tutorial', 'id', 'name', 'school', 'gender', 'cgpa'])
        next(reader, None) 
        
        for row in reader:
            # Check for empty lines/rows 
            if not any(row.values()):
                continue
            #Type conversion for 'cgpa'
            try:
                row['cgpa'] = float(row['cgpa'])
            except ValueError:
                print(f"Warning: Could not convert CGPA to float for row: {row}")
                continue # Skip this student if data is invalid
            # Add the 'team' key with a default value of 0, as in your original code
            row['team'] = 0
            # The keys are already strings from the CSV, matching your original keys
            students.append(row)

    print("Loaded", len(students), "students")
    return students
def group_by_tutorial(students):
    #Grouping students by their tutorials
    tutorials = {}
    for student in students:
        tut = student['tutorial']
        if tut not in tutorials:
            tutorials[tut] = []
        tutorials[tut].append(student)
    
    print("Found", len(tutorials), "tutorial groups")
    return tutorials

def sort_cgpa(students):
    #Sort students by CGPA in descending order using insertion sort
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


def form_teams(students, team_size):

    if len(students) == 0:
        return []
    
    thresholds = calculate_ratio(students, team_size)
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
    
    stem_sorted = sort_cgpa(stem_students)
    nonstem_sorted = sort_cgpa(nonstem_students)
    
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
    
    males_sorted = sort_cgpa(males)
    females_sorted = sort_cgpa(females)
    
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
            if len(teams[idx]) < team_targets[idx] and check_balanced(teams[idx], student, team_targets[idx], thresholds):
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
            if len(teams[idx]) < team_targets[idx] and check_balanced(teams[idx], student, team_targets[idx], thresholds):
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
def write_csv(all_students, filename):
    #Bubble Sort by tutorial then by team
    for i in range(len(all_students)):
        for j in range(len(all_students) - i - 1):
            current_std = all_students[j]
            next_std = all_students[j + 1]
            if current_std['tutorial'] > next_std['tutorial'] or (current_std['tutorial'] == next_std['tutorial'] and current_std['team'] > next_std['team']):
                all_students[j], all_students[j + 1] = next_std, current_std
    #Write sorted data into CSV           
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['tutorial', 'id', 'school', 'name', 'gender', 'cgpa', 'team'])
        writer.writeheader()
        writer.writerows(all_students)
    
    print("Saved to", filename)

def main():
    print("Team Allocation (STEM/NON-STEM):")
    team_size = 5
    print(f"\nTeam Size: {team_size}")
    
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
