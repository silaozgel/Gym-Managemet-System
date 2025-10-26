import datetime
from collections import Counter


class Person:
    def __init__(self, name, email, phone_num, age):
        self.name = name
        self.email = email
        self.phone_num = phone_num
        self.age = age

class User(Person):
    def __init__(self, user_id, name, email, phone_num, age):
        super().__init__(name, email, phone_num, age)
        self.user_id = user_id
        self.membership = None

    def assign_membership(self, membership):
        self.membership = membership
        print(f"Membership assigned for {self.name} until {membership.end_date}.")

    def calculate_billing(self):
        if not self.membership:
            print(f"User {self.name} is not a member.")
            return 0
        current_date = datetime.date.today()
        billing_start = max(self.membership.start_date, current_date.replace(day=1))
        billing_end = min(self.membership.end_date, current_date.replace(day=1) + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
        if billing_start > billing_end:
            print(f"No active membership for {self.name}.")
            return 0
        total_cost = self.membership.cost_per_month
        print(f"Billing for {self.name} (ID: {self.user_id}): {total_cost} Euro.")
        return total_cost

class Membership:
    def __init__(self, start_date, duration_months, cost_per_month):
        self.start_date = start_date
        self.end_date = start_date + datetime.timedelta(days=30 * duration_months)
        self.cost_per_month = cost_per_month * duration_months

class Class:
    def __init__(self, class_id, name, instructor, date, time):
        self.class_id = class_id
        self.name = name
        self.instructor = instructor
        self.date = date
        self.time = time

    def __str__(self):
        return f"ID: {self.class_id} | Name: {self.name} | Instructor: {self.instructor} | Date: {self.date} | Time: {self.time}"

class YogaClass(Class):
    def __init__(self, class_id, instructor, date, time):
        super().__init__(class_id, "Yoga", instructor, date, time)

class BoxClass(Class):
    def __init__(self, class_id, instructor, date, time):
        super().__init__(class_id, "Box", instructor, date, time)

class SwimmingClass(Class):
    def __init__(self, class_id, instructor, date, time):
        super().__init__(class_id, "Swimming", instructor, date, time)

class GymnasticsClass(Class):
    def __init__(self, class_id, instructor, date, time):
        super().__init__(class_id, "Gymnastics", instructor, date, time)

class FitnessClass(Class):
    def __init__(self, class_id, instructor, date, time):
        super().__init__(class_id, "Fitness", instructor, date, time)


class GymManagement:
    def __init__(self):
        self.users = []
        self.classes = []
        self.attendance = []

    def add_user(self):
        user_id = len(self.users) + 1
        name = input("Enter user name: ")
        email = input("Enter user email: ")
        phone_num = input("Enter user phone number: ")
        age = int(input("Enter user age: "))
        user = User(user_id, name, email, phone_num, age)
        self.users.append(user)
        print(f"User {name} added successfully with ID {user_id}.")

    def add_membership(self):
        user_id = int(input("Enter user ID to assign membership: "))
        user = self.find_user(user_id)
        if not user:
            print("!User not found!")
            return
        duration = int(input("Enter membership duration in months: "))
        cost_per_month = 500
        membership = Membership(datetime.date.today(), duration, cost_per_month)
        user.assign_membership(membership)

    def schedule_class(self):
        class_id = len(self.classes) + 1
        name = input("Enter class type (Yoga/Box/Swimming/Gymnastics/Fitness): ").capitalize()
        instructor = input("Enter instructor name: ")
        date = input("Enter class date (DD-MM-YYYY): ")
        time = input("Enter class time (HH:MM): ")
        if name == "Yoga":
            new_class = YogaClass(class_id, instructor, date, time)
        elif name == "Box":
            new_class = BoxClass(class_id, instructor, date, time)
        elif name == "Swimming":
            new_class = SwimmingClass(class_id, instructor, date, time)
        elif name == "Gymnastics":
            new_class = GymnasticsClass(class_id, instructor, date, time)
        elif name == "Fitness":
            new_class = FitnessClass(class_id, instructor, date, time)
        else:
            print("!Invalid class type!")
            return
        self.classes.append(new_class)
        print(f"Class '{name}' scheduled successfully with ID {class_id}.")

    def add_attendance(self):
        user_id = int(input("Enter user ID: "))
        user = self.find_user(user_id)
        if not user:
            print("!User not found!")
            return
        class_id = int(input("Enter class ID: "))
        clss = self.find_class(class_id)
        if not clss:
            print("!Class not found!")
            return
        self.attendance.append({"user_id": user_id, "class_id": class_id, "date": clss.date, "time": clss.time})
        print(f"{user.name} attended the class '{clss.name}' on {clss.date} at {clss.time}.")

    def report_peak_hours(self):
        if not self.attendance:
            print("!Attendance not found!")
            return
        peak_times = Counter([(entry["date"], entry["time"]) for entry in self.attendance])
        most_common = peak_times.most_common(5)
        print("\n---- Peak Hours ----")
        for (date, time), count in most_common:
            print(f"Date: {date}, Time: {time}, Attendance: {count}")

    def calculate_monthly_income(self):
        current_date = datetime.date.today()
        total_income = 0
        for user in self.users:
            if user.membership:
                if user.membership.start_date <= current_date <= user.membership.end_date:
                    total_income += user.membership.cost_per_month
        print(f"Total monthly income: {total_income} Euro")

    def find_user(self, user_id):
        return next((user for user in self.users if user.user_id == user_id), None)

    def find_class(self, class_id):
        return next((clss for clss in self.classes if clss.class_id == class_id), None)

    def view_users(self):
        if not self.users:
            print("!User not found!")
            return
        print("\n---- User List ----")
        for user in self.users:
            membership_status = (f"Membership active until {user.membership.end_date}" if user.membership else "No Membership")
            print(f"ID: {user.user_id} | Name: {user.name} | Email: {user.email} | Phone: {user.phone_num} | {membership_status}")

    def view_classes(self):
        if not self.classes:
            print("!Class not found!")
            return
        print("\n---- Class Schedule ----")
        for clss in self.classes:
            print(clss)

    def main_menu(self):
        while True:
            print("\n---- Welcome to Management ----")
            print("1) Add User")
            print("2) Add Membership")
            print("3) View Users")
            print("4) Schedule Class")
            print("5) View Classes")
            print("6) Add Attendance")
            print("7) Peak Hours")
            print("8) Billing")
            print("9) Monthly Income")
            print("10) Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_user()
            elif choice == "2":
                self.add_membership()
            elif choice == "3":
                self.view_users()
            elif choice == "4":
                self.schedule_class()
            elif choice == "5":
                self.view_classes()
            elif choice == "6":
                self.add_attendance()
            elif choice == "7":
                self.report_peak_hours()
            elif choice == "8":
                user_id = int(input("Enter user ID for billing: "))
                user = self.find_user(user_id)
                if user:
                    user.calculate_billing()
            elif choice == "9":
                self.calculate_monthly_income()
            elif choice == "10":
                print("\n---- Have a nice day! ----")
                break
            else:
                print("\n!Invalid choice. Please select 1 to 10!")

if __name__ == "__main__":
    gym_management = GymManagement()
    gym_management.main_menu()

