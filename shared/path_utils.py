import os

def get_project_root() -> str:
    """Return the absolute path to the project root directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

def resolve_memory_path(relative_path: str) -> str:
    """
    Resolve full path to memory files stored under memory_store/.

    :param relative_path: Path relative to memory_store/, e.g. 'faiss.index'
    :return: Absolute path
    """
    full_path = os.path.join(get_project_root(), "memory_store", relative_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Memory file not found: {full_path}")
    return full_path
