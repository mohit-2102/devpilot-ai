from pathlib import Path

def detect_framework(repo: Path):
    package_json = repo/"package.json"
    if not package_json.exists():
        return "Unknown"
    
    content = package_json.read_text()
    
    if "next" in content:
        return "Next.js"
    
    if '"react"' in content:
        return "React"
    
    return "Unknown"

def analyze_repository(repository_path: str):
    repo = Path(repository_path)

    total_files = sum(1 for item in repo.rglob("*") if item.is_file())
    
    framework = detect_framework(repo)

    return {
        "exists": repo.exists(),
        "is_directory": repo.is_dir(),
        "total_files": total_files,
        "framework": framework,
    }