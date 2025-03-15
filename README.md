# C++ Project Setup Tool

This repository contains a Python script that automates the setup of a new C++ project by creating the necessary folder structure, initializing a Git repository, and adding CMake, CI/CD, and other modern development tools.

## Features

- Creates a standard C++ project folder structure
- Initializes a Git repository
- Generates `.gitignore` file
- Creates `CMakeLists.txt` files for building the project
- Adds a basic `README.md` file
- Sets up initial source files and headers
- Configures unit testing with CMake

## Folder Structure

The generated project will have the following structure:

```
project_name/
├── src/            # Source files
├── include/        # Header files
├── lib/            # Libraries
├── bin/            # Executable files
├── tests/          # Unit tests
├── docs/           # Documentation
├── .gitignore      # Git ignore file
├── README.md       # Project README file
└── CMakeLists.txt  # Root CMake file
```

## Usage

1. Clone this repository:
    ```sh
    git clone https://github.com/yourusername/cpp_project_setup_tool.git
    cd cpp_project_setup_tool
    ```

2. Run the setup script in the folder where you want the C++ project folder to be created:
    ```sh
    python3 cpp_project_setup.py
    ```

3. Follow the prompts to enter your project name.

4. Navigate to your new project directory:
    ```sh
    cd your_project_name
    ```

5. Build your project using CMake:
    ```sh
    mkdir build
    cd build
    cmake ..
    make
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.