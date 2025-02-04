import subprocess  
import os 

# Define the path to activate the virtual environment on Windows
env_path = os.path.join('myenv', 'Scripts', 'activate.bat')

# List of commands to run: start Django server, run Celery worker, and run Celery beat
commands = [
    f'call {env_path} && python manage.py runserver',  # Command to start Django development server
    f'call {env_path} && celery -A jobs.celery worker --loglevel=info',  # Command to start Celery worker
    f'call {env_path} && celery -A jobs beat --loglevel=info'  # Command to start Celery beat
]

# List to keep track of the processes
processes = []

try:
    # Loop through each command in the list and execute it
    for command in commands:
        print(f'Running: {command}')  # Print the command being run
        process = subprocess.Popen(command, shell=True)  # Start the command as a subprocess
        processes.append(process)  # Add the process to the processes list

    # Wait for all processes to finish
    for process in processes:
        process.wait()

except Exception as e:  # Handle any exceptions that occur during execution
    print(f'An error occurred: {e}')
finally:
    # After finishing or encountering an error, terminate any processes that are still running
    for process in processes:
        if process.poll() is None:  # Check if the process is still running
            process.terminate()  # Terminate the process if it's still running
