"""
Advanced Student Performance Analytics System
------------------------------------------------
A class of 10 students, 5 compulsory subjects.
Collects, organizes and analyses student marks using NumPy.
"""

import numpy as np

NUM_STUDENTS = 10
NUM_SUBJECTS = 5

# ============================================================
# 1. BATCH AND STUDENT INFORMATION
# ============================================================

def get_batch_info():
    """Accept batch string, clean it, and extract department name."""
    raw = input("Enter Batch Information (e.g., 'Batch-2026-Computer_Science'): ")
    batch_info = raw.strip()                     # remove leading/trailing spaces

    parts = batch_info.split("-")                 # ['Batch', '2026', 'Computer_Science']
    department_raw = parts[-1] if len(parts) >= 3 else batch_info
    department_name = department_raw.replace("_", " ").strip()

    return batch_info, department_name


def get_batch_info_sample():
    """Pre-filled sample batch info (used when user chooses sample data)."""
    raw = "   Batch-2026-Computer_Science   "
    batch_info = raw.strip()
    parts = batch_info.split("-")
    department_raw = parts[-1] if len(parts) >= 3 else batch_info
    department_name = department_raw.replace("_", " ").strip()
    print(f"Batch Information: {batch_info}")
    return batch_info, department_name


def get_subjects():
    """Subjects are fixed for the whole program -> stored as a Tuple."""
    subjects = ("Mathematics", "Physics", "Chemistry", "English", "Computer_Science")
    return subjects


def get_students():
    """Sample: 10 pre-filled student names -> stored in a List, with auto Roll Numbers."""
    students = [
        "Aarav Sharma", "Diya Patel", "Vihaan Reddy", "Ananya Iyer", "Arjun Nair",
        "Ishita Gupta", "Reyansh Rao", "Saanvi Menon", "Kabir Singh", "Myra Joshi"
    ]

    roll_numbers = range(101, 101 + NUM_STUDENTS)  # Range data type

    print("\nRoll Number Allocation:")
    print("-" * 30)
    for roll, name in zip(roll_numbers, students):
        print(f"Roll No: {roll}   Name: {name}")

    return students, list(roll_numbers)


def get_students_input():
    """Accept 10 student names from the user -> stored in a List, with auto Roll Numbers."""
    students = []
    print(f"\nEnter names of {NUM_STUDENTS} students:")
    for i in range(NUM_STUDENTS):
        name = input(f"  Student {i + 1} Name: ").strip()
        students.append(name)

    roll_numbers = range(101, 101 + NUM_STUDENTS)  # Range data type

    print("\nRoll Number Allocation:")
    print("-" * 30)
    for roll, name in zip(roll_numbers, students):
        print(f"Roll No: {roll}   Name: {name}")

    return students, list(roll_numbers)


def get_marks(students, subjects):
    """Sample: pre-filled marks (out of 100) for each student in each subject -> 10x5 NumPy array.

    Row order matches `students` list; column order matches `subjects` tuple:
    (Mathematics, Physics, Chemistry, English, Computer_Science)
    """
    marks_data = [
        [88, 76, 92, 81, 95],   # Aarav Sharma
        [45, 38, 55, 60, 50],   # Diya Patel   -> failed in Physics
        [72, 68, 74, 70, 78],   # Vihaan Reddy
        [91, 89, 87, 93, 96],   # Ananya Iyer  -> Distinction
        [35, 42, 30, 48, 55],   # Arjun Nair   -> failed in Maths & Chemistry
        [63, 59, 66, 61, 70],   # Ishita Gupta
        [85, 90, 88, 84, 92],   # Reyansh Rao  -> Distinction
        [58, 62, 49, 65, 60],   # Saanvi Menon
        [77, 71, 80, 75, 82],   # Kabir Singh
        [95, 93, 91, 97, 98],   # Myra Joshi   -> Distinction
    ]
    marks = np.array(marks_data, dtype=int)

    print("\nMarks recorded for all students:")
    print(f"{'Name':15s} " + " ".join(f"{s[:10]:>10s}" for s in subjects))
    for name, row in zip(students, marks):
        print(f"{name:15s} " + " ".join(f"{v:10d}" for v in row))

    return marks


def get_marks_input(students, subjects):
    """Accept marks from the user for each student in each subject -> 10x5 NumPy array."""
    marks = np.zeros((NUM_STUDENTS, NUM_SUBJECTS), dtype=int)

    print("\nEnter marks (out of 100) for each student in each subject:")
    for i, name in enumerate(students):
        print(f"\n--- Marks for {name} ---")
        for j, subject in enumerate(subjects):
            while True:
                try:
                    m = int(input(f"  {subject}: "))
                    if 0 <= m <= 100:
                        marks[i][j] = m
                        break
                    else:
                        print("    Marks must be between 0 and 100.")
                except ValueError:
                    print("    Please enter a valid integer.")

    return marks


# ============================================================
# 2. ACADEMIC PERFORMANCE ANALYSIS
# ============================================================

def analyse_performance(marks, students, subjects):
    total_marks = np.sum(marks, axis=1)                       # total per student
    percentage = np.round((total_marks / (NUM_SUBJECTS * 100)) * 100, 2)

    subject_avg = np.round(np.mean(marks, axis=0), 2)         # average per subject

    highest_mark = np.max(marks)
    lowest_mark = np.min(marks)

    highest_student_idx = np.argmax(total_marks)
    lowest_student_idx = np.argmin(total_marks)

    class_avg_percentage = round(np.mean(percentage), 2)

    highest_avg_subject_idx = np.argmax(subject_avg)
    lowest_avg_subject_idx = np.argmin(subject_avg)

    last_two_subjects_first_three = marks[0:3, -2:]           # slicing

    results = {
        "total_marks": total_marks,
        "percentage": percentage,
        "subject_avg": subject_avg,
        "highest_mark": highest_mark,
        "lowest_mark": lowest_mark,
        "highest_student": students[highest_student_idx],
        "lowest_student": students[lowest_student_idx],
        "class_avg_percentage": class_avg_percentage,
        "highest_avg_subject": subjects[highest_avg_subject_idx],
        "lowest_avg_subject": subjects[lowest_avg_subject_idx],
        "last_two_subjects_first_three": last_two_subjects_first_three,
    }

    print("\n" + "=" * 60)
    print("ACADEMIC PERFORMANCE ANALYSIS")
    print("=" * 60)

    print("\nStudent-wise Total Marks & Percentage:")
    for i, name in enumerate(students):
        print(f"  {name:15s} Total: {total_marks[i]:3d}   Percentage: {percentage[i]:.2f}%")

    print("\nSubject-wise Average Marks:")
    for j, subject in enumerate(subjects):
        print(f"  {subject:20s}: {subject_avg[j]:.2f}")

    print(f"\nHighest Marks in Class : {highest_mark}")
    print(f"Lowest Marks in Class  : {lowest_mark}")
    print(f"Highest Scoring Student: {results['highest_student']} "
          f"(Total: {total_marks[highest_student_idx]})")
    print(f"Lowest Scoring Student : {results['lowest_student']} "
          f"(Total: {total_marks[lowest_student_idx]})")
    print(f"Overall Class Average Percentage: {class_avg_percentage:.2f}%")
    print(f"Subject with Highest Average: {results['highest_avg_subject']} "
          f"({subject_avg[highest_avg_subject_idx]:.2f})")
    print(f"Subject with Lowest Average : {results['lowest_avg_subject']} "
          f"({subject_avg[lowest_avg_subject_idx]:.2f})")

    print("\nMarks of first 3 students in last 2 subjects "
          f"({subjects[-2]}, {subjects[-1]}):")
    print(last_two_subjects_first_three)

    return results


# ============================================================
# 3. STUDENT PERFORMANCE ANALYTICS
# ============================================================

def student_analytics(marks, students, subjects, percentage, class_avg_percentage, use_sample):
    print("\n" + "=" * 60)
    print("STUDENT PERFORMANCE ANALYTICS")
    print("=" * 60)

    # --- Subject search ---
    if use_sample:
        search_subject = "Physics"
        print(f"\nChecking if '{search_subject}' exists in subject list...")
    else:
        search_subject = input("\nEnter a subject name to check if it exists: ").strip()

    if search_subject in subjects:
        idx = subjects.index(search_subject)
        print(f"'{search_subject}' found in subject list at index {idx}.")
    else:
        print(f"'{search_subject}' does not exist in the subject list.")

    # --- Distinction holders (percentage >= 85) ---
    distinction_holders = [students[i] for i in range(NUM_STUDENTS) if percentage[i] >= 85]

    # --- Students who failed in one or more subjects (marks < 40) ---
    failed_students = [students[i] for i in range(NUM_STUDENTS) if np.any(marks[i] < 40)]

    # --- Students above class average ---
    above_average = [students[i] for i in range(NUM_STUDENTS) if percentage[i] > class_avg_percentage]

    # --- Reversed list (original untouched) ---
    reversed_students = list(reversed(students))

    # --- Alphabetical order (original untouched) ---
    alphabetical_students = sorted(students)

    print(f"\nDistinction Holders (Percentage >= 85%): {distinction_holders if distinction_holders else 'None'}")
    print(f"Failed Students (Marks < 40 in any subject): {failed_students if failed_students else 'None'}")
    print(f"Students Above Class Average ({class_avg_percentage:.2f}%): "
          f"{above_average if above_average else 'None'}")
    print(f"\nOriginal Student List : {students}")
    print(f"Reversed Student List : {reversed_students}")
    print(f"Alphabetical Order    : {alphabetical_students}")

    return distinction_holders, failed_students, above_average


# ============================================================
# 4. SUMMARY REPORT
# ============================================================

def print_summary_report(batch_info, department_name, students, results,
                          distinction_holders, failed_students):
    print("\n" + "=" * 60)
    print(" " * 15 + "ACADEMIC PERFORMANCE REPORT")
    print("=" * 60)
    print(f"{'Batch Name':30s}: {batch_info}")
    print(f"{'Department Name':30s}: {department_name}")
    print(f"{'Total Number of Students':30s}: {len(students)}")
    print(f"{'Overall Class Average %':30s}: {results['class_avg_percentage']:.2f}%")
    print(f"{'Highest Scoring Student':30s}: {results['highest_student']}")
    print(f"{'Lowest Scoring Student':30s}: {results['lowest_student']}")
    print(f"{'Subject with Highest Average':30s}: {results['highest_avg_subject']}")
    print(f"{'Subject with Lowest Average':30s}: {results['lowest_avg_subject']}")
    print(f"{'Number of Distinction Holders':30s}: {len(distinction_holders)}")
    print(f"{'Number of Failed Students':30s}: {len(failed_students)}")
    print("=" * 60)


# ============================================================
# MAIN PROGRAM
# ============================================================

# ============================================================
# MAIN PROGRAM (Menu-driven)
# ============================================================

def load_data():
    """Records are read automatically (built-in sample dataset) -> no manual typing needed."""
    batch_info, department_name = get_batch_info_sample()
    subjects = get_subjects()
    students, roll_numbers = get_students()
    marks = get_marks(students, subjects)
    return batch_info, department_name, subjects, students, roll_numbers, marks


def show_menu():
    print("\n" + "=" * 60)
    print(" " * 12 + "MAIN MENU - CHOOSE AN OPERATION")
    print("=" * 60)
    print(" 1. Total Marks & Percentage of each student")
    print(" 2. Average marks for each subject")
    print(" 3. Highest & Lowest marks in the class")
    print(" 4. Highest-scoring & Lowest-scoring student")
    print(" 5. Overall class average percentage")
    print(" 6. Subject with Highest & Lowest average")
    print(" 7. Marks of first 3 students in last 2 subjects (slicing)")
    print(" 8. Search a subject in the subject tuple")
    print(" 9. List of Distinction holders (Percentage >= 85%)")
    print("10. List of Failed students (Marks < 40 in any subject)")
    print("11. Students above class average")
    print("12. Reverse the student list (original unchanged)")
    print("13. Student names in alphabetical order (original unchanged)")
    print("14. Full Academic Performance Analysis (all of Section 2)")
    print("15. Full Student Performance Analytics (all of Section 3)")
    print("16. Final Summary Report (Section 4)")
    print(" 0. Exit")
    print("=" * 60)
    return input("Enter your choice: ").strip()


def main():
    print("=" * 60)
    print(" " * 10 + "STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("=" * 60)

    # ---- Records read automatically, once, at startup ----
    batch_info, department_name, subjects, students, roll_numbers, marks = load_data()

    # ---- Core computations (needed across menu options) ----
    total_marks = np.sum(marks, axis=1)
    percentage = np.round((total_marks / (NUM_SUBJECTS * 100)) * 100, 2)
    subject_avg = np.round(np.mean(marks, axis=0), 2)
    highest_mark = np.max(marks)
    lowest_mark = np.min(marks)
    highest_student_idx = np.argmax(total_marks)
    lowest_student_idx = np.argmin(total_marks)
    class_avg_percentage = round(np.mean(percentage), 2)
    highest_avg_subject_idx = np.argmax(subject_avg)
    lowest_avg_subject_idx = np.argmin(subject_avg)

    distinction_holders = [students[i] for i in range(NUM_STUDENTS) if percentage[i] >= 85]
    failed_students = [students[i] for i in range(NUM_STUDENTS) if np.any(marks[i] < 40)]
    above_average = [students[i] for i in range(NUM_STUDENTS) if percentage[i] > class_avg_percentage]

    results = {
        "total_marks": total_marks, "percentage": percentage, "subject_avg": subject_avg,
        "highest_mark": highest_mark, "lowest_mark": lowest_mark,
        "highest_student": students[highest_student_idx], "lowest_student": students[lowest_student_idx],
        "class_avg_percentage": class_avg_percentage,
        "highest_avg_subject": subjects[highest_avg_subject_idx],
        "lowest_avg_subject": subjects[lowest_avg_subject_idx],
    }

    while True:
        choice = show_menu()

        if choice == "1":
            print("\nStudent-wise Total Marks & Percentage:")
            for i, name in enumerate(students):
                print(f"  {name:15s} Total: {total_marks[i]:3d}   Percentage: {percentage[i]:.2f}%")

        elif choice == "2":
            print("\nSubject-wise Average Marks:")
            for j, subject in enumerate(subjects):
                print(f"  {subject:20s}: {subject_avg[j]:.2f}")

        elif choice == "3":
            print(f"\nHighest Marks in Class : {highest_mark}")
            print(f"Lowest Marks in Class  : {lowest_mark}")

        elif choice == "4":
            print(f"\nHighest Scoring Student: {students[highest_student_idx]} "
                  f"(Total: {total_marks[highest_student_idx]})")
            print(f"Lowest Scoring Student : {students[lowest_student_idx]} "
                  f"(Total: {total_marks[lowest_student_idx]})")

        elif choice == "5":
            print(f"\nOverall Class Average Percentage: {class_avg_percentage:.2f}%")

        elif choice == "6":
            print(f"\nSubject with Highest Average: {subjects[highest_avg_subject_idx]} "
                  f"({subject_avg[highest_avg_subject_idx]:.2f})")
            print(f"Subject with Lowest Average : {subjects[lowest_avg_subject_idx]} "
                  f"({subject_avg[lowest_avg_subject_idx]:.2f})")

        elif choice == "7":
            last_two_subjects_first_three = marks[0:3, -2:]
            print(f"\nMarks of first 3 students in last 2 subjects "
                  f"({subjects[-2]}, {subjects[-1]}):")
            print(last_two_subjects_first_three)

        elif choice == "8":
            search_subject = input("Enter a subject name to search: ").strip()
            if search_subject in subjects:
                idx = subjects.index(search_subject)
                print(f"'{search_subject}' found in subject list at index {idx}.")
            else:
                print(f"'{search_subject}' does not exist in the subject list.")

        elif choice == "9":
            print(f"\nDistinction Holders (Percentage >= 85%): "
                  f"{distinction_holders if distinction_holders else 'None'}")

        elif choice == "10":
            print(f"\nFailed Students (Marks < 40 in any subject): "
                  f"{failed_students if failed_students else 'None'}")

        elif choice == "11":
            print(f"\nStudents Above Class Average ({class_avg_percentage:.2f}%): "
                  f"{above_average if above_average else 'None'}")

        elif choice == "12":
            reversed_students = list(reversed(students))
            print(f"\nOriginal Student List : {students}")
            print(f"Reversed Student List : {reversed_students}")

        elif choice == "13":
            alphabetical_students = sorted(students)
            print(f"\nOriginal Student List      : {students}")
            print(f"Alphabetical Order List     : {alphabetical_students}")

        elif choice == "14":
            analyse_performance(marks, students, subjects)

        elif choice == "15":
            student_analytics(marks, students, subjects, percentage, class_avg_percentage, use_sample=True)

        elif choice == "16":
            print_summary_report(batch_info, department_name, students, results,
                                  distinction_holders, failed_students)

        elif choice == "0":
            print("\nExiting Student Performance Analytics System. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please select a valid option from the menu.")


if __name__ == "__main__":
    main()