import argparse
import sys
from contextlib import ExitStack
from pathlib import Path

from report_converter import ReportExtractor, SectionMeta, TradeCols


def _list_csv_files(directories: list[str]) -> list[Path]:
    csv_files: list[Path] = []
    for directory in directories:
        root = Path(directory)
        if not root.exists() or not root.is_dir():
            continue
        for path in sorted(root.glob("*.csv")):
            if path.stat().st_size == 0:
                continue
            csv_files.append(path)
    return csv_files


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract transactions from one or more directories containing IBKR CSV reports."
    )
    parser.add_argument(
        "directories",
        nargs="+",
        help="One or more directories to scan for CSV files.",
    )
    parser.add_argument(
        "-s",
        "--save-csv",
        action="store_true",
        help="Save extracted transactions to report.csv.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv if argv is not None else sys.argv[1:])

    csv_files = _list_csv_files(args.directories)
    if not csv_files:
        print("No CSV files found in provided directories.")
        return

    extractor = ReportExtractor(sections=[SectionMeta(section_name="TRNT", columns=TradeCols)])

    with ExitStack() as stack:
        handles = [stack.enter_context(path.open("r", newline="")) for path in csv_files]
        report = extractor.extract_files(handles)

    print(f"Processed files: {len(csv_files)}")
    print(f"Extracted transactions: {len(report)}")

    if args.save_csv:
        output_path = Path("report.csv")
        report.to_csv(output_path, index=False)
        print(f"Saved extracted report to: {output_path.resolve()}")

    print(report)


if __name__ == "__main__":
    main()
