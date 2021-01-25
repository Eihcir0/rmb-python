import subprocess


def run_command(command):
    # bashCommand = "cwm --rdf test.rdf --ntriples > test.nt"
    # bashCommand = "python manage.py makemigrations"

    # This is the magic that runs the command:
    # subprocess.run([command], stdout=subprocess.PIPE).stdout.decode('utf-8')
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output, error
