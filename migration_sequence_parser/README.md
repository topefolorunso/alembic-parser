to run the package:
    pip install pipreqs to generate migration package dependencies
    - `pip install pipreqs`
    generate migration dependencies file requirements.txt file
    - run `cd <path to parser directory>`
    - run `pipreqs <path to base migration folder> --savepath requirements.txt`
    install the dependencies
    - `pip install -r requirements.txt`
    - copy the command below to terminal
        ```
        root_dir="<path to base migration folder>" \
        py ~/solution/parser.py
        ```
    - replace `<path to base migration folder>` with the base migration folder path
    - run the command


Your read me should be like this:
1. Generate dependency file with pipreqs:
    `pip install pipreqs`
    `cd <path to parser directory>`
    `pipreqs <path to base migration folder> --savepath requirements.txt`
2. Install dependencies with 
    `pip install -r requirements.txt`
3. Execute sample migration
    `py parser.py`
4. Execute migration in a different directory
    ```
    base_dir="<path to base migration folder>" \
    py parser.py
    ```

assumptions
- all migration scripts exist in one parent directory, no sub-directories
- no migration script has more than one downstream file
- only one sequence exists in a given package