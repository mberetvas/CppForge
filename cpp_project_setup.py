#!/usr/bin/env python3
"""
C++ Project Setup Script

This script automates the setup of a new C++ project by creating the necessary
folder structure, initializing a Git repository, and adding CMake, CI/CD,
and other modern development tools.
"""

import re
import subprocess
import sys
import logging
from pathlib import Path

# Constants
SUBDIRS = ["src", "include", "lib", "bin", "tests", "docs"]
GITIGNORE_CONTENT = """# Compiled object files
*.o
*.obj
*.so
*.a
*.dll
*.dylib

# Executables
*.exe
*.out
*.app

# Build directories
build/
bin/
lib/

# IDE files
.vscode/
.idea/
.history/
*.suo
*.user
*.sdf
*.opensdf
*.sln.docstates

# CMake files
CMakeCache.txt
CMakeFiles/
cmake_install.cmake
Makefile

# Debug files
*.dSYM/
*.pdb
*.ilk

# Temporary files
*.log
*.tlog
*.tmp
*.temp
*.swp
*~

# OS specific files
.DS_Store
Thumbs.db
"""

logging.basicConfig(level=logging.INFO, format="%(message)s")


def is_valid_project_name(name: str) -> bool:
    """
    Check if the project name contains only valid characters.

    Args:
        name (str): The project name to validate

    Returns:
        bool: True if the name is valid, False otherwise
    """
    return bool(re.match(r"^[a-zA-Z0-9_-]+$", name))


def create_directory(path: Path) -> bool:
    """
    Create a directory if it doesn't exist.

    Args:
        path (Path): The directory path to create

    Returns:
        bool: True if directory was created or already exists, False on error
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
        logging.info("Created directory: %s", path)
        return True
    except (PermissionError, OSError) as e:
        logging.error("Error creating directory %s: %s", path, e)
        return False


def initialize_git_repo(path: Path) -> bool:
    """
    Initialize a Git repository in the specified path.

    Args:
        path (Path): The path where the Git repository should be initialized

    Returns:
        bool: True if repository was initialized successfully, False otherwise
    """
    try:
        subprocess.run(
            ["git", "init"], cwd=path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        logging.info("Initialized Git repository in: %s", path)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.error("Error initializing Git repository: %s", e)
        return False


def create_file(path: Path, content: str) -> bool:
    """
    Create a file with the specified content.

    Args:
        path (Path): The path where the file should be created
        content (str): The content to write to the file

    Returns:
        bool: True if the file was created successfully, False otherwise
    """
    try:
        path.write_text(content)
        logging.info("Created file: %s", path)
        return True
    except (PermissionError, OSError) as e:
        logging.error("Error creating file %s: %s", path, e)
        return False


def create_cmake_files(path: Path, project_name: str) -> bool:
    """
    Create CMakeLists.txt files for the project.

    Args:
        path (Path): The root path of the project
        project_name (str): The name of the project

    Returns:
        bool: True if files were created successfully, False otherwise
    """
    root_cmake_content = f"""cmake_minimum_required(VERSION 3.10)
project({project_name} VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Set output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)

# Compiler flags
if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU" OR CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    add_compile_options(-Wall -Wextra -Wpedantic)
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    add_compile_options(/W4 /permissive-)
endif()

add_subdirectory(src)
add_subdirectory(tests)
add_subdirectory(docs)
"""
    src_cmake_content = """add_executable(${PROJECT_NAME} main.cpp)
"""
    tests_cmake_content = """enable_testing()
add_executable(${PROJECT_NAME}_test test_main.cpp)
add_test(NAME ${PROJECT_NAME}_test COMMAND ${PROJECT_NAME}_test)
"""
    docs_cmake_content = """find_package(Doxygen)
if (DOXYGEN_FOUND)
    configure_file(Doxyfile.in Doxyfile @ONLY)
    add_custom_target(doc
        COMMAND ${DOXYGEN_EXECUTABLE} Doxyfile
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        COMMENT "Generating API documentation with Doxygen"
        VERBATIM)
endif()
"""
    try:
        create_file(path / "CMakeLists.txt", root_cmake_content)
        create_file(path / "src" / "CMakeLists.txt", src_cmake_content)
        create_file(path / "tests" / "CMakeLists.txt", tests_cmake_content)
        create_file(path / "docs" / "CMakeLists.txt", docs_cmake_content)
        logging.info("Created CMakeLists.txt files.")
        return True
    except (OSError, IOError) as e:
        logging.error("Error creating CMakeLists.txt files: %s", e)
        return False


def setup_cpp_project():
    """
    Main function to set up a C++ project.

    This function prompts the user for a project name, creates the necessary folder structure,
    initializes a Git repository, and creates a .gitignore file.
    """
    logging.info("C++ Project Setup Tool")
    logging.info("======================")

    # Prompt user for project name
    while True:
        project_name = input("Enter project name (alphanumeric, underscores, and hyphens only): ")
        if not project_name:
            logging.error("Project name cannot be empty. Please try again.")
            continue

        if not is_valid_project_name(project_name):
            logging.error(
                "Invalid project name. Please use only alphanumeric characters, underscores, and hyphens."
            )
            continue

        break

    # Create project root directory
    root_dir = Path(project_name)
    if not create_directory(root_dir):
        logging.error("Failed to create project directory. Setup aborted.")
        return

    # Create subdirectories
    for subdir in SUBDIRS:
        subdir_path = root_dir / subdir
        if not create_directory(subdir_path):
            logging.warning("Failed to create %s directory. Continuing with setup...", subdir)

    # Initialize Git repository
    if not initialize_git_repo(root_dir):
        logging.warning("Failed to initialize Git repository. Continuing with setup...")

    # Create .gitignore file
    if not create_file(root_dir / ".gitignore", GITIGNORE_CONTENT):
        logging.warning("Failed to create .gitignore file. Continuing with setup...")

    # Create README.md file
    readme_content = f"""# {project_name}

A C++ project.

## Directory Structure

- `src/`: Source files
- `include/`: Header files
- `lib/`: Libraries
- `bin/`: Executable files
- `tests/`: Unit tests
- `docs/`: Documentation

## Build Instructions

[Add build instructions here]

## Setup Instructions

To set up this project, run the `cpp_project_setup.py` script in the folder where you want the C++ project folder to be created. For example:

```sh
python path/to/cpp_project_setup.py
```

## License

[Add license information here]
"""
    if not create_file(root_dir / "README.md", readme_content):
        logging.warning("Failed to create README.md file. Continuing with setup...")

    # Create CMakeLists.txt files
    if not create_cmake_files(root_dir, project_name):
        logging.warning("Failed to create CMakeLists.txt files. Continuing with setup...")

    # Create basic source files
    main_cpp_content = """#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
"""
    if not create_file(root_dir / "src" / "main.cpp", main_cpp_content):
        logging.warning("Failed to create main.cpp file. Continuing with setup...")

    header_content = """#ifndef PROJECT_HEADER_H
#define PROJECT_HEADER_H

// Add your header content here

#endif // PROJECT_HEADER_H
"""
    if not create_file(root_dir / "include" / "project_header.h", header_content):
        logging.warning("Failed to create header file. Continuing with setup...")

    test_content = """#include <iostream>

int main() {
    std::cout << "Running tests..." << std::endl;
    // Add your test code here
    return 0;
}
"""
    if not create_file(root_dir / "tests" / "test_main.cpp", test_content):
        logging.warning("Failed to create test file. Continuing with setup...")

    logging.info("\nProject setup complete!")
    logging.info("Project '%s' has been created with the following structure:", project_name)
    logging.info("- %s/", project_name)
    for subdir in SUBDIRS:
        logging.info("  - %s/", subdir)
    logging.info("  - .gitignore")
    logging.info("  - README.md")
    logging.info("  - CMakeLists.txt")
    logging.info("\nYou can now navigate to your project directory: cd %s", project_name)


if __name__ == "__main__":
    try:
        setup_cpp_project()
    except KeyboardInterrupt:
        logging.error("\nSetup aborted by user.")
        sys.exit(1)
