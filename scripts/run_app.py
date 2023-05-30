import subprocess
from app.config import port, entrypoint

# Run the command
subprocess.run(["poetry", "run", "flask", "run", "--port", port], env={"FLASK_APP": entrypoint})