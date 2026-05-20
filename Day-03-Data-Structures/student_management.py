# ----- Introduction to list -----#
##Tuples are immutable data structures, meaning they cannot be changed.

students = ['Marta','Antonio']
std_marks =[20,15]
print("Hello", students[1], "Your marks is: ", std_marks[1])
print("Hello", students[0], "Your marks is: ", std_marks[0])


# ----- Introduction to tuples -----#
## Tuples are immutable data structures, meaning they cannot be changed. They are defined using parentheses () instead of square brackets [].
students_tuple = ('Marta','Antonio')
std_marks_tuple =(12,40)
print("Hello", students_tuple[1], "Your marks is: ", std_marks_tuple[1])
print("Hello", students_tuple[0], "Your marks is: ", std_marks_tuple[0])    


# ----- Introduction to dictionary -----#    
## Dictionaries are mutable data structures that store key-value pairs. They are defined using curly braces {} and each key is separated from its value by a colon (:). The keys must be unique and immutable, while the values can be of any data type.

students_dict = {
    "name": "Miguel",
    "marks": 90,
    "age": 20,
}
print(students_dict)