import csv
import sys

def create_hierarchy(paths):
    hierarchy = {}
    top_node = None
    for path in paths:
        nodes = path.strip().split('.')
        if top_node is None:
            top_node = nodes[0]
        parent = None
        for node in nodes:
            if parent:
                hierarchy[node] = parent
            parent = node
    if top_node:
        hierarchy[top_node] = None
    return hierarchy

def write_to_csv(hierarchy, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['NODE', 'PARENT']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for node, parent in hierarchy.items():
            writer.writerow({'NODE': node, 'PARENT': parent})

# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <input_file>")
    sys.exit(1)

input_file = "./uploads/" + sys.argv[1]
# print(f"CSV Conversion Input Filename: {input_file}")
# print()

# Read paths from file
with open(input_file, 'r') as file:
    paths = file.readlines()

# Derive output file name
output_file = "./downloads/" + sys.argv[1] + '.csv'
# print(f"CSV File written to : {output_file}")
# print()
hierarchy = create_hierarchy(paths)
write_to_csv(hierarchy, output_file)

# print(f"Generated file: {output_file}")
# print()
