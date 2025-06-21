from pathlib import Path
from loguru import logger


def log_dir_structure(start_path: Path | str, indent: str = ""):
    allowed_dirs = {"src", "tests"}  # Only include these directories

    for path in sorted(Path(start_path).iterdir()):
        if path.name == "__pycache__" or path.suffix == ".pyc":
            continue
        if path.is_dir() and path.name not in allowed_dirs and indent == "":
            continue  # Skip top-level dirs not in allowed_dirs
        logger.info(indent + "├── " + path.name)
        if path.is_dir():
            log_dir_structure(path, indent + "│   ")