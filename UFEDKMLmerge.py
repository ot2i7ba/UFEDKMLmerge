# Copyright (c) 2024 ot2i7ba
# https://github.com/ot2i7ba/
# This code is licensed under the MIT License (see LICENSE for details).

"""
Merges several KML files exported from Cellebrite UFED into one file
"""

import os
import sys
import logging
import time
from datetime import datetime
from lxml import etree
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# Global Constants
LOG_FILE = 'UFEDKMLmerge.log'
MERGED_KML_FILE = 'Merged.kml'
LARGE_FILE_THRESHOLD = 10 * 1024 * 1024  # 10 MB

# Configure logging
def configure_logging():
    """
    Configure logging to log both to the console and a log file.
    This function ensures that all significant events are recorded for auditing.
    """
    if not os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'w') as f:
                f.write("")
            print(f"Log file created: {LOG_FILE}")
        except IOError as e:
            print(f"Failed to create log file: {e}")

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(LOG_FILE)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

    logging.info("Logging configured successfully")

# Helper functions
def clear_screen():
    """Clear the screen depending on the operating system."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_blank_line():
    """Print a blank line for better readability."""
    print("\n")

def print_header():
    """Print the header for the script."""
    print(" UFEDKMLmerge v0.0.1 by ot2i7ba ")
    print("================================")
    print_blank_line()

def list_kml_files():
    """
    List all KML files in the current directory and count placemarks in each.
    Returns:
        list: A list of tuples containing KML file names, their placemark counts, and file sizes.
    """
    kml_files = [f for f in os.listdir('.') if f.endswith('.kml')]
    if not kml_files:
        logging.info("No KML files found in the current directory.")
        print("No KML files found in the current directory.")
        sys.exit(0)

    kml_file_info = []
    for kml_file in kml_files:
        placemark_count = count_placemarks_in_file(kml_file)
        file_size_mb = os.path.getsize(kml_file) / (1024 * 1024)  # in MB
        kml_file_info.append((kml_file, placemark_count, file_size_mb))
    
    return kml_file_info

def count_placemarks_in_file(kml_file):
    """
    Count the number of placemarks in a KML file using streaming.
    Args:
        kml_file (str): The path to the KML file.
    Returns:
        int: The number of placemarks found in the file.
    """
    try:
        placemark_count = 0
        for event, elem in etree.iterparse(kml_file, events=('end',), tag='{http://www.opengis.net/kml/2.2}Placemark'):
            placemark_count += 1
            elem.clear()
        return placemark_count
    except (etree.XMLSyntaxError, Exception) as e:
        logging.error(f"Error counting placemarks in file {kml_file}: {e}")
        return 0

def get_user_selection(kml_files):
    """
    Prompt the user to select which KML files to merge.
    Returns:
        list: A list of selected KML filenames.
    """
    while True:
        print("Found KML files:")
        for idx, (file, placemark_count, file_size_mb) in enumerate(kml_files, 1):
            print(f"{idx}. {file:<30} {file_size_mb:6.2f} MB    {placemark_count} placemarks")
        print("e. Exit")
        print_blank_line()

        selected_indices = input("Enter numbers of files to merge (e.g., 1, 2, 5) or Enter to merge all: ").strip().lower()
        if selected_indices == 'e':
            print("Exiting the script. Goodbye!")
            logging.info("User chose to exit the script.")
            sys.exit(0)
        if not selected_indices:
            logging.info("No specific files selected, merging all.")
            selected_files = [file for file, _, _ in kml_files]
        else:
            try:
                selected_files = []
                for index in selected_indices.split(','):
                    index = index.strip()
                    if index.isdigit() and 1 <= int(index) <= len(kml_files):
                        selected_files.append(kml_files[int(index) - 1][0])
                if not selected_files:
                    raise ValueError("No valid selection made.")
            except (IndexError, ValueError) as e:
                logging.error(f"Invalid selection: {e}")
                print("Invalid selection, please try again or enter 'e' to exit.")
                continue

        # Check if enough files are selected for merging
        if len(selected_files) < 2:
            print("At least two KML files are required to perform a merge. Please select more files.")
            logging.info("Not enough files selected for merging.")
            display_countdown(3)  # Show a 3-second countdown
            clear_screen()
            print_header()
            kml_files = list_kml_files()  # Re-list KML files
        else:
            logging.info(f"{len(selected_files)} files selected for merging.")
            return selected_files

def parse_kml_file(kml_file):
    """
    Parse a KML file and return its root element.
    Uses streaming to handle large files efficiently.
    Args:
        kml_file (str): The path to the KML file.
    Returns:
        root (Element): The root element of the parsed KML file.
    """
    try:
        if os.path.getsize(kml_file) > LARGE_FILE_THRESHOLD:
            logging.info(f"Processing large file {kml_file} with streaming...")
            context = etree.iterparse(kml_file, events=('end',), tag='{http://www.opengis.net/kml/2.2}Placemark')
            root = etree.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
            document = etree.SubElement(root, 'Document')
            for event, elem in context:
                document.append(elem)
                elem.clear()
            return root
        else:
            logging.info(f"Processing file {kml_file} normally...")
            tree = etree.parse(kml_file)
            return tree.getroot()
    except (etree.XMLSyntaxError, Exception) as e:
        logging.error(f"Error parsing file {kml_file}: {e}")
        return None

def merge_kml_files(selected_files):
    """
    Merge the selected KML files into a single KML file.
    Args:
        selected_files (list): List of KML files selected for merging.
    """
    merged_root = etree.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
    document = etree.SubElement(merged_root, 'Document')
    placemark_count = 0  # Counter for the number of Placemarks

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(parse_kml_file, kml_file): kml_file for kml_file in selected_files}
        for future in as_completed(futures):
            kml_file = futures[future]
            try:
                root = future.result()
                if root is not None:
                    placemarks = root.findall('.//{http://www.opengis.net/kml/2.2}Placemark')
                    document.extend(placemarks)
                    placemark_count += len(placemarks)
                    logging.info(f"File {kml_file} successfully merged with {len(placemarks)} placemarks.")
                else:
                    logging.error(f"Failed to merge file {kml_file}.")
            except Exception as e:
                logging.error(f"Exception occurred while merging file {kml_file}: {e}")

    if len(document) > 0:
        output_file = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_Merged.kml"
        with open(output_file, 'wb') as f:
            f.write(etree.tostring(merged_root, pretty_print=True))
        logging.info(f"Merged KML file saved as {output_file}")
        print(f"Merged KML file saved as: {output_file}")
        print_blank_line()
        
        # Save statistics and analysis to Excel
        save_analysis_to_excel(selected_files, placemark_count)
        print(f"{len(selected_files)} files have been successfully merged into {output_file}.")
    else:
        logging.error("No valid KML files were merged.")
        print("No valid KML files were merged.")
        print_blank_line()

def save_analysis_to_excel(selected_files, placemark_count):
    """
    Save analysis results to an Excel file with additional statistics.
    Args:
        selected_files (list): List of selected KML files.
        placemark_count (int): Total number of placemarks merged.
    """
    analysis_file = f"Analysis_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    data = {
        'File Name': selected_files,
        'Placemarks Count': [placemark_count] * len(selected_files),
        'File Size (MB)': [os.path.getsize(f) / (1024 * 1024) for f in selected_files]  # Convert to MB
    }
    df = pd.DataFrame(data)
    with pd.ExcelWriter(analysis_file) as writer:
        df.to_excel(writer, sheet_name='Summary', index=False)
        # Additional statistics can be added here, like specific tag counts
    logging.info(f"Analysis saved as {analysis_file}")
    print(f"Analysis saved as {analysis_file}")

def display_countdown(seconds):
    """
    Display a countdown timer in the console.
    Args:
        seconds (int): The number of seconds for the countdown.
    """
    print_blank_line()
    for remaining in range(seconds, 0, -1):
        print(f"\rReturning to main menu in {remaining} seconds...", end="")
        time.sleep(1)
    print("\rReturning to main menu...                     ")

def main():
    """Main function to execute the KML merging script."""
    while True:
        configure_logging()
        clear_screen()
        print_header()

        kml_files = list_kml_files()
        selected_files = get_user_selection(kml_files)
        merge_kml_files(selected_files)

        # Visualize a 3-second countdown before clearing the screen
        display_countdown(3)
        clear_screen()

if __name__ == "__main__":
    main()
