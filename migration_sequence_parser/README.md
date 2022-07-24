# Description

This application parses a migration package, determines the migration sequence (if it exists), and executes the migration according to the determined sequence


# How to run

1. Generate dependency file using pipreqs package:
    - install pipreqs
    ```
    pip install pipreqs
    ```

    - navigate to the parser directory
    ```
    cd <path to parser directory>
    ```

    - generate dependency file
    ```
    pipreqs <path to base migration folder> --savepath requirements.txt
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
    base_dir="<path to base migration folder>" \
    py parser.py
    ```

# Assumptions
- All migration scripts exist in one parent directory, no sub-directories
- No migration script has more than one downstream file
- Only one migration sequence exists in a given package
