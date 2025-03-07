# API Fetch - PubMed Research Papers

# Project Overview

This project fetches research papers from PubMed based on a user-specified query.
It processes the retrieved data and categorizes the papers into "Pharma/Biotech" or "Other," then saves the results in a CSV file.
# Installation and Execution

Prerequisites

Ensure you have Python 3.9 or later installed.

Install Dependencies

You can install dependencies using pip or poetry:

Using pip

pip install requests pandas xmltodict

Using Poetry

poetry install

Run the Program

To fetch research papers, run:

python src/main.py "cancer treatment"

To save results to a file:

python src/main.py "cancer treatment" -f results.csv

# Tools and Libraries Used

Requests (Docs) - For making API calls to PubMed.

Pandas (Docs) - For data processing and CSV export.

xmltodict (Docs) - For parsing XML responses.

BeautifulSoup (Docs) - For HTML parsing (if needed in future enhancements).

# Additional Information

This project integrates with Poetry for dependency management. To add new dependencies, use:

poetry add package-name

