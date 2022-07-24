# Description

This application parses a migration package, determines the migration sequence (if it exists), and executes the migration according to the determined sequence.


# How to run

## 1. Generate dependency file using pipreqs package:

### install pipreqs
        pip install pipreqs

### generate dependency file
        pipreqs <path to base migration directory> --savepath requirements.txt

## 2. Install dependencies with:
        pip install -r requirements.txt

## 3. Execute sample migration:
        py parser.py

## 4. Execute migration in a different directory
        base_dir="<path to base migration directory>" \
        py parser.py


# Assumptions
- All migration scripts exist in one parent directory, no sub-directories
- No migration script has more than one downstream file
- Only one migration sequence exists in a given package

# Test Cases

## 1.  Ideal
        py parser.py
        
### Expected Output:

    **************************************************************************************
    Migration files would be applied in below sequence

    1de5a8c20056(1de5a8c20056_initial_migration_include.py) -> 6dd757e58240(6dd757e58240_user_group_migrations_addition_include.py) -> 6bbb0ed8668e(6bbb0ed8668e_add_unique_id_in_integrations_include.py) -> 529d6f7221aa(529d6f7221aa_integrations_column_changes_include.py) -> c28d9110572d(c28d9110572d_integrations_unique_identifier_name_include.py) -> bffbe44bfbc2(bffbe44bfbc2_client_configuration_col_include.py) -> fa137ca2e4f4(fa137ca2e4f4_column_remane_to_name_include.py) -> c5bd1ade54d7(c5bd1ade54d7_rename_vendor_configuration_include.py)
    **************************************************************************************

    Migration successfully completed

## 2.  Invalid revision files
        base_dir=".\tests\test_invalid_revision_files" \
        py parser.py

### Expected Output:

    Cannot determine position of the following files
    Unable to link nodes, cannot determine first migration file

## 3.  Missing down revision files
        base_dir=".\tests\test_missing_down_revision" \
        py parser.py

### Expected Output:

    Cannot determine position of the following files
    Unable to link nodes, cannot determine first migration file

## 4.  Missing module in migration script
        base_dir=".\tests\test_missing_module" \
        py parser.py

### Expected Output:

    Exception: No module named 'missing_module'
    Ensure 'missing_module' module is present in requirements.txt and installed properly

## 5.  Multiple downstream files
        base_dir=".\tests\test_multiple_downstreams" \
        py parser.py
        
### Expected Output:

    Exception: 6dd757e58240_user_group_migrations_addition_include.py has more than 1 downstream files...

            check the files below...

            **************************************************************************************
            6bbb0ed8668e_add_unique_id_in_integrations_include.py
            2de5a8c20056_test_multiple_downstrams.py
            **************************************************************************************

## 6.  Multiple files with no down revisions
        base_dir=".\tests\test_multiple_heads" \
        py parser.py
        
### Expected Output:

    Exception: Cannot determine first migration script...

        Multiple head migration nodes exist in the package, check the files below...
        **************************************************************************************
        1de5a8c20056_initial_migration_include.py
        2de5a8c20056_test_multiple_heads.py
        **************************************************************************************

## 7.  No head exists in migration package
        base_dir=".\tests\test_no_head" \
        py parser.py
        
### Expected Output:

    Cannot determine position of the following files
    **************************************************************************************
    1de5a8c20056_initial_migration_include.py

    **************************************************************************************

    Exception: Unable to link nodes, cannot determine first migration file

## 8.  Error during migration (test roll back)
        base_dir=".\tests\test_roll_back" \
        py parser.py
        
### Expected Output:
