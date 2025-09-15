import requests as req

req.packages.urllib3.disable_warnings()


def listGroups(server, cert):
    uri = "/user-management/api/list-groupnames"
    url = server + uri
    r = req.get(url, cert=cert, verify=False)
    return r.json()


def groupExists(server, cert, group):
    r = listGroups(server, cert)
    g = next((item for item in r if item["groupname"] == group), None)
    if g:
        return True
    else:
        return False


def listUsers(server, cert):
    uri = "/user-management/api/list-users"
    url = server + uri
    r = req.get(url, cert=cert, verify=False)
    return r.json()


def userExists(server, cert, user):
    r = listUsers(server, cert)
    g = next((item for item in r if item["username"] == user), None)
    if g:
        return True
    else:
        return False


def createUser(
    server,
    cert,
    username,
    password,
    grouplistBoth=None,
    grouplistIn=None,
    grouplistOut=None,
):
    uri = "/user-management/api/new-user"
    url = server + uri
    headers = {"Content-Type": "application/json"}
    data = {"username": username, "password": password}
    if grouplistIn != None:
        data.update({"groupListIN": grouplistIn})
    if grouplistOut != None:
        data.update({"groupListOUT": grouplistOut})
    if grouplistBoth != None:
        data.update({"groupList": grouplistBoth})
    r = req.post(url, headers=headers, json=data, cert=cert, verify=False)
    return r


def deleteUser(server, cert, username):
    uri = f"/user-management/api/delete-user/{username}"
    url = server + uri
    headers = {"Content-Type": "application/json"}
    r = req.delete(url, headers=headers, cert=cert, verify=False)
    print(r.text)
    return r


def isAdmin(server, cert):
    uri = "/Marti/api/util/isAdmin"
    url = server + uri
    r = req.get(url, cert=cert, verify=False)
    if r.text == "true":
        return True
    else:
        return False
