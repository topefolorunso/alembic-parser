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
- The migration package contains at least 1 migration script
- All migration scripts exist in one parent directory, no sub-directories
- All migration scripts are valid migration scripts i.e they contain valid revision and down_revision parameters
- Only one migration sequence exists in a given package
- No migration script has more than one downstream file
- All package dependencies are included in the requirements.txt file and are pip installed properly


# Test Cases

## 1.  Ideal
        py parser.py
        
### Expected Output:

    <truncated log message>
    **************************************************************************************
    Migration files would be applied in below sequence

    1de5a8c20056(1de5a8c20056_initial_migration_include.py) -> 6dd757e58240(6dd757e58240_user_group_migrations_addition_include.py) -> 6bbb0ed8668e(6bbb0ed8668e_add_unique_id_in_integrations_include.py) -> 529d6f7221aa(529d6f7221aa_integrations_column_changes_include.py) -> c28d9110572d(c28d9110572d_integrations_unique_identifier_name_include.py) -> bffbe44bfbc2(bffbe44bfbc2_client_configuration_col_include.py) -> fa137ca2e4f4(fa137ca2e4f4_column_remane_to_name_include.py) -> c5bd1ade54d7(c5bd1ade54d7_rename_vendor_configuration_include.py)
    **************************************************************************************
    <truncated log message>
    Migration successfully completed

## 2.  Invalid revision files
        base_dir="..\test_data\test_invalid_revision_files" \
        py parser.py

### Expected Output:

    <truncated log message>
    Cannot determine position of the following files
    **************************************************************************************
    2de5a8c20056_test_no_down_revision.py

    2de5a8c20056_test_no_revision_id.py

    **************************************************************************************
    <truncated log message>

    Exception: Unable to link nodes, cannot determine first migration file

## 3.  Missing down revision files
        base_dir="..\test_data\test_missing_down_revision" \
        py parser.py

### Expected Output:
    <truncated log message>
    Cannot determine position of the following files
    **************************************************************************************
    2de5a8c20056_missing_down_revision.py

    **************************************************************************************
    <truncated log message>

    Exception: Unable to link nodes, cannot determine first migration file

## 4.  Missing module in migration script
        base_dir="..\test_data\test_missing_module" \
        py parser.py

### Expected Output:

    <truncated log message>

    Exception: No module named 'missing_module'
    Ensure 'missing_module' module is present in requirements.txt and installed properly

## 5.  Multiple downstream files
        base_dir="..\test_data\test_multiple_downstreams" \
        py parser.py
        
### Expected Output:

    <truncated log message>
    Exception: 6dd757e58240_user_group_migrations_addition_include.py has more than 1 downstream files...

                check the files below...

                **************************************************************************************
                6bbb0ed8668e_add_unique_id_in_integrations_include.py
                2de5a8c20056_test_multiple_downstrams.py
                **************************************************************************************

## 6.  Multiple files with no down revisions
        base_dir="..\test_data\test_multiple_heads" \
        py parser.py
        
### Expected Output (disallowing multiple heads):

    <truncated log message>

    Exception: Cannot determine first migration script...

            Multiple head migration nodes exist in the package, check the files below...
            **************************************************************************************
            1de5a8c20056_initial_migration_include.py
            2de5a8c20056_test_multiple_heads.py
            **************************************************************************************

### Expected Output (allowing multiple heads):

    <truncated log message>
    generating migration sequence 1...
    **************************************************************************************
    Migration files would be applied in below sequence

    1de5a8c20056(1de5a8c20056_initial_migration_include.py)
    **************************************************************************************
    generating migration sequence 2...
    **************************************************************************************
    Migration files would be applied in below sequence

    2de5a8c20056(2de5a8c20056_test_multiple_heads.py)
    **************************************************************************************
    <truncated log message>


## 7.  No head exists in migration package
        base_dir="..\test_data\test_no_head" \
        py parser.py
        
### Expected Output:

    <truncated log message>
    Cannot determine position of the following files
    **************************************************************************************
    1de5a8c20056_initial_migration_include.py

    **************************************************************************************
    <truncated log message>

    Exception: Unable to link nodes, cannot determine first migration file

## 8.  Error during migration (test roll back)
        base_dir="..\test_data\test_roll_back" \
        py parser.py
        
### Expected Output:

    <truncated log message>
    **************************************************************************************
    Migration files would be applied in below sequence

    1de5a8c20056(1de5a8c20056_initial_migration_include.py) -> 6dd757e58240(6dd757e58240_user_group_migrations_addition_include.py) -> 6bbb0ed8668e(6bbb0ed8668e_add_unique_id_in_integrations_include.py) -> 529d6f7221aa(529d6f7221aa_integrations_column_changes_include.py) -> c28d9110572d(c28d9110572d_integrations_unique_identifier_name_include.py) -> bffbe44bfbc2(bffbe44bfbc2_client_configuration_col_include.py) -> fa137ca2e4f4(fa137ca2e4f4_column_remane_to_name_include.py) -> c5bd1ade54d7(c5bd1ade54d7_rename_vendor_configuration_include.py)
    **************************************************************************************
    <truncated log message>
    **************************************************************************************
    Problem with migration file c5bd1ade54d7_rename_vendor_configuration_include.py...
    commencing roll back actions...
    **************************************************************************************
    <truncated log message>

    roll back successfull