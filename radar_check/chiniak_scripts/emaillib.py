import subprocess

def email_notice(subject, body, target, cc, sendcc = False):
    bodyecho = subprocess.Popen(['echo', body], stdout=subprocess.PIPE)

    if sendcc: 
        mail = subprocess.Popen(["mail", "-s", subject, '-c', '"'+cc+'"', '"'+target+'"', ], stdin = bodyecho.stdout, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    else:
        mail = subprocess.Popen(["mail", "-s", subject,  '"'+target+'"', ], stdin = bodyecho.stdout, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    bodyecho.stdout.close()
    out, error = mail.communicate()
    print out


if '__name__' == '__main__':
        email_notice('test', 'this is a test', 'jtklein@alaska.edu', 'jtklein@alaska.edu')
