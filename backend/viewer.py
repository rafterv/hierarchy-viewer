import subprocess
import sys

def call_hierarchy2csv(filename):
    print(f"Calling ./hierarchy2csv.py {filename}")
    subprocess.call(["python3", "./hierarchy2csv.py", filename])

def call_processor(viewer_filename, rankdir, from_col='node', to_col='parent', rev=True, display_col=None, group_col=None, value_col=None, all=False):
    command = [
        "python3",
        "./processor.py",
        "--f", viewer_filename,
        "--from", from_col,
        "--to", to_col,
        "--rankdir", rankdir,
        "--rev"
    ]
    print(f"{command}")
    print()
    subprocess.call(command)

def main():
    if len(sys.argv) < 2:
        print("Usage: python viewer.py <filename> <graphdirection>")
        sys.exit(1)

    filename = sys.argv[1]
    rankdir = sys.argv[2] if len(sys.argv) > 2 else 'LR'

    call_hierarchy2csv(filename)
    print(f"Input Filename for processing: {filename}")
    print()
    call_processor(filename, rankdir)

if __name__ == "__main__":
    main()
