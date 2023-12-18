from stega_encryptor import imageEncrypt
from stega_decryptor import imageDecrypt

options = -1
print("### Welcome to educational Steganografy project created by Quasar (ITH-1 2023) ###")
print("### Look, you have some options below: ")
print("#-> Input (0), if you want to encrypt a message;\n#-> Input (1), if you want to decrypt one.")
print("### Please, choose the option from above: ", end="")
while True:
    try:
        options = int(input())
        if options != 1 and options != 0:
            print("#?# There is no such option. Please, try again: ", end="")
            continue
        break
    except ValueError:
        print("#?# Hmm... I guess this is not a number. Please, try again: ", end="")
        continue

print("### Please, put the image you want to use in the same directory, where program is being executed.")
print("### After that, please, enter it's name with file extension.")
if options == 0:
    print("### Encrypt ###")
    while True:
        try:
            imageEncrypt(input("#-> Image to use: "))
            break
        except FileNotFoundError:
            print("#!# No such file in the current directory :(")
            continue
else:
    print("### Decrypt ###")
    while True:
        try:
            imageDecrypt(input("#-> Image to decrypt: "))
            break
        except FileNotFoundError:
            print("#!# No such file in the current directory :(")
            continue



