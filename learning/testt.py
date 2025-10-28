"""
SC1003 Team Allocation Simulator - BALANCED VERSION
Ensures proper gender and school balance with user-configurable team size
"""

import random

# ============================================================================
# STEP 1: READ THE CSV FILE
# ============================================================================

def read_csv_file(filename):
    """Read the records.csv file and return a list of students."""
    students = []
    
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()
    
    # Skip the header (first line)
    for i in range(1, len(lines)):
        line = lines[i].strip()
        if not line:
            continue
        parts = line.split(',')
        
        # Create a student dictionary
        student = {
            'tutorial': parts[0],
            'id': parts[1],
            'name': parts[2],
            'school': parts[3],
            'gender': parts[4],
            'cgpa': float(parts[5]),
            'team': 0  # Will assign later
        }
        students.append(student)
    
    print("Loaded", len(students), "students")
    return students


# ============================================================================
# STEP 2: GROUP STUDENTS BY TUTORIAL
# ============================================================================

def group_by_tutorial(students):
    """Put students into groups based on their tutorial."""
    tutorials = {}
    
    for student in students:
        tut = student['tutorial']
        
        if tut not in tutorials:
            tutorials[tut] = []
        
        tutorials[tut].append(student)
    
    print("Found", len(tutorials), "tutorial groups")
    return tutorials


# ============================================================================
# STEP 3: CHECK IF WE CAN ADD A STUDENT TO A TEAM (STRICT RULES)
# ============================================================================

def count_gender(team):
    """Count how many males and females in a team."""
    male_count = 0
    female_count = 0
    
    for student in team:
        if student['gender'].upper() in ['M', 'MALE']:
            male_count = male_count + 1
        else:
            female_count = female_count + 1
    
    return male_count, female_count


def count_schools(team):
    """Count students from each school in a team."""
    school_count = {}
    
    for student in team:
        school = student['school']
        if school not in school_count:
            school_count[school] = 0
        school_count[school] = school_count[school] + 1
    
    return school_count


def can_add_to_team(team, student, team_size):
    """
    Check if we can add this student to the team without breaking balance rules.
    STRICT: No gender or school should exceed (team_size // 2) + 1
    """
    
    # Rule 1: Team is full
    if len(team) >= team_size:
        return False
    
    # Calculate max allowed for majority (half + 1)
    future_size = len(team) + 1
    max_allowed = (future_size // 2) + 1
    
    # Rule 2: Gender balance - strict check
    male_count, female_count = count_gender(team)
    
    if student['gender'].upper() in ['M', 'MALE']:
        if male_count + 1 > max_allowed:
            return False
    else:
        if female_count + 1 > max_allowed:
            return False
    
    # Rule 3: School balance - strict check
    school_count = count_schools(team)
    student_school = student['school']
    
    current_school_count = school_count.get(student_school, 0)
    if current_school_count + 1 > max_allowed:
        return False
    
    return True


# ============================================================================
# STEP 4: FORM TEAMS WITH PROPER BALANCING
# ============================================================================

def is_stem_school(school):
    """Check if a school is STEM or not."""
    stem_keywords = ['ENG', 'SCSE', 'EEE', 'MAE', 'CEE', 'MSE', 'SCIENCE', 'SPMS', 'CCDS', 'SBS']
    
    for keyword in stem_keywords:
        if keyword.upper() in school.upper():
            return True
    return False


def form_teams_balanced(students, team_size):
    """
    Form teams with strict balance requirements:
    1. Prioritize minority gender students first
    2. Sort by CGPA for balance
    3. Use round-robin with strict constraint checking
    """
    
    if len(students) == 0:
        return []
    
    # Step 1: Identify minority gender
    male_count = 0
    female_count = 0
    for s in students:
        if s['gender'].upper() in ['M', 'MALE']:
            male_count += 1
        else:
            female_count += 1
    
    minority_gender = 'M' if male_count < female_count else 'F'
    
    # Step 2: Separate into priority groups
    minority_students = []
    majority_students = []
    
    for s in students:
        if (minority_gender == 'M' and s['gender'].upper() in ['M', 'MALE']) or \
           (minority_gender == 'F' and s['gender'].upper() in ['F', 'FEMALE']):
            minority_students.append(s)
        else:
            majority_students.append(s)
    
    # Step 3: Sort both groups by CGPA (descending) - simple bubble sort
    for i in range(len(minority_students)):
        for j in range(i + 1, len(minority_students)):
            if minority_students[j]['cgpa'] > minority_students[i]['cgpa']:
                temp = minority_students[i]
                minority_students[i] = minority_students[j]
                minority_students[j] = temp
    
    for i in range(len(majority_students)):
        for j in range(i + 1, len(majority_students)):
            if majority_students[j]['cgpa'] > majority_students[i]['cgpa']:
                temp = majority_students[i]
                majority_students[i] = majority_students[j]
                majority_students[j] = temp
    
    # Step 4: Initialize teams
    num_teams = (len(students) + team_size - 1) // team_size
    teams = []
    for _ in range(num_teams):
        teams.append([])
    
    # Step 5: Place minority gender students first (round-robin)
    team_index = 0
    for student in minority_students:
        placed = False
        attempts = 0
        start_index = team_index
        
        while not placed and attempts < num_teams:
            if can_add_to_team(teams[team_index], student, team_size):
                teams[team_index].append(student)
                placed = True
                team_index = (team_index + 1) % num_teams
            else:
                team_index = (team_index + 1) % num_teams
                attempts += 1
                if team_index == start_index:
                    break
        
        if not placed:
            # Force into smallest team (last resort)
            smallest = 0
            for t in range(len(teams)):
                if len(teams[t]) < len(teams[smallest]):
                    smallest = t
            teams[smallest].append(student)
    
    # Step 6: Place majority gender students (round-robin)
    for student in majority_students:
        placed = False
        attempts = 0
        start_index = team_index
        
        while not placed and attempts < num_teams:
            if can_add_to_team(teams[team_index], student, team_size):
                teams[team_index].append(student)
                placed = True
                team_index = (team_index + 1) % num_teams
            else:
                team_index = (team_index + 1) % num_teams
                attempts += 1
                if team_index == start_index:
                    break
        
        if not placed:
            # Force into smallest team (last resort)
            smallest = 0
            for t in range(len(teams)):
                if len(teams[t]) < len(teams[smallest]):
                    smallest = t
            teams[smallest].append(student)
    
    return teams


# ============================================================================
# STEP 5: SAVE OUTPUT TO CSV
# ============================================================================

def save_to_csv(all_students, filename):
    """Save the team assignments to a new CSV file."""
    file = open(filename, 'w')
    
    # Write header
    file.write("Tutorial Group,Student ID,School,Name,Gender,CGPA,Team Assigned\n")
    
    # Write each student
    for student in all_students:
        line = student['tutorial'] + ',' + student['id'] + ',' + student['school'] + ','
        line = line + student['name'] + ',' + student['gender'] + ','
        line = line + str(student['cgpa']) + ',' + str(student['team']) + '\n'
        file.write(line)
    
    file.close()
    print("Saved to", filename)


# ============================================================================
# STEP 6: PRINT STATISTICS
# ============================================================================

def print_team_stats(teams):
    """Show some information about the teams formed."""
    print("\n--- TEAM STATISTICS ---")
    
    for i in range(len(teams)):
        team = teams[i]
        if len(team) == 0:
            continue
            
        print("Team", i + 1, "- Size:", len(team))
        
        # Count genders
        male_count, female_count = count_gender(team)
        print("  Gender: M =", male_count, ", F =", female_count)
        
        # Count schools
        school_count = count_schools(team)
        print("  Schools:", school_count)
        
        # Average CGPA
        total_cgpa = 0
        for student in team:
            total_cgpa = total_cgpa + student['cgpa']
        avg_cgpa = total_cgpa / len(team) if len(team) > 0 else 0
        print("  Average CGPA:", round(avg_cgpa, 2))
        print()


# ============================================================================
# MAIN PROGRAM
# ============================================================================

def main():
    print("=" * 50)
    print("SC1003 Team Allocation Simulator")
    print("=" * 50)
    
    # Step 1: Get team size from user
    while True:
        try:
            team_size = int(input("\nEnter desired team size (4-10): "))
            if 4 <= team_size <= 10:
                break
            else:
                print("Please enter a number between 4 and 10")
        except:
            print("Invalid input. Please enter a number.")
    
    print(f"\nUsing team size: {team_size}")
    print("=" * 50)
    
    # Step 2: Read data
    all_students = read_csv_file('records.csv')
    
    # Step 3: Group by tutorial
    tutorials = group_by_tutorial(all_students)
    
    # Step 4: Process each tutorial
    team_number = 1
    
    for tutorial_name in tutorials:
        print("\nProcessing Tutorial:", tutorial_name)
        tutorial_students = tutorials[tutorial_name]
        
        # Form teams for this tutorial
        teams = form_teams_balanced(tutorial_students, team_size)
        
        # Assign team numbers
        for team in teams:
            for student in team:
                student['team'] = team_number
            team_number = team_number + 1
        
        # Show stats
        print_team_stats(teams)
    
    # Step 5: Save output
    save_to_csv(all_students, 'FDBA_Team1_JohnSmith.csv')
    
    print("\n" + "=" * 50)
    print("DONE! Check the output CSV file.")
    print("=" * 50)


# Run the program
main()
