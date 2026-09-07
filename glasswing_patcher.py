import re
import os

def patch_vulnerabilities(input_file, output_file):
    print(f"[*] INITIATING AUTONOMOUS REMEDIATION ON {input_file}...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print("[!] File not found.")
        return

    # Patch 1: Replace eval() with safe ast.literal_eval()
    if 'eval(' in code:
        code = "import ast\n" + code.replace('eval(', 'ast.literal_eval(')
        print("    [+] Patched [CRITICAL]: Replaced eval() with safe ast.literal_eval()")

    # Patch 2: Replace os.system with secure subprocess (and shell=False)
    if 'os.system(' in code:
        if 'import subprocess' not in code:
            code = "import subprocess\n" + code
        # Semantic replacement mapping
        code = re.sub(r'os\.system\((.*?)\)', r'subprocess.run([\1], shell=False, check=True)', code)
        print("    [+] Patched [HIGH]: Upgraded os.system() to secure subprocess.run() blocking command injection.")

    # Patch 3: Strip hardcoded secrets and map to Environment Variables
    if re.search(r'(api_key.*?=\s*)["\'].*?["\']', code, re.IGNORECASE):
        code = re.sub(r'(api_key.*?=\s*)["\'].*?["\']', r'\1os.environ.get("GLASSWING_API_KEY_SECURE")', code)
        print("    [+] Patched [MEDIUM]: Stripped hardcoded secret and shifted to environment variable.")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f"[*] REMEDIATION COMPLETE. Secure payload saved to {output_file}")

if __name__ == "__main__":
    patch_vulnerabilities('test_payload.py', 'test_payload_secure.py')
