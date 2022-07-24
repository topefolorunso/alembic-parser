# Description

This application parses a migration package, determines the migration sequence (if it exists), and executes the migration according to the determined sequence.


# How to run

1. Generate dependency file using pipreqs package:
    - install pipreqs
    ```
    pip install pipreqs
    ```
    - generate dependency file
    ```
    cd <path to parser directory>
    pipreqs <path to base migration directory> --savepath requirements.txt
    ```

2. Install dependencies with:
    ```
    pip install -r requirements.txt
    ```

3. Execute sample migration:
    ```
    py parser.py
    ```
    
4. Execute migration in a different directory
    ```
    base_dir="<path to base migration directory>" \
    py parser.py
    ```


# Assumptions
- All migration scripts exist in one parent directory, no sub-directories
- No migration script has more than one downstream file
- Only one migration sequence exists in a given package

# Test Cases

1.  Ideal
    ```
    py parser.py
    ```

2.  Invalid revision files
    ```
    base_dir=".\test_invalid_revision_files" \
    py parser.py
    ```

    Expected Output:

    Cannot determine position of the following files
    Unable to link nodes, cannot determine first migration file

3.  Missing down revision files
    ```
    base_dir=".\test_missing_down_revision" \
    py parser.py
    ```

    Expected Output:

    Cannot determine position of the following files
    Unable to link nodes, cannot determine first migration file

4.
    ```
    base_dir=".\test_missing_module" \
    py parser.py
    ```

    Expected Output:

    Exception: No module named 'missing_module'
    Ensure 'missing_module' module is present in requirements.txt and installed properly

5.
    ```
    base_dir="<path to base migration directory>" \
    py parser.py
    ```

    Expected Output:

    Cannot determine position of the following files
    Unable to link nodes, cannot determine first migration file

6.
    ```
    base_dir="<path to base migration directory>" \
    py parser.py
    ```

7.
    ```
    base_dir="<path to base migration directory>" \
    py parser.py
    ```

8.
    ```
    base_dir="<path to base migration directory>" \
    py parser.py
    ```
