# -*- coding: utf-8 -*-
"""api_fetcher.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xWQIoVsM_ar_NQ0fQx61VdxhXZnztSrq
"""

import requests
import xmltodict
import pandas as pd
import sys
import argparse


def fetch_papers(query, max_results=10):
    """Fetches research papers from PubMed based on a search query."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    details_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    # Search for papers using the query
    search_params = {
        'db': 'pubmed',
        'term': query,
        'retmax': max_results,
        'retmode': 'xml'
    }
    search_response = requests.get(base_url, params=search_params)
    search_data = xmltodict.parse(search_response.content)

    # Extract paper IDs from search results
    ids = search_data['eSearchResult'].get('IdList', {}).get('Id', [])
    if not ids:
        print("No results found.")
        return []

    # Fetch details of the papers using their IDs
    fetch_params = {
        'db': 'pubmed',
        'id': ",".join(ids),
        'retmode': 'xml'
    }
    fetch_response = requests.get(details_url, params=fetch_params)
    fetch_data = xmltodict.parse(fetch_response.content)

    papers_data = []

    for article in fetch_data.get('PubmedArticleSet', {}).get('PubmedArticle', []):
        try:
            paper = {}
            medline_citation = article.get('MedlineCitation', {})
            article_data = medline_citation.get('Article', {})

            # Extract paper details
            paper['PubmedID'] = medline_citation.get('PMID', 'N/A')
            paper['Title'] = article_data.get('ArticleTitle', 'Unknown Title')

            # Extract publication date
            journal_info = article_data.get('Journal', {}).get('JournalIssue', {})
            pub_date = journal_info.get('PubDate', {})
            paper['Publication Date'] = pub_date.get('Year', 'Unknown')

            paper['Category'] = "Other"  # Default category

            # Extract author details and affiliations
            authors = article_data.get('AuthorList', {}).get('Author', [])
            if isinstance(authors, dict):
                authors = [authors]

            pharma_authors, pharma_companies, corresponding_email = [], [], ""
            for author in authors:
                affiliations = author.get('AffiliationInfo', [])
                if isinstance(affiliations, dict):
                    affiliations = [affiliations]

                for aff_info in affiliations:
                    aff = aff_info.get('Affiliation', '')
                    if 'pharma' in aff.lower() or 'biotech' in aff.lower():
                        pharma_authors.append(author.get('LastName', 'Unknown'))
                        pharma_companies.append(aff)
                        paper['Category'] = "Pharma/Biotech"

                if author.get('CorrespondingYN') == 'Y':
                    corresponding_email = author.get('Email', 'N/A')

            paper['Non-academic Author(s)'] = ", ".join(pharma_authors) or 'N/A'
            paper['Company Affiliation(s)'] = ", ".join(pharma_companies) or 'N/A'
            paper['Corresponding Author Email'] = corresponding_email or 'N/A'

            papers_data.append(paper)
        except KeyError:
            continue

    return papers_data


def save_to_csv(papers_data, filename):
    """Saves research papers to a CSV file with all required columns."""
    df = pd.DataFrame(papers_data, columns=[
        "PubmedID", "Title", "Publication Date",
        "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email", "Category"
    ])
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")


def print_to_console(papers_data):
    """Prints research papers to the console."""
    if not papers_data:
        print("No papers found.")
        return

    print("\nFetched Research Papers:")
    for paper in papers_data:
        print(f"PubmedID: {paper['PubmedID']}, Title: {paper['Title']}, Date: {paper['Publication Date']}, Category: {paper['Category']}")


import argparse

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")

    # Positional argument for query
    parser.add_argument("query", nargs="?", help="Search query for PubMed.")

    # Optional arguments
    parser.add_argument("-f", "--file", type=str, help="Specify filename to save results.")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information.")

    args = parser.parse_args()

    # Show help if query is missing
    if not args.query:
        parser.print_help()
        return

    print(f"Fetching papers for query: {args.query}")
    if args.debug:
        print("Debug mode enabled.")

    if args.file:
        print(f"Results will be saved to {args.file}")
    else:
        print("Results will be printed to the console.")

if __name__ == "__main__":
    main()

# Integration with Poetry
# Create pyproject.toml
"""
[tool.poetry]
name = "api_fetch"
version = "0.1.0"
description = "Fetch research papers using PubMed API."
authors = ["dadireddymeghana@gmail.com"]

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.28.1"
pandas = "^1.5.3"
xmltodict = "^0.13.0"

[tool.poetry.scripts]
get-papers-list = "src.main:main"
"""

query = "cancer treatment"

# Fetch papers from PubMed
papers_data = fetch_papers(query)

# Separate Pharma/Biotech and Other papers
pharma_papers = [paper for paper in papers_data if paper['Category'] == "Pharma/Biotech"]
other_papers = [paper for paper in papers_data if paper['Category'] == "Other"]

# Save to CSV
save_to_csv(papers_data, "output.csv")

# Printing results
print(f"Pharma/Biotech Papers: {len(pharma_papers)}")
print(f"Other Papers: {len(other_papers)}")