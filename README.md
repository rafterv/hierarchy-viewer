Hierarchy Viewer
================
This package is designed to automate the process of converting a hierarchical dataset into a graphical representation.This builds on the original repo from cristiscu. `viewer.py` is the main script,it calls two other scripts, `hierarchy2csv.py` and `processor.py`, to generate a graph visualization based on the input data.

Requirements
================
- Python 3.x
- pandas
- graphviz

Usage
================
```bash
python viewer.py <filename> [<graphdirection>]
```

- `<filename>`: Path to the input hierarchical dataset file. The file should be in a supported format.
- `[<graphdirection>]` (optional): Direction of the graph layout. Valid options are:
  - LR (Left to Right)
  - RL (Right to Left)
  - TB (Top to Bottom)
  - BT (Bottom to Top)
  
If `<graphdirection>` is not provided, the default direction is LR (Left to Right).

## Input File Format
The input file should be a hierarchical dataset in a dot notation format. Each line represents a node in the hierarchy. The format of each line should be as follows:
```
parent_node.child_node
```
For example:
```
sys.hcs.Octan.ContosoElectronics.Bristol
sys.hcs.Octan.ContosoElectronics.Clapton
sys.hcs.Octan.ContosoElectronics.EMEA.Germany
sys.hcs.Octan.ContosoElectronics.EMEA.South Africa
```
This represents a hierarchical structure where `sys.hcs.Octan.ContosoElectronics` is the parent node of `Bristol` and `Clapton`, and `sys.hcs.Octan.ContosoElectronics.EMEA` is the parent node of `Germany` and `South Africa`.

