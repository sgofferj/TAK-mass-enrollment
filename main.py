import lang_en as lang
import os
import getopt, sys
import takserver as tak
import functions as func
from urllib.parse import quote
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section
import qrcode

def getChunks(data, n):
    for i in range(0, len(data), n):
        yield data[i:i+n]

def main(server,api,cert,csvfile):
    pdf = MarkdownPdf(toc_level=3, optimize=True)
    data = func.readFile(csvfile)
    
    for chunks in getChunks(data,5):
        text=""
        for row in chunks:
            name = row[0]
            user = row[1]
            groups = row[2].split(",")
            groupsIn = row[3].split(",")
            groupsOut = row[4].split(",")
            if groupsIn == ['']:
                groupsIn = []
            if groupsOut == ['']:
                groupsOut = []
            password = func.createPW()
            if tak.userExists(api,cert,user):
                print(f"User '{user}' exists, skipping")
            else:
                print(f"Creating user '{user}' for '{name}'")
                text +="<div class='creds'>\n"
                text += f"<div class='secret'>{lang.txt_credentials} - {lang.txt_secret}</div>\n"
                text += "<table>\n"
                print(groupsIn,groupsOut)
                result = tak.createUser(api, cert, user, password, groups, groupsIn, groupsOut)
                if result.status_code == 200:
                    print(f"User '{user}' created")
                else:
                    print(f"Error creating user '{user}': {result.status_code}")
                url = func.createURL(server,user,quote(password))
                img = qrcode.make(url)
                img = img.resize((130,130))
                img.save(f"{user}.png")
                text += "<tr>"
                text += f"<td><h1>{name} ({user})</h1>"
                for group in groups:
                    text += f"<span class='group'>{group}</span> "
                text +"</td>"
                text += f"<td class='instructions'><strong>{lang.txt_instructions_header}</strong><br>\n{lang.txt_instructions_body}</td>"
                text += f"<td><div><img src='{user}.png' /></div></td>"
                text += "</tr>\n"
                text += "</table>\n"
                text += "</div>\n"
        pdf.add_section(Section(text), user_css = "h1 {font-size: 1.5em;} table {border-bottom: 1px solid black;} tr {width: 100%} td {padding: 0.5em;} .secret {color: red; font-size: 1em; font-weight: bold;} .creds {padding: 1em;} .instructions {font-size: 0.75em;} .group {font-size: 0.5em;}")
    pdf.save("enrollment-slips.pdf")

def configParser():
    argumentList = sys.argv[1:]
    options = "hf:s:c:k:"
    long_options = ["Help","File=","Server=", "Cert=", "Key="]
    server = None
    cert = None
    key = None
    csvfile = None
    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-h", "--Help"):
                print ("Displaying Help")
                
            elif currentArgument in ("-s", "--Server"):
                server = (currentValue)
                
            elif currentArgument in ("-c", "--Cert"):
                cert = (currentValue)

            elif currentArgument in ("-k", "--Key"):
                key = (currentValue)

            elif currentArgument in ("-f", "--File"):
                csvfile = (currentValue)

    except getopt.error as err:
        print (str(err))

    crt = (cert, key);
    return server, crt, csvfile


server, cert, csvfile = configParser()

if server != "" and len(cert) > 0 and csvfile != None:
    api = f"https://{server}:8443"
    if os.path.exists(csvfile):
        print ("CSV file found")
        if tak.isAdmin(api,cert):
            print("User is admin")
            main(server,api,cert,csvfile)
        else:
            print("User is not admin")
    else:
        print("CSV file not found")
else:
    print("Some argument is missing")