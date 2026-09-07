import os

def process_user_input(user_command):
    # CRITICAL: eval allows arbitrary code execution
    result = eval(user_command)
    return result

def backup_database(db_name):
    # HIGH: os.system allows command injection if db_name is tainted
    os.system(f"backup_tool --db {db_name}")

def connect_to_api():
    # MEDIUM: Hardcoded API secret
    api_key_production = "sk_live_1234567890abcdef"
    return api_key_production
