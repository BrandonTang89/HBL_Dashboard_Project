from hashing_helper import *

for item in pass_dict.items():
    f = open("password_dir/" + item[0] + "_passwords.txt", "w")
    f.write(item[1] + "\n")
    f.close()

for item in (personal_pass_dict.items()):
    f = open("password_dir/" + item[0] + "_passwords.txt", "a")
    for index, password in enumerate(item[1]):
        # print(password)
        f.write(str(index+1) + " " + password + "\n")

    f.close()

print(pass_dict)