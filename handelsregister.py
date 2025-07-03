#!/usr/bin/env python3
"""
bundesAPI/handelsregister is the command-line interface for the shared register
of companies portal for the German federal states.
You can query, download, automate and much more, without using a web browser.
"""

import argparse
import mechanize
import re
import pathlib
import sys
import json
from bs4 import BeautifulSoup

# Map CLI options
schlagwortOptionen = {
    "all": 1,
    "min": 2,
    "exact": 3
}

class HandelsRegister:
    def __init__(self, args):
        self.args = args
        self.browser = mechanize.Browser()

        # enable/disable debug
        self.browser.set_debug_http(args.debug)
        self.browser.set_debug_responses(args.debug)

        self.browser.set_handle_robots(False)
        self.browser.set_handle_equiv(True)
        self.browser.set_handle_gzip(True)
        self.browser.set_handle_refresh(False)
        self.browser.set_handle_redirect(True)
        self.browser.set_handle_referer(True)

        self.browser.addheaders = [
            ("User-Agent", "Mozilla/5.0 ..."),
            ("Accept-Language", "en-GB,en;q=0.9"),
            ("Accept-Encoding", "gzip, deflate, br"),
            ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
            ("Connection", "keep-alive"),
        ]
        
        self.cachedir = pathlib.Path("cache")
        self.cachedir.mkdir(parents=True, exist_ok=True)

    def companyname2cachename(self, companyname):
        return self.cachedir / companyname

    def search_company(self):
        # Check cache
        cachename = self.companyname2cachename(self.args.schlagwoerter)
        if not self.args.force and cachename.exists():
            html = cachename.read_text(encoding="utf-8")
        else:
            self.browser.open("https://www.handelsregister.de", timeout=10)
            self.browser.follow_link(text="Advanced search")
            self.browser.select_form(name="form")
            self.browser["form:schlagwoerter"] = self.args.schlagwoerter
            self.browser["form:schlagwortOptionen"] = [str(schlagwortOptionen[self.args.schlagwortOptionen])]
            response = self.browser.submit()
            html = response.read().decode("utf-8")
            cachename.write_text(html, encoding="utf-8")
        return get_companies_in_searchresults(html)

def parse_result(tr):
    cells = [td.text.strip() for td in tr.find_all("td")]
    d = {
        "court": cells[1],
        "name": cells[2],
        "state": cells[3],
        "status": cells[4],
        "documents": cells[5],
        "history": []
    }
    # history in columns 8+
    for i in range(8, len(cells), 3):
        d["history"].append({"name": cells[i], "location": cells[i+1]})
    return d

def get_companies_in_searchresults(html):
    soup = BeautifulSoup(html, "html.parser")
    grid = soup.find("table", role="grid")
    results = []
    if grid:
        for tr in grid.find_all("tr"):
            if tr.get("data-ri") is not None:
                results.append(parse_result(tr))
    return results

def parse_args():
    parser = argparse.ArgumentParser(description="A handelsregister CLI")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-f", "--force", action="store_true")
    parser.add_argument("-s", "--schlagwoerter",
                        help="Search term",
                        required=True)
    parser.add_argument("-so", "--schlagwortOptionen",
                        choices=["all","min","exact"],
                        default="all",
                        help="all/min/exact")
    args = parser.parse_args()
    if args.debug:
        import logging
        logger = logging.getLogger("mechanize")
        logger.addHandler(logging.StreamHandler(sys.stdout))
        logger.setLevel(logging.DEBUG)
    return args

def main(cli_args=None):
    """
    Entry-point for both CLI use and Python imports.
    If cli_args is provided, it should be a list of strings, e.g. ["-s","MyCo","-so","all"].
    Returns a Python dict of results.
    """
    if cli_args is not None:
        sys.argv = [sys.argv[0]] + cli_args
    args = parse_args()
    hr = HandelsRegister(args)
    companies = hr.search_company()
    return {"search_term": args.schlagwoerter, "results": companies}

if __name__ == "__main__":
    # Run as script: print the JSON to stdout
    res = main(sys.argv[1:])
    print(json.dumps(res, ensure_ascii=False, indent=2))
