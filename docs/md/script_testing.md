# Testing Script

## Unit testing for ml microservice

```bash
# Step 1: (Optional) Setup environment variables if needed
export GOOGLE_APPLICATION_CREDENTIALS="src/ml/creds/your-service-account.json"

# Step 2a: Run pytest on a specific test file
pytest src/ml/tests/tools/test_wdm_parser.py -v

# Step 2b: Run pytest on the full test suite in the 'tests' folder
pytest src/ml/tests/ -v

# Optional: Disable warnings for cleaner output
pytest src/ml/tests/ -v -p no:warnings

# Optional: Run with coverage report
pytest --cov=src/ml src/ml/tests/ -v
```
