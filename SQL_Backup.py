import subprocess
import datetime

ct = datetime.datetime.now()

# Define database connection details
host = "localhost"
user = "root"
password = "Hashini@123"
database = "coconut"

backup_file = "C:\Hashini\AV_IOT\coconut\Data\backup.sql"

def backup():
# Execute the mysqldump command
    command = f"mysqldump -h{host} -u{user} -p{password} {database} > {backup_file}"
    process = subprocess.run(command, shell=True)

    # Print out status messages based on the return code
    if process.returncode == 0:
        print("Database backup completed successfully.")
    else:
        print(f"Database backup failed with return code {process.returncode}.")