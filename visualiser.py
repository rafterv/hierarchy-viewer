import subprocess
import sys

def call_hierarchy2csv(filename):
    subprocess.call(["python3", "hierarchy2csv.py", filename])

def call_viewer(viewer_filename, rankdir, from_col='node', to_col='parent', rev=True, display_col=None, group_col=None, value_col=None, all=False):
    command = [
        "python3",
        "viewer.py",
        "--f", viewer_filename,
        "--from", from_col,
        "--to", to_col,
        "--rankdir", rankdir,
        "--rev"
    ]
    # for i, arg in enumerate(command):
    #     print(f"Argument {i}: {arg}")  # Print out each argument individually
    subprocess.call(command)

def main():
    if len(sys.argv) < 2:
        print("Usage: python main_script.py <filename> <graphdirection>")
        sys.exit(1)

    filename = sys.argv[1]
    viewer_filename = filename.rsplit('.', 1)[0]
    rankdir = sys.argv[2] if len(sys.argv) > 2 else 'LR'

    call_hierarchy2csv(filename)
    #print(f"Generated filename: {filename}")
    #viewer_filename = "data/voss_hierarchy"
    #print(f"Generated filename: {viewer_filename}")
    call_viewer(viewer_filename, rankdir)

if __name__ == "__main__":
    main()
