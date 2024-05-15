# /backend/viewer.py
import subprocess
import sys
import processor
import pandas as pd
import json
import logging

# Configure logging
log_file_path = '/var/log/viewer.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def call_hierarchy2csv(filename):
    logging.info(f"Calling hierarchy2csv.py {filename}")
    subprocess.call(["python3", "./hierarchy2csv.py", filename])

def call_processor(viewer_filename, rankdir, from_col='node', to_col='parent', rev=True, display_col=None, group_col=None, value_col=None, all=False):
    df = pd.read_csv(f"../downloads/{viewer_filename}.csv").convert_dtypes()
    cols = list(map(str.upper, df.columns.values.tolist()))
    df = df.reset_index()
    viewer_filename = "../downloads/" + viewer_filename

    # Validate column names
    fromCol = from_col.upper()
    if fromCol not in cols:
        raise ValueError("'from' column not found!")
    
    toCol = to_col.upper()
    if toCol not in cols:
        raise ValueError("'to' column not found!")
    
    displayCol = None
    if display_col is not None:
        displayCol = display_col.upper()
        if displayCol not in cols:
            raise ValueError("'display' column not found!")
    
    groupCol = None
    if group_col is not None:
        groupCol = group_col.upper()
        if groupCol not in cols:
            raise ValueError("'group' column not found!")

    valueCol = None
    if value_col is not None:
        valueCol = value_col.upper()
        if valueCol not in cols:
            raise ValueError("'value' column not found!")
    
    png_download, magjac_download = processor.makeGraph(df, cols, fromCol, toCol, displayCol, groupCol, valueCol, rev, all, viewer_filename, rankdir)
    json_download, html_download = processor.makeTree(df, fromCol, toCol, displayCol, valueCol, viewer_filename)
    #This print statement is required for server.py to get the download links....don't delete it again
    print(json.dumps({"png_download": png_download, "magjac_download": magjac_download, "json_download": json_download, "html_download":html_download }))
    ##################################################################################################
    logging.info("Viewer processing complete")
    logging.info(f"Generated PNG download link: {png_download}")
    logging.info(f"Generated MAGJAC download link: {magjac_download}")
    logging.info(f"Generated JSON download link: {json_download}")
    logging.info(f"Generated HTML download link: {html_download}")
    return json.dumps({"png_download": png_download, "magjac_download": magjac_download, "json_download": json_download, "html_download":html_download }) 

def main():
    if len(sys.argv) < 2:
        logging.error("Filename argument missing")
        sys.exit(1)

    filename = sys.argv[1]
    rankdir = sys.argv[2] if len(sys.argv) > 2 else 'LR'

    call_hierarchy2csv(filename)
    logging.info(f"Input Filename for processing: {filename}")
    call_processor(filename, rankdir)

if __name__ == "__main__":
    main()
