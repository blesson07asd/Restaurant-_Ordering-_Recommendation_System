student={}

def add_student():
    name = input("Enter a name: ")
    age = input("Enter the age: ")
    studentid = input("Enter the ID: ")
    marks = float(input("Enter marks: "))
    student[studentid] = {'name': name, 'age': age, 'studentid': studentid, 'marks': marks}
    print("Student added.\n")


def view_student():
    if not student:
        print("not found")
    for id,info in student.items():
        print(f"id:{id},name:{info['name']},age:{info['age']},studentid:{info['studentid']}")
        print()

def search_student():
    studentid=input("enter an id")
    if studentid in student:
        info=student[studentid]       
        print(f"id:{studentid},name:{info['name']},age:{info['age']},studentid:{info['studentid']}")
    else:
        print("not found")

def average_marks():
    if not student:
        print("not found")
    else:
        total_marks=0
        count=0
        for info in student.values():
            if 'marks' in info:
                total_marks += info['marks']
                count += 1
        average_marks=total_marks/count if count > 0 else 0
        print(f"average marks:{average_marks}")

def save_to_a_file():
    with open("student.txt","w") as f:
        for id,info in student.items():
            f.write(f"id:{id},name:{info['name']},age:{info['age']},studentid:{info['studentid']}\n")

def menu():
    while True:
        print("1.add student")
        print("2.view student")
        print("3.search student")
        print("4.average marks")
        print("5.save to a file")
        print("6.exit")
        choice=input("enter your choice")
        if choice=="1":
            add_student()
        elif choice=="2":
            view_student()
        elif choice=="3":
            search_student()
        elif choice=="4":
            average_marks()
        elif choice=="5":
            save_to_a_file()
        elif choice=="6":
            break
        else:
            print("Invalid choice")
menu()