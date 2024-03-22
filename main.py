from requests import Session
from pprint import pprint
import io,json
import sys
from sys import version_info
import argparse
import fnmatch as fnm

session = Session()
pyver = '.'.join([str(i) for i in version_info])

pypi = "https://pypi.org/pypi"
json_url = lambda p: f"{pypi}/{p}/json"
def search(query: str):
    import xmlrpc.client as xmlrpclib
    import fnmatch as fnm
  
    
    client = xmlrpclib.ServerProxy(pypi)
# get a list of package names
    pkglist = client.list_packages()
    results =list()
    results = fnm.filter(pkglist,f"*{query}*")
    
    if len(results) == 1:
        return get_pkg_data(session, results[0])
    
    return results

        



def get_pkg_data(S: Session,pkg: str) ->object:
    S.headers['Accept'] = "application/json"
    S.headers['User-Agent'] = f"{pyver} pypi search utility by infernox64@gmail.com"
    url = json_url(pkg)
    res = S.get(url)
    return res.json()

def main():
    ap = argparse.ArgumentParser('pypi-search', description='a tool for querying the python package index database API')
    ap.add_argument("query", "-q", type=str)
    subparsers = ap.add_subparsers(dest='subcommands',required=True)
    search_cmd = subparsers.add_parser('search')
    