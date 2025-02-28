import os
import datetime
from pathlib import Path

def display_file_attributes(filepath):
    file = Path(filepath)
    
    if not file.exists():
        print(f"File '{filepath}' does not exist.")
        return

    stats = file.stat()
    
    # st_birthtime may not be available on all systems, fallback to st_ctime
    try:
        creation_time = datetime.datetime.fromtimestamp(stats.st_birthtime)
    except AttributeError:
        creation_time = datetime.datetime.fromtimestamp(stats.st_ctime)
    
    size = stats.st_size

    print(f"---------------------------------")
    print(f"File: {filepath}")
    print(f"Size: {size} bytes")
    print(f"Creation Time: {creation_time}")
    # If running on Windows, you might have st_file_attributes.
    print(f"File Attributes: {getattr(stats, 'st_file_attributes', 'N/A')}")
    print(f"---------------------------------")


