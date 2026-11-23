import json
import os
import sys
from pathlib import Path

metrics_file = Path(os.environ.get("METRICS_FILE", "artifacts/monitor_metrics.json"))
baseline_accuracy = float(os.environ.get("BASELINE_ACCURACY", "0.892"))
allowed_drop = float(os.environ.get("ALLOWED_ACCURACY_DROP", "0.10"))

if not metrics_file.exists():
    print(f"ERROR: Metrics file not found: {metrics_file}")
    sys.exit(2)

metrics = json.loads(metrics_file.read_text())
current_accuracy = float(metrics["accuracy"])
threshold = baseline_accuracy - allowed_drop

print(f"Baseline accuracy: {baseline_accuracy:.4f}")
print(f"Current accuracy:  {current_accuracy:.4f}")
print(f"Allowed drop:      {allowed_drop:.4f}")
print(f"Drift threshold:   {threshold:.4f}")

if current_accuracy < threshold:
    print("DRIFT DETECTED")
    print("Retraining is required.")
    sys.exit(10)
else:
    print("NO DRIFT")
    print("Model remains within the accepted performance range.")
    sys.exit(0)