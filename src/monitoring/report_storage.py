import json
from pathlib import Path

# ye function monitoring report ko JSON file me save krega.
# reports ko project ke reports dictionary me store kiya jayega.
def save_monitoring_report(report, output_path):
    # output path ko Path object me convert kr rhe hai.
    output_path = Path(output_path)

    # parent directory exist nhi krti hai to automatically create hogi.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # monitoring report ko formatted JSON file me save kr rhe hai.
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

# ye function previously saved monitoring report ko
# JSON file se read krke Python dictionary me return krega.
def load_monitoring_report(input_path):
    # input path ko Path object me convert kr rhe hai.
    input_path = Path(input_path)

    # JSON file ko read mode me open kr rhe hai.
    with input_path.open("r", encoding="utf-8") as file:
        # JSON data ko Python dictionary me convert kr rhe hai.
        report = json.load(file)

    # loaded monitoring report return kr rhe hai.
    return report