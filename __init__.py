"""Faraday Control Center Alexa Skill"""
from flask import Flask
from flask_ask import Ask, statement, question
from faradayapi import get_workspaces, get_users, get_activities, get_vulns, get_vulns_count
import hackernewsapi
import netsecapi

APP = Flask(__name__)
ASK = Ask(APP, "/control_center")

@APP.route('/')
def homepage():
    """Default skill funcion"""
    return "Faraday Control Center Alexa Skill"

@ASK.launch
def start_skill():
    """Welcome skill"""
    welcome_message = 'Faraday Control Center is online'
    return question(welcome_message)

@ASK.intent("NoIntent")
def no_intent():
    """Abort skill"""
    bye_text = 'Faraday Control Center Shutting Down'
    return statement(bye_text)

@ASK.intent("AbortIntent")
def default():
    """Command not found"""
    msg = "Faraday command not found, please try with help"
    msg += ", say 'abort' to stop Faraday Control Center"
    return question(msg)

@ASK.intent("AMAZON.HelpIntent")
def helpintent():
    """List of avaiable commands"""
    msg = "Available commands:"
    msg += 'list worskpaces: show your current workspaces.'
    msg += 'list users: show your current users.'
    msg += 'status workspacename: show you a overview of the workspace.'
    msg += 'infosec or hackernews: give you lastest news of selected site'
    msg += 'hackernews: gives you lastest news of hackernews.'
    msg += 'netsec: give you lastest news of netsec.'
    msg += 'abort: to cancel the Faraday Control Center.'
    return question(msg)

@ASK.intent("ShowIntent")
def show_intent(workspace):
    """Return a overview of the workspace"""

    vulns = get_vulns(workspace)
    if not 'count' in vulns:
        bye_text = "Workspace {} not found" . format(workspace)
        return question(bye_text)

    vulns_count = get_vulns_count(workspace)
    activities = get_activities(workspace)


    msg = "{} have {} vulnerabilities." . format(workspace, vulns_count['total_count'])
    for k in vulns_count['groups']:
        msg += " {}: {} ," . format(k['count'], k['name'])

    msg += "Last vulnerabilities:"
    for i in vulns['vulnerabilities']:
        vuln = i['value']
        msg += "{}: {}. " . format(vuln['severity'], vuln['name'])

    msg += "Last activities: "
    for i in range(0, 4):
        row = activities['activities'][i]
        msg += "{} run {}, adding {} hosts," . format(row['creator'],
                                                      row['tool'],
                                                      row['hosts_count'])
        msg += "{} services and {} vulns, " . format(row['services_count'],
                                                     row['vulnerabilities_count'])
    return question(msg)

@ASK.intent("InfosecIntent")
def share_infosec():
    """Return a top 5 news of netsec & hackenews  """
    return question(share_netsec(1) + share_hackernew(1))

@ASK.intent("NetsecIntent")
def share_netsec(text):
    """Return a top 5 news of netsec """
    news = netsecapi.topstories()
    news_msg = "Last news of netsec, "
    for i in range(2, 8):
        news_msg += "Title: " + u'{0}'.format(news.entries[i].title) + ", "
    if text:
        return news_msg

    return question(news_msg)

@ASK.intent("HackernewsIntent")
def share_hackernew(text):
    """Return a top 5 news of hackernews """
    news = hackernewsapi.topstories()
    news_msg = "Last news of hackernews, "
    for i in range(0, 5):
        news_msg += "Title: " + u'{0}'.format(news.entries[i].title) + ", "
    if text:
        return news_msg

    return question(news_msg)

@ASK.intent("UsersIntent")
def share_users():
    """Return list of Faraday users """
    users = get_users()
    users_msg = "Not users found"
    if 'rows' in users:
        users_msg = "{} Users:  " . format(len(users['rows']))
        for i in users['rows']:
            users_msg += "{}, " . format(i['doc']['username'])

    return question(users_msg)

@ASK.intent("WorkspacesIntent")
def share_workspaces():
    """Return list of Faraday workspaces with a overview """
    workspaces = get_workspaces()
    workspace_msg = "{} available. " . format(len(workspaces)) + ", "
    for i in workspaces:
        workspace_msg += ("Name: {}" . format(i['name']) +
                          " with {} hosts" . format(i['stats']['hosts']) +
                          ", {} vulns" . format(i['stats']['total_vulns']) +
                          ", {} services, " . format(i['stats']['services']))
    return question(workspace_msg)

if __name__ == '__main__':
    APP.run(debug=True)
