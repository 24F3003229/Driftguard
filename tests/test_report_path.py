from pathlib import Path
from src.monitoring.report_path import (
    create_report_path,
)

# ye test verify krta hai ki generated report path 
# expected reports directory ke andr create ho rha hai.
def test_create_report_path():
    # report path generate kr rhe hai
    report_path = create_report_path()

    # returned value Path object hone chahiye.
    assert isinstance(report_path, Path)

    # report reports directory ke andr honi chahiye.
    assert report_path.parent == Path("reports")

    # filename monitoring_report se start hona chahiye.
    assert report_path.name.startswith(
        "monitoring_report_"
    )

    # filename JSON extension ke sath end hona chahiye.
    assert report_path.name.endswith(".json")