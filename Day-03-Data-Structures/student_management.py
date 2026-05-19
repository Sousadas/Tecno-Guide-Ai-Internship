students = []

def add_student(name, age):
    students.append({'name': name, 'age': age})

if __name__ == '__main__':
    add_student('Alice', 21)
    add_student('Bob', 22)
    print('Students:', students)
