import subprocess

whitelist = {
    "list": ["ls", "-la"],
    "current_dir": ["pwd"],
    "whoami": ["whoami"]
}

def run_os_command(data):
    command_key = data.get("command_key")

    if command_key not in whitelist:
        return {"status": "error", "message": "Invalid command_key"}

    command = whitelist[command_key]
    
    try:
        result = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
        return {"status": "success", "output": result}
    
    except subprocess.CalledProcessError as e:
        return {"status": "error", "output": e.output}