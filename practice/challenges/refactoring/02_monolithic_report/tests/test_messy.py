"""Tests for the report generator.

These must pass before AND after your refactoring.

Run with:
    cd practice/challenges/refactoring/02_monolithic_report
    python -m pytest tests/
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from messy import generate_report


def _write_test_csv(filepath, rows):
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "category", "product", "quantity", "unit_price"])
        for row in rows:
            writer.writerow(row)


SAMPLE_DATA = [
    ["2024-01-05", "Electronics", "Widget", "3", "25.00"],
    ["2024-01-05", "Electronics", "Gadget", "1", "150.00"],
    ["2024-01-12", "Books", "Novel", "4", "12.99"],
    ["2024-01-20", "Electronics", "Widget", "2", "25.00"],
    ["2024-01-20", "Books", "Textbook", "1", "89.99"],
    ["2024-02-03", "Electronics", "Widget", "5", "25.00"],
    ["2024-02-10", "Books", "Novel", "2", "12.99"],
]


def test_basic_report(tmp_path):
    input_csv = str(tmp_path / "sales.csv")
    output_txt = str(tmp_path / "report.txt")
    _write_test_csv(input_csv, SAMPLE_DATA)

    result = generate_report(input_csv, output_txt, 2024, 1)

    assert result["total"] == 416.95
    assert "Electronics" in result["categories"]
    assert "Books" in result["categories"]
    assert result["categories"]["Electronics"] == 275.0
    assert result["categories"]["Books"] == 141.95
    assert result["top_product"] == "Electronics" or result["top_product"] in [
        "Widget", "Gadget", "Novel", "Textbook"
    ]


def test_report_file_written(tmp_path):
    input_csv = str(tmp_path / "sales.csv")
    output_txt = str(tmp_path / "report.txt")
    _write_test_csv(input_csv, SAMPLE_DATA)

    generate_report(input_csv, output_txt, 2024, 1)

    assert os.path.exists(output_txt)
    with open(output_txt) as f:
        content = f.read()
    assert "MONTHLY SALES REPORT" in content
    assert "2024-01" in content
    assert "Electronics" in content


def test_no_data_for_month(tmp_path):
    input_csv = str(tmp_path / "sales.csv")
    output_txt = str(tmp_path / "report.txt")
    _write_test_csv(input_csv, SAMPLE_DATA)

    result = generate_report(input_csv, output_txt, 2024, 6)

    assert result["total"] == 0
    assert result["categories"] == {}
    assert result["top_product"] is None


def test_february_data(tmp_path):
    input_csv = str(tmp_path / "sales.csv")
    output_txt = str(tmp_path / "report.txt")
    _write_test_csv(input_csv, SAMPLE_DATA)

    result = generate_report(input_csv, output_txt, 2024, 2)

    assert result["total"] == 150.98
    assert result["categories"]["Electronics"] == 125.0
    assert result["categories"]["Books"] == 25.98


def test_daily_average(tmp_path):
    input_csv = str(tmp_path / "sales.csv")
    output_txt = str(tmp_path / "report.txt")
    _write_test_csv(input_csv, SAMPLE_DATA)

    result = generate_report(input_csv, output_txt, 2024, 1)

    # 3 unique days in January: 5th, 12th, 20th
    expected_avg = round(416.95 / 3, 2)
    assert result["daily_average"] == expected_avg
