username = ["Admin"] # SB C++ Fuck
userpassword = ["Admin"]
user = input()
password = input()

if user in username:
    if password in userpassword:
        print("Login!")
        exit()
print("Faild!")