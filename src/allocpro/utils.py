from pathlib import Path


def find_project_root_directory(max_parent_dirs: int = 3) -> Path:
    root_dir = None
    current_dir = Path.cwd()
    src_dirs = list(current_dir.glob("**/src"))
    if len(src_dirs) > 1:
        raise RuntimeError("Cannot determine the project source directory. "
                           f"Multiple 'src' directories found inside {current_dir}:\n"
                           "\n".join(str(src_dir) for src_dir in src_dirs))
    if len(src_dirs) == 1:
        src_dir = src_dirs[0]
        root_dir = src_dir.parent

    while root_dir is None and max_parent_dirs > 0:
        max_parent_dirs -= 1
        current_dir = current_dir.parent
        if current_dir.name == "src":
            root_dir = current_dir.parent
        else:
            src_dirs = list(current_dir.glob("**/src"))
            if len(src_dirs) == 1:
                src_dir = src_dirs[0]
                root_dir = src_dir.parent

    if root_dir is None:
        raise FileNotFoundError(
            "Failed to find project root directory. Search exceeded maximum number of "
            "parent directories that project root directory can be searched on."
        )
    return root_dir
