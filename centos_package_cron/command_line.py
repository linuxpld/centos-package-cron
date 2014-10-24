import argparse
import socket
import sys
from email_producer import EmailProducer

__VERSION__ = '1.0'

def main():
    args = parse_args()    
    repos_to_exclude_list = []
    if args.disablerepo != None:
        repos_to_exclude_list = args.disablerepo.split(',')
    repos_to_include_list = []
    if args.enablerepo != None:
        repos_to_include_list = args.enablerepo.split(',')
    producer = EmailProducer(repos_to_exclude_list, repos_to_include_list, args.skipold)
    email_content = producer.produce_email()
    if email_content != '':
        executor.run_command(['/usr/bin/mail',
                              '-s %s' % (args.email_subject),
                              '-r %s' % (args.email_from),
                              args.email_to],
                             email_content)           
                            
def parse_args():
    parser = argparse.ArgumentParser(description="Emails administrators with CentOS security updates and changelogs of non-security updates. Version %s" % __VERSION__)
    
    parser.add_argument('-e', '--email_to',
    type=str,
    required=True,
    help='Email following user with the output.'
    'Could be `centos_package_cron -e johndoe@mail.com`. '
    "Uses system's `mail` to send emails.")
    
    default_from = "CentOS Update Check on %s <noreply@centos.org>" %(socket.gethostname())
    parser.add_argument('-f', '--email_from',
    type=str,
    default=default_from,
    help='Email from this user'
    'Could be `centos_package_cron -f johndoe@mail.com`. '
    "Uses system's `mail` to send emails  Will use '%s' by default." % (default_from))
    
    default_subject= "CentOS Update Check on %s" %(socket.gethostname())
    parser.add_argument('-s', '--email_subject',
    type=str,
    default=default_subject,
    help='Email using this subject'
    'Could be `centos_package_cron -s "the test subject"`. '
    "Uses system's `mail` to send emails with this subject  Will use '%s' by default." % (default_subject)) 
    
    parser.add_argument('-dr','--disablerepo',
    type=str,
    help='List of comma separated repos to exclude when dealing with Yum')
    
    parser.add_argument('-er','--enablerepo',
    type=str,
    help='List of comma separated repos to include when dealing with Yum')
    
    parser.add_argument('-so','--skipold',
    type=bool,
    default=True,
    help='Only annoys the person with 1 email for a given advisory/package update notice.')
    
    return parser.parse_args()

if __name__ == '__main__':
    sys.exit(main())
