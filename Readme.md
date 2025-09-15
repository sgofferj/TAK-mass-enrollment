# TAK-mass-enrollment

Create TAK server users and a PDF with ATAK Quick Connect QR codes from a CSV file.

&copy;2025 Stefan Gofferje

License: GPL V3

**IMPORTANT: Please read the instructions completely before use!**

## Introduction

I wrote this script to assist with the introduction of the TAK ecosystem during a reserve exercise
of the Finnish Defense Forces. It should be useful in any use case where a lot of users need to be
added to a _temporary_ TAK server. In theory, it can also be used to mass-add users to a permanent
TAK server but I personally wouldn't do it because user management can get very messy very quickly
then. For permanent TAK servers, you should probably look into using LDAP backends.

The script only works with the official TAK server from tak.gov.

## Functions

The script will read a list uf users and groups from a CSV file. It first checks if the user certificate
has admin rights on the server. If not, the script will exit with an error message. If the user cert has
admin rights, the script will go through the users in the CSV file.

It will then check if a user already exists on the server. If so, it will skip user creation.
**THIS IS FOR SECURITY REASONS!** We don't want the CSV data messing with existing users, say,
changing the password of a server admin user... If all is good, a secure randomly generated password
is generated and the user is created on the server.

Groups are created by TAK server automatically if they don't exist, so no need to check there.

In addition to creating the users, we create a PDF file which contains slips with the user's real name,
username, QR codes for the ATAK Quick Connect function and some usage instructions. Those slips are ment
to be cut and handed to the user.

## Limitations

### No support for Windows

I don't usually use Windows and thus don't have experience with Python on Windows.

### No support for Apple

I don't own any Apple devices and thus don't have experience with Python on Apple. Consequently,
I also don't have iTAK and can't test anything for that.

### Only certificate authentication (for the moment)

I haven't figured out yet how the password authentication flow for the TAK server API works. If you know how,
please open an issue and explain it. I'll add it later.

## Installation

- Make sure, you have at least Python 3.12, python-pip and python-venv installed
- Clone or download the repository
- Go to the repository and check main.py. On the top of the file, you'll find a line saying `import lang_xx as lang`.
  Change this to whatever language you want to use, e.g. `import lang_en as lang`. The language file needs to exist,
  of course.
- Next open a command line and go to the installation directory. Execute
  ```bash
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

## Usage

### Server preparation

Two things are important for the script and the enrollment to work properly:

1. The TAK server certificate needs to have either the domain name or the IP address (whatever you plan to use
   for connection) in the common name. You do this by using `makeCert.sh server <common name>` and then configuring
   the resulting .jks-file as the server certificate. For more information, please consult the TAK server
   documentation.
2. The EUDs (Android devices) need to trust the server certificate. If you use a self-signed certificate (which
   is usually the case), you need to get the TAK-CA-xxx.pem file from tak/certs/files, ideally remove the password
   with `openssl rsa -in TAK-CA-xxx.pem -out CAcert.pem` and make it available to the EUDs for download. The EUD
   users need to download the certificate and add it to the EUDs Android truststore by going to Android settings
   -> Security -> Encryption and Credentials -> Install a certificate -> CA certificate.

### The CSV format

The CSV file has the following format:

`Real name;username;own groups;IN groups;OUT groups`

Please note the semicolons to separate the fields!

The first line of the CSV file is skipped, so you can leave a header line to remember the field meanings.

- `Real name` is the real name of the user. That field is only used when creating the PDF file.
- `username` is the username created on the TAK server.
- `groups` are the user's primary groups that they can see and be seen by.
- `IN groups` is a list of groups that the user should be visible to but without the user being able
  to see them. This could be e.g. exercise leaders, judges, etc.
- `OUT groups` is a list of groups that the user should be able to see in addition to their own group but
  without sending any data to them. This could be e.g. feeders.

Every user **should** have at least one own group (otherwise, TAK server puts them in the **ANON** group automatically),
but the additional groups are optional. Multiple groups in a group field should be separated by **commas** while the
fields are separated by **semicolons**.

Every row also **must** have 5 columns. If a column is empty, add semicolons (max 4 per row, see examples).

#### Examples

`Sample, Susan;susans;intelligence,humint;supervisors;incidents`

Susan is a member of the groups intelligence and humint, she gets data from the group incidents and she can be seen
by the supervisors group but she cannot see them.

```
Judge, James;jamesj;judges;;
Marine, Marcus;marcusm;blue_team;judges;
```

James is a member of a judges group for an exercise. Marcus is a member of the blue_team group and additionally can
be seen by the judges group but cannot see them.

### Parameters

The script takes the following parameters, all of which are mandatory

- -s / --Server <server address> - the address of the server, either IP address or domain name, without any protocol
- -c / --Cert <certificate file> - the path to the admin user certifcate in PEM format
- -k / --Key <key file> - the path to the admin user certificate key file in PEM format
- -f / --File <CSV file> - the path to the CSV file
- --delete - deletes all users listed in the CSV from the server. Useful for cleanup, e.g. after an exercise

### venv

Make sure, you activate the Python virtual environment before calling the script

```bash
source venv/bin/activate
```

### Example call

`python main.py -s takserver.domain.tld -c cert.pem -k key.pem -f users.csv`

## Support

If you need support installing or configuring the TAK server, please go to the ATAK subreddit
or join the TAK Discord.

If you have a question about the script or find a bug, please open an issue. Suggestions for improvements
or pull requests are also welcome 😀.
