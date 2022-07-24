# How to run

1. Generate dependency file with pipreqs:
    ```pip install pipreqs```
    ```cd <path to parser directory>```
    ```pipreqs <path to base migration folder> --savepath requirements.txt```
2. Install dependencies with 
    `pip install -r requirements.txt`
3. Execute sample migration
    `py parser.py`
4. Execute migration in a different directory
    ```
    base_dir="<path to base migration folder>" \
    py parser.py
    ```

# Assumptions
- all migration scripts exist in one parent directory, no sub-directories
- no migration script has more than one downstream file
- only one sequence exists in a given package