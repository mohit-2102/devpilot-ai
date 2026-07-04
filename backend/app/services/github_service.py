import tempfile
from pathlib import Path
import subprocess
# from app.services.parser_service import analyze_repository


def clone_repository(url: str):
    temp_dir = Path(tempfile.mkdtemp())
    print(temp_dir)
    repo_path = temp_dir / "repository"
    result = subprocess.run(
        [
            "git",
            "clone",
            url,
            str(repo_path),
        ],
        capture_output=True,
        text=True,
        timeout=60
        )
    print(result.returncode)
    print(result.stdout)
    print(result.stderr)
    from app.services.parser_service import analyze_repository

    analysis = analyze_repository(str(repo_path))
    
    return {
        "success": result.returncode == 0,
        "analysis": analysis,
    } 