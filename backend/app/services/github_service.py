import tempfile
from pathlib import Path
import subprocess


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
    return {
        "url": url,
        "temp_directory": str(temp_dir),
        "repository_path": str(repo_path),
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }