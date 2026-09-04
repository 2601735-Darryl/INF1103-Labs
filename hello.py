print("=====================")
print("Welcome here")
print("My first post!")
print("=====================")

followers = 100
followers += 50 
print (f'Day 1 : {followers}')
followers += 20
print (f'Day 2 : {followers}')
followers += 10
print (f'Day 3 : {followers}')

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