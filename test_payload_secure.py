import subprocess
import ast
import os

def process_user_input(user_command):
    # CRITICAL: eval allows arbitrary code execution
    result = ast.literal_eval(user_command)
    return result

def backup_database(db_name):
    # HIGH: os.system allows command injection if db_name is tainted
    subprocess.run([f"backup_tool --db {db_name}"], shell=False, check=True)

def connect_to_api():
    # MEDIUM: Hardcoded API secret
    api_key_production = os.environ.get("GLASSWING_API_KEY_SECURE")
    return api_key_production
