"""Faraday API connector"""
import configparser
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests import Session
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable SSL warnings

CONFIG = configparser.ConfigParser()
CONFIG.read("etc/config.txt")
URL = CONFIG.get("faradayConfig", "url")
USER = CONFIG.get("faradayConfig", "user")
PASSWORD = CONFIG.get("faradayConfig", "password")

def get_workspaces():
    """Return array of workspaces"""
    cluster = get_api_data('{}/_api/v2/ws/'.format(URL))
    return cluster

def get_users():
    """Return array of users"""
    cluster = get_api_data('{}/_api/v2/users/'.format(URL))
    return cluster

def get_vulns_count(workspace):
    """Return count of vulns group by severity"""
    cluster = get_api_data('{}/_api/v2/ws/{}/vulns/count/?group_by=severity'.format(URL, workspace))
    return cluster

def get_vulns(workspace):
    """Return array last 5 vulns"""
    options = "?page=1&page_size=5&sort=date&sort_dir=desc"
    cluster = get_api_data('{}/_api/v2/ws/{}/vulns/{}'.format(URL, workspace, options))
    return cluster

def get_activities(workspace):
    """Return array of activities"""
    cluster = get_api_data('{}/_api/v2/ws/{}/activities/'.format(URL, workspace))
    return cluster

def get_api_data(req_url):
    """Do authentication and query to the API"""
    session = Session()
    try:
        resp = session.post('{}/_api/login'.format(URL), json={'email': USER, 'password': PASSWORD})
    except requests.exceptions.RequestException as error:
        print 'Error!: API {}'.format(error)
        return []

    if resp.status_code != 200:
        print 'Error! API responded with: {}'.format(resp.status_code)
        return []

    print 'Requesting Page: {}'.format(req_url)
    try:
        resp = session.get(req_url)
    except requests.exceptions.RequestException as error:
        print 'Error!: API {}'.format(error)
        return []
    if resp.status_code != 200:
        print 'Error! API responded with: {}'.format(resp.status_code)
        return []
    return resp.json()
