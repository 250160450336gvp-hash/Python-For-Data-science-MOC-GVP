"""
Student Performance Analytics System (Menu-Based Version)
-------------------------------------------------------------
10 students ka data pehle se stored hai (list of dictionaries).

Calculate (har student ke liye):
  - Total Marks
  - Percentage
  - Grade (A, B, C, D, F)

"""

SUBJECTS = ["Maths", "Science", "English", "History", "Computer"]
PASS_MARK = 40  # is se kam marks matlab us subject me fail

# ---------------------------------------------------------
# 1. Student data (fixed - 10 students)
# ---------------------------------------------------------
students = [
    {"roll": 1,  "name": "Amit",   "marks": [78, 65, 90, 55, 88]},
    {"roll": 2,  "name": "Bhavna", "marks": [45, 39, 60, 70, 50]},
    {"roll": 3,  "name": "Chirag", "marks": [95, 92, 89, 91, 97]},
    {"roll": 4,  "name": "Divya",  "marks": [33, 42, 38, 50, 45]},
    {"roll": 5,  "name": "Esha",   "marks": [88, 76, 92, 85, 80]},
    {"roll": 6,  "name": "Farhan", "marks": [60, 55, 65, 70, 62]},
    {"roll": 7,  "name": "Gauri",  "marks": [70, 68, 75, 60, 72]},
    {"roll": 8,  "name": "Hiten",  "marks": [50, 45, 40, 39, 55]},
    {"roll": 9,  "name": "Isha",   "marks": [82, 79, 85, 88, 90]},
    {"roll": 10, "name": "Jatin",  "marks": [30, 25, 35, 40, 20]},
]


# ---------------------------------------------------------
# 2. Grade calculator
# ---------------------------------------------------------
def get_grade(percentage):
    if percentage >= 90:
        return "A"
    elif percentage >= 75:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"


# ---------------------------------------------------------
# 3. Calculate Total Marks, Percentage, Grade for each student
# ---------------------------------------------------------
def calculate_results():
    for s in students:
        total = sum(s["marks"])
        percentage = total / len(SUBJECTS)
        s["total"] = total
        s["percentage"] = round(percentage, 2)
        s["grade"] = get_grade(percentage)


# ---------------------------------------------------------
# 4. Display functions (each linked to a menu choice)
# ---------------------------------------------------------
def show_all_students():
    print("\n" + "=" * 60)
    print("STUDENT REPORT")
    print("=" * 60)
    for s in students:
        print(f"Roll {s['roll']:<3} {s['name']:<10} Marks: {s['marks']} "
              f"Total: {s['total']:<4} %: {s['percentage']:<6} Grade: {s['grade']}")


def show_class_average():
    class_average = round(sum(s["percentage"] for s in students) / len(students), 2)
    print(f"\nClass Average Percentage : {class_average}%")
    return class_average


def show_highest_scorer():
    highest_marks = max(s["total"] for s in students)
    highest_scorers = [s["name"] for s in students if s["total"] == highest_marks]
    print(f"\nHighest Scorer(s)        : {highest_scorers} (Total: {highest_marks})")


def show_lowest_scorer():
    lowest_marks = min(s["total"] for s in students)
    lowest_scorers = [s["name"] for s in students if s["total"] == lowest_marks]
    print(f"\nLowest Scorer(s)         : {lowest_scorers} (Total: {lowest_marks})")


def show_above_average():
    class_average = round(sum(s["percentage"] for s in students) / len(students), 2)
    above_average = [s["name"] for s in students if s["percentage"] > class_average]
    print(f"\nAbove Average Students   : {above_average}")


def show_failed_students():
    failed_students = [s["name"] for s in students if any(m < PASS_MARK for m in s["marks"])]
    print(f"\nFailed in 1+ Subjects    : {failed_students}")


def show_everything():
    show_all_students()
    print("\n" + "=" * 60)
    print("CLASS ANALYTICS")
    print("=" * 60)
    show_class_average()
    show_highest_scorer()
    show_lowest_scorer()
    show_above_average()
    show_failed_students()


# ---------------------------------------------------------
# 5. Menu
# ---------------------------------------------------------
def show_menu():
    print("\n" + "=" * 60)
    print("MENU")
    print("=" * 60)
    print("1. Class Average Percentage")
    print("2. Highest Scorer(s)")
    print("3. Lowest Scorer(s)")
    print("4. Students Above Class Average")
    print("5. Students Who Failed in 1+ Subjects")
    print("6. Show All Student Records (Total, %, Grade)")
    print("7. Show Everything (All of the above)")
    print("0. Exit")


def main():
    calculate_results()

    while True:
        show_menu()
        choice = input("\nApna choice enter karo: ").strip()

        if choice == "1":
            show_class_average()
        elif choice == "2":
            show_highest_scorer()
        elif choice == "3":
            show_lowest_scorer()
        elif choice == "4":
            show_above_average()
        elif choice == "5":
            show_failed_students()
        elif choice == "6":
            show_all_students()
        elif choice == "7":
            show_everything()
        elif choice == "0":
            print("\nBye!")
            break
        else:
            print("\nGalat choice! 0-7 ke beech koi number enter karo.")


if __name__ == "__main__":
    main()