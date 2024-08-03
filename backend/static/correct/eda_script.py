import subprocess

for i in range(1, 50 + 1):
    result = subprocess.run(["make", "-l"], capture_output=True, text=True)
    print(result.stdout)
