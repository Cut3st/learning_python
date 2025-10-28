"""
SC1003 Team Allocation Validator - GUI Version
Easy-to-use window application for checking team balance
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import math

class TeamValidatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SC1003 Team Allocation Validator")
        self.root.geometry("1000x700")
        
        # Create main frame
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ====================================================================
        # TOP SECTION: File Selection and Settings
        # ====================================================================
        
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # File selection
        tk.Label(top_frame, text="CSV File:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.file_path = tk.StringVar()
        tk.Entry(top_frame, textvariable=self.file_path, width=60).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(top_frame, text="Browse...", command=self.browse_file, bg="#4CAF50", fg="white").grid(row=0, column=2, padx=5, pady=5)
        
        # Team size input
        tk.Label(top_frame, text="Team Size:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.team_size = tk.StringVar(value="5")
        tk.Entry(top_frame, textvariable=self.team_size, width=10).grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Run button
        tk.Button(top_frame, text="▶ Run Validation", command=self.run_validation, 
                 bg="#2196F3", fg="white", font=("Arial", 11, "bold"), 
                 padx=20, pady=5).grid(row=1, column=2, padx=5, pady=5)
        
        # ====================================================================
        # MIDDLE SECTION: Tabbed Results Display
        # ====================================================================
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab 1: Summary
        self.summary_tab = scrolledtext.ScrolledText(notebook, wrap=tk.WORD, font=("Courier", 9))
        notebook.add(self.summary_tab, text="📊 Summary")
        
        # Tab 2: Gender Issues
        self.gender_tab = scrolledtext.ScrolledText(notebook, wrap=tk.WORD, font=("Courier", 9))
        notebook.add(self.gender_tab, text="👥 Gender Imbalance")
        
        # Tab 3: School Issues
        self.school_tab = scrolledtext.ScrolledText(notebook, wrap=tk.WORD, font=("Courier", 9))
        notebook.add(self.school_tab, text="🏫 School Imbalance")
        
        # Tab 4: CGPA Issues
        self.cgpa_tab = scrolledtext.ScrolledText(notebook, wrap=tk.WORD, font=("Courier", 9))
        notebook.add(self.cgpa_tab, text="📈 CGPA Variance")
        
        # ====================================================================
        # BOTTOM SECTION: Status Bar
        # ====================================================================
        
        self.status_bar = tk.Label(main_frame, text="Ready. Select a CSV file to begin.", 
                                   relief=tk.SUNKEN, anchor=tk.W, bg="#f0f0f0")
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def browse_file(self):
        """Open file dialog to select CSV."""
        filename = filedialog.askopenfilename(
            title="Select Team Allocation CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
            self.status_bar.config(text=f"Selected: {filename}")
    
    def clear_all_tabs(self):
        """Clear all text widgets."""
        self.summary_tab.delete('1.0', tk.END)
        self.gender_tab.delete('1.0', tk.END)
        self.school_tab.delete('1.0', tk.END)
        self.cgpa_tab.delete('1.0', tk.END)
    
    def run_validation(self):
        """Run the validation and display results."""
        filename = self.file_path.get()
        
        if not filename:
            messagebox.showerror("Error", "Please select a CSV file first!")
            return
        
        try:
            team_size = int(self.team_size.get())
            if team_size < 4 or team_size > 10:
                messagebox.showerror("Error", "Team size must be between 4 and 10!")
                return
        except:
            messagebox.showerror("Error", "Invalid team size! Please enter a number 4-10.")
            return
        
        self.clear_all_tabs()
        self.status_bar.config(text="Processing... Please wait.")
        self.root.update()
        
        try:
            # Run validation
            results = self.validate_csv(filename, team_size)
            
            # Display results in tabs
            self.summary_tab.insert('1.0', results['summary'])
            self.gender_tab.insert('1.0', results['gender'])
            self.school_tab.insert('1.0', results['school'])
            self.cgpa_tab.insert('1.0', results['cgpa'])
            
            self.status_bar.config(text=f"✓ Validation complete! Overall Score: {results['score']:.1f}% | Grade: {results['grade']}")
            
            messagebox.showinfo("Success", f"Validation complete!\n\nOverall Score: {results['score']:.1f}%\nGrade: {results['grade']}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.status_bar.config(text="Error during validation.")
    
    def validate_csv(self, filename, expected_team_size):
        """Validate CSV and return results as dictionary."""
        
        # Read file
        file = open(filename, 'r')
        lines = file.readlines()
        file.close()
        
        # Parse students
        students = []
        for i in range(1, len(lines)):
            line = lines[i].strip()
            if not line:
                continue
            
            parts = line.split(',')
            if len(parts) >= 7:
                students.append({
                    'tutorial': parts[0], 'id': parts[1], 'name': parts[2],
                    'school': parts[3], 'gender': parts[4], 'cgpa': parts[5], 'team': parts[6]
                })
        
        # Group by tutorial and team
        tutorials = {}
        for s in students:
            tut, team = s['tutorial'], s['team']
            if tut not in tutorials:
                tutorials[tut] = {}
            if team not in tutorials[tut]:
                tutorials[tut][team] = []
            tutorials[tut][team].append(s)
        
        # Analyze
        total_teams = sum(len(teams) for teams in tutorials.values())
        gender_balanced, gender_imbalanced = 0, []
        school_balanced, school_imbalanced = 0, []
        all_team_means, all_team_stds, cgpa_high_variance = [], [], []
        team_sizes = []
        
        for tut_name in tutorials:
            for team_num in tutorials[tut_name]:
                team = tutorials[tut_name][team_num]
                size = len(team)
                team_sizes.append(size)
                max_allowed = (size // 2) + 1
                
                # Gender
                males = sum(1 for s in team if s['gender'].upper() in ['M', 'MALE'])
                females = len(team) - males
                if males <= max_allowed and females <= max_allowed:
                    gender_balanced += 1
                else:
                    gender_imbalanced.append((tut_name, team_num, males, females, size, max_allowed))
                
                # School
                school_count = {}
                for s in team:
                    school_count[s['school']] = school_count.get(s['school'], 0) + 1
                school_ok = True
                for school, count in school_count.items():
                    if count > max_allowed:
                        school_imbalanced.append((tut_name, team_num, school, count, size, max_allowed))
                        school_ok = False
                        break
                if school_ok:
                    school_balanced += 1
                
                # CGPA
                cgpas = [float(s['cgpa']) for s in team if s['cgpa']]
                if len(cgpas) > 1:
                    mean = sum(cgpas) / len(cgpas)
                    std = math.sqrt(sum((x - mean) ** 2 for x in cgpas) / len(cgpas))
                    all_team_means.append(mean)
                    all_team_stds.append(std)
                    if std >= 0.7:
                        cgpa_high_variance.append((tut_name, team_num, mean, std))
        
        # Calculate scores
        gender_balance_rate = (gender_balanced / total_teams) * 100
        school_balance_rate = (school_balanced / total_teams) * 100
        high_var = sum(1 for std in all_team_stds if std >= 0.5)
        cgpa_score = 100 - (high_var / total_teams * 100)
        overall_score = (gender_balance_rate * 0.4 + school_balance_rate * 0.4 + cgpa_score * 0.2)
        
        if overall_score >= 95:
            grade = "A+ (Excellent)"
        elif overall_score >= 90:
            grade = "A  (Very Good)"
        elif overall_score >= 85:
            grade = "B+ (Good)"
        elif overall_score >= 80:
            grade = "B  (Acceptable)"
        elif overall_score >= 75:
            grade = "C+ (Needs Improvement)"
        else:
            grade = "C  (Poor)"
        
        # Build result strings
        summary = self.build_summary(students, total_teams, expected_team_size, team_sizes,
                                     gender_balanced, len(gender_imbalanced), gender_balance_rate,
                                     school_balanced, len(school_imbalanced), school_balance_rate,
                                     all_team_means, all_team_stds, overall_score, grade)
        
        gender = self.build_gender_report(gender_imbalanced)
        school = self.build_school_report(school_imbalanced)
        cgpa = self.build_cgpa_report(cgpa_high_variance, all_team_means, all_team_stds, total_teams)
        
        return {
            'summary': summary, 'gender': gender, 'school': school, 'cgpa': cgpa,
            'score': overall_score, 'grade': grade
        }
    
    def build_summary(self, students, total_teams, expected_size, team_sizes, 
                     gender_bal, gender_imbal, gender_rate,
                     school_bal, school_imbal, school_rate,
                     means, stds, score, grade):
        """Build summary text."""
        s = "="*70 + "\n"
        s += "TEAM ALLOCATION VALIDATION SUMMARY\n"
        s += "="*70 + "\n\n"
        
        s += f"Total Students: {len(students)}\n"
        s += f"Total Teams:    {total_teams}\n"
        s += f"Expected Size:  {expected_size}\n\n"
        
        size_counts = {}
        for size in team_sizes:
            size_counts[size] = size_counts.get(size, 0) + 1
        
        s += "TEAM SIZE DISTRIBUTION:\n"
        s += "-"*70 + "\n"
        for size in sorted(size_counts.keys()):
            count = size_counts[size]
            perc = (count / total_teams) * 100
            status = "✓" if size == expected_size else "⚠"
            s += f"{status} Size {size}: {count:4d} teams ({perc:5.1f}%)\n"
        
        s += "\n" + "="*70 + "\n"
        s += "BALANCE SUMMARY\n"
        s += "="*70 + "\n\n"
        
        s += f"GENDER BALANCE:\n"
        s += f"  ✓ Balanced:   {gender_bal:4d} teams ({gender_rate:5.1f}%)\n"
        s += f"  ✗ Imbalanced: {gender_imbal:4d} teams ({100-gender_rate:5.1f}%)\n\n"
        
        s += f"SCHOOL DIVERSITY:\n"
        s += f"  ✓ Balanced:   {school_bal:4d} teams ({school_rate:5.1f}%)\n"
        s += f"  ✗ Imbalanced: {school_imbal:4d} teams ({100-school_rate:5.1f}%)\n\n"
        
        if means:
            s += f"CGPA STATISTICS:\n"
            s += f"  Average team mean: {sum(means)/len(means):.3f}\n"
            s += f"  Average team std:  {sum(stds)/len(stds):.3f}\n"
            s += f"  Range: {min(means):.3f} to {max(means):.3f}\n\n"
        
        s += "="*70 + "\n"
        s += "OVERALL QUALITY SCORE\n"
        s += "="*70 + "\n\n"
        s += f"Gender Balance:     {gender_rate:5.1f}%\n"
        s += f"School Diversity:   {school_rate:5.1f}%\n"
        s += f"CGPA Distribution:  {100 - (sum(1 for std in stds if std >= 0.5) / len(stds) * 100):5.1f}%\n"
        s += "-"*70 + "\n"
        s += f"OVERALL SCORE:      {score:5.1f}%\n"
        s += f"GRADE:              {grade}\n"
        
        return s
    
    def build_gender_report(self, imbalanced):
        """Build gender imbalance report."""
        if not imbalanced:
            return "✅ No gender imbalances detected!\nAll teams have proper gender balance."
        
        s = f"GENDER-IMBALANCED TEAMS ({len(imbalanced)} total)\n"
        s += "="*70 + "\n\n"
        for i, (tut, team, m, f, size, max_allow) in enumerate(imbalanced, 1):
            s += f"{i:3d}. Tutorial {tut:6s}, Team {team:4s}: M={m}, F={f} "
            s += f"(size={size}, max allowed={max_allow})\n"
        return s
    
    def build_school_report(self, imbalanced):
        """Build school imbalance report."""
        if not imbalanced:
            return "✅ No school imbalances detected!\nAll teams have proper school diversity."
        
        s = f"SCHOOL-IMBALANCED TEAMS ({len(imbalanced)} total)\n"
        s += "="*70 + "\n\n"
        for i, (tut, team, school, count, size, max_allow) in enumerate(imbalanced, 1):
            s += f"{i:3d}. Tutorial {tut:6s}, Team {team:4s}: {school:15s} "
            s += f"has {count}/{size} members (max allowed={max_allow})\n"
        return s
    
    def build_cgpa_report(self, high_var, means, stds, total_teams):
        """Build CGPA report."""
        s = "CGPA VARIANCE ANALYSIS\n"
        s += "="*70 + "\n\n"
        
        low_var = sum(1 for std in stds if std < 0.3)
        med_var = sum(1 for std in stds if 0.3 <= std < 0.5)
        high_v = sum(1 for std in stds if std >= 0.5)
        
        s += f"Low variance (< 0.3):      {low_var:4d} teams ({low_var/total_teams*100:5.1f}%)\n"
        s += f"Medium variance (0.3-0.5): {med_var:4d} teams ({med_var/total_teams*100:5.1f}%)\n"
        s += f"High variance (≥ 0.5):     {high_v:4d} teams ({high_v/total_teams*100:5.1f}%)\n\n"
        
        if high_var:
            s += f"Teams with VERY HIGH variance (≥ 0.7): {len(high_var)}\n"
            s += "-"*70 + "\n"
            for i, (tut, team, mean, std) in enumerate(high_var[:50], 1):
                s += f"{i:3d}. Tutorial {tut:6s}, Team {team:4s}: Mean={mean:.2f}, Std={std:.2f}\n"
            if len(high_var) > 50:
                s += f"\n... and {len(high_var) - 50} more\n"
        else:
            s += "✅ No teams with very high CGPA variance!\n"
        
        return s

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TeamValidatorGUI(root)
    root.mainloop()
