import os

c = os.getcwd()
print(c)

for f in os.listdir():
    if "-" in f:
        print(f)
        new_name = f.replace('-','_')
        os.rename(f, new_name)