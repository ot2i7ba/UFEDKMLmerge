# UFEDKMLmerge
UFEDKMLmerge is a Python script designed to merge multiple KML files exported from Cellebrite UFED [^1] into a single KML file. This tool streamlines the merging process, making it easier to handle large sets of KML files efficiently. The script includes logging, error handling, and options for selecting which KML files to merge. This script has been tailored to meet my professional needs, helping me streamline my workflow. By sharing this script, I hope it can be useful for others working with similar data sets. UFEDKMLmerge serves as an excellent complement to [UFEDMapper](https://github.com/ot2i7ba/UFEDMapper).

> [!NOTE]
> This script is specifically used to work with KML files exported from Cellebrite UFED. I have not tested it with other KML files, and therefore cannot guarantee its compatibility or performance with KML files from other sources.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
   - [Usage](#usage)
   - [PyInstaller](#pyinstaller)
   - [Releases](#releases)
- [Example](#example)
   - [Screenshots](#screenshots)
- [Changes](#changes)
- [License](#license)

# Features
- Logging: Logs activities both to a file and the console.
- Parse and merge multiple KML files into a single output file.
- Count and display the number of placemarks in each KML file.
- User-friendly interface for selecting files to merge.
- Enhanced user interaction and error handling.
- Save analysis results to an Excel file.

# Requirements
- Python 3.6 or higher
   - The following Python packages:
   - lxml>=4.6.3,<5.0.0
   - pandas>=1.3.0,<1.4.0
   - openpyxl>=3.0.7,<4.0.0

# Installation
1. **Clone the repository**
   ```sh
   git clone https://github.com/ot2i7ba/UFEDKMLmerge.git
   cd UFEDKMLmerge
   ```

2. **Install the required dependencies**
   ```sh
   pip install -r requirements.txt
   ```

# Usage
1. Place your KML files in the same directory as the script.
2. Run the script
   ```sh
   python UFEDKMLmerge.py
   ```
3. Follow the prompts to select which KML files to merge.

## Follow the Prompts
**KML File Selection**
The script lists all KML files in the directory and presents a numbered list for selection.

**Confirmation**
The script will prompt for confirmation before merging the selected files.

**Output File**
The merged KML file is saved with a timestamp in its name.

# PyInstaller
To compile the UFEDKMLmerge script into a standalone executable, you can use PyInstaller. Follow the steps below:

1. Install PyInstaller (if not already installed):
   ```bash
   pip install pyinstaller
   ```

2. Compile the script using the following command:
   ```bash
   pyinstaller --onefile --name UFEDKMLmerge --icon=ufedkmlmerge.ico UFEDKMLmerge.py
   ```

- `--onefile`: Create a single executable file.
- `--name UFEDKMLmerge`: Name the executable UFEDMapper.
- `--icon=ufedkmlmerge.ico`: Use ufedkmlmerge.ico as the icon for the executable.

**Running the executable**: After compilation, you can run the executable found in the dist directory.

## Releases
A compiled and 7zip-packed version of UFEDKMLmerge for Windows is available as a release. You can download it from the **[Releases](https://github.com/ot2i7ba/UFEDKMLmerge/releases)** section on GitHub. This version includes all necessary dependencies and can be run without requiring Python to be installed on your system.

> [!IMPORTANT]
> Please ensure the KML files are properly formatted and free of errors before using them with UFEDKMLmerge. Improperly formatted KML files can lead to unexpected behavior or errors during the merging process.

# Example

## The script lists available KML files and prompts for selection
```
Found KML files:
1. Example.kml                 5.34 MB    12345 placemarks
2. Locations.kml               9.84 MB    24998 placemarks
e. Exit

Enter numbers of files to merge (e.g., 1, 2) or Enter to merge all:
```

## After selecting files, the script merges them and saves the result
```
Enter a prefix for the output files (optional):
```

## Optionally filter data by date range:
```
Merging selected KML files...
Merged KML file saved as: 20240823_123456_Merged.kml
```

# Logging
The log file UFEDKMLmerge.log will be created in the same directory as the script. This log file records all actions taken by the script, including file selections and errors.

# Changes
## Initial Release
- Basic functionality to list, select, and merge KML files.
- Logging to both console and log file.
- Ability to save analysis results to an Excel file.

___

# License
This project is licensed under the **[MIT license](https://github.com/ot2i7ba/UFEDKMLmerge/blob/main/LICENSE)**, providing users with flexibility and freedom to use and modify the software according to their needs.

# Contributing
Contributions are welcome! Please fork the repository and submit a pull request for review.

# Disclaimer
This project is provided without warranties. Users are advised to review the accompanying license for more information on the terms of use and limitations of liability.

# Conclusion
This script has been tailored to fit my specific professional needs, and while it may seem like a small tool, it has a significant impact on my workflow. UFEDKMLmerge simplifies the process of merging multiple KML files into a single file, making it a useful tool for professionals who need to manage large datasets extracted from Cellebrite UFED. By automating this process, it saves time and reduces the likelihood of errors during manual file handling. I hope this tool proves to be as beneficial for others as it has been for me. Greetings to my dear colleagues [^2] who avoid scripts like the plague and think that consoles and Bash are some sort of dark magic – the [compiled](https://github.com/ot2i7ba/UFEDKMLmerge/releases) version will spare you the console kung-fu and hopefully be a helpful tool for you as well. 😉

[^1]: [Cellebrite UFED](https://cellebrite.com/) (Universal Forensic Extraction Device) is a forensic tool to extract and analyze data from mobile devices.
[^2]: Greetings to PPHA-IuK.
