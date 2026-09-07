import ast
import os
import sys

class GlasswingSecurityAnalyzer(ast.NodeVisitor):
    """
    Project Glasswing: Defensive Static Analysis Engine.
    Scans abstract syntax trees (AST) for insecure code patterns.
    """
    def __init__(self, filename):
        self.filename = filename
        self.vulnerabilities = []

    def log_vuln(self, node, severity, message):
        self.vulnerabilities.append({
            "line": node.lineno,
            "severity": severity,
            "message": message
        })

    def visit_Call(self, node):
        # Detect dangerous function calls
        if isinstance(node.func, ast.Name):
            if node.func.id in ['eval', 'exec']:
                self.log_vuln(node, "CRITICAL", f"Use of dangerous function '{node.func.id}' detected. Allows arbitrary code execution.")
        
        # Detect raw OS commands
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == 'system' and isinstance(node.func.value, ast.Name) and node.func.value.id == 'os':
                self.log_vuln(node, "HIGH", "Use of os.system() detected. Potential command injection vector.")

        self.generic_visit(node)

    def visit_Assign(self, node):
        # Detect hardcoded secrets
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id.lower()
                if any(keyword in var_name for keyword in ['password', 'secret', 'api_key', 'token']):
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        self.log_vuln(node, "MEDIUM", f"Hardcoded credential/secret assigned to '{target.id}'.")
        
        self.generic_visit(node)

def analyze_file(filepath):
    print(f"[*] GLASSWING ENGINE: Analyzing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)
    except Exception as e:
        print(f"[!] Failed to parse {filepath}: {e}")
        return

    analyzer = GlasswingSecurityAnalyzer(filepath)
    analyzer.visit(tree)

    if analyzer.vulnerabilities:
        print(f"[!] {len(analyzer.vulnerabilities)} vulnerabilities discovered in {filepath}:")
        for v in analyzer.vulnerabilities:
            print(f"    - Line {v['line']} | [{v['severity']}] {v['message']}")
    else:
        print(f"[+] {filepath} passed security heuristics. No obvious vectors found.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_file(sys.argv[1])
    else:
        print("Usage: python glasswing_analyzer.py <file_to_scan.py>")
