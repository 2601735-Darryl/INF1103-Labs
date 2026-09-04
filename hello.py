print("=====================")
print("Welcome here")
print("My first post!")
print("=====================")

username = input("Enter Username: ")
age = int(input("Enter Age: "))
category = input("Enter Content Category: ")

print("\nInstagram Profile")
print("====================")
print(f'Username : {username}')
print(f'Age : {age}')
print(f'Category : {category}')

if age>40 and category == "fun":
    print('You are old, what is fun for you?')