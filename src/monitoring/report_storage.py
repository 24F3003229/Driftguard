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

# ye function reports directory me available monitoring reports me se
# sbse recently modified report ko find krke return krega.
def load_latest_monitoring_report(reports_directory):
    # reports directory ko Path object me convert kr rhe hai.
    reports_directory = Path(reports_directory)

    # directory me sirf JSON monitoring report files find kr rhe hai.
    report_files = list(reports_directory.glob("*.json"))

    # agr koi monitoring report available nhi hai,
    # to clear error raise kr rhe hai.
    if not report_files:
        raise FileNotFoundError(
            "No monitoring reports found."
        )

    # files ko modification time ke according sort kr rhe hai.
    # sbse recently modified files last me hogi.
    latest_report = max(
        report_files,
        key=lambda file_path: file_path.stat().st_mtime,
    )

    # latest JSON report ke load krke return kr rhe hai.
    return load_monitoring_report(latest_report)