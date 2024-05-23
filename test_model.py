import subprocess
import json
import numpy as np
from joblib import load  # Adjusted import for joblib
import json
import sys

def run_feature_extraction(script_path, input_file):
    # Run the feature extraction script and capture its output
    result = subprocess.run(
        ['python', script_path, input_file],
        capture_output=True,
        text=True
    )
    # Check for errors in the script execution
    if result.returncode != 0:
        print("Error running feature extraction script:")
        print(result.stderr)
        return None
    # Return the stdout which contains the JSON output
    return result.stdout

def model(input_csv):
    # Load the trained model
    loaded_model = load('/home/ajh/knn.joblib')

    # Run feature extraction
    feature_script = '/home/ajh/feature_extraction.py'
    output = run_feature_extraction(feature_script, input_csv)

    if output is None:
        return

    # Parse the output as JSON
    try:
        X_test = np.array(json.loads(output))
    except Exception as e:
        print("Error converting output to numpy array:", e)
        return

    # Ensure the data is in the correct numerical format
    X_test = X_test.astype(float)

    # Make predictions
    predictions = loaded_model.predict(X_test)
    print(predictions[1])

if __name__ == "__main__":
    input_csv = sys.argv[1]
    m = model(input_csv)

    
