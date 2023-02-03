import os

BASEDIR = os.environ["BASEDIR"]
with open(f"{BASEDIR}/number") as f:
    num = int(f.read())

with open(f"{BASEDIR}/files/a{num}.txt", "w"):
    pass

num += 1

with open(f"{BASEDIR}/number", "w") as f:
    f.write(str(num))