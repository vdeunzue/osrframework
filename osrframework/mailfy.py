#!/usr/bin/env python
# -*- coding: cp1252 -*-
#
##################################################################################
#
#    Copyright 2015 Félix Brezo and Yaiza Rubio (i3visio, contacto@i3visio.com)
#
#    This program is part of OSRFramework. You can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##################################################################################

''' 
mailfy.py Copyright (C) F. Brezo and Y. Rubio (i3visio) 2015
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions.  For additional info, visit to <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''
__author__ = "Felix Brezo, Yaiza Rubio "
__copyright__ = "Copyright 2015, i3visio"
__credits__ = ["Felix Brezo", "Yaiza Rubio"]
__license__ = "GPLv3+"
__version__ = "v1.0.0"
__maintainer__ = "Felix Brezo, Yaiza Rubio"
__email__ = "contacto@i3visio.com"


import argparse
import json
import os

import osrframework.utils.platform_selection as platform_selection
import osrframework.utils.general as general
# From emailahoy code
import emailahoy

# For the manual checkout
#import DNS, smtplib, socket

# For the timeout function
#from osrframework.utils.timeout import timeout

def getMoreInfo(e):
    '''
        Method that calls different third party API.
        
        :param e:   Email to verify.
        
        :result:    
    '''
    # Grabbing the email
    email = {}
    email["type"] = "i3visio.email"
    email["value"] = e
    email["attributes"] = []
    
    # Grabbing the alias
    alias = {}
    alias["type"] = "i3visio.alias"
    alias["value"] = e.split("@")[0]
    alias["attributes"] = []

    # Grabbing the domain
    domain= {}
    domain["type"] = "i3visio.domain"
    domain["value"] = e.split("@")[1]
    domain["attributes"] = []
    
    return email, alias, domain

# TO-DO:
# Needs verification and further work.
"""@timeout(5)
def manualEmailCheck(mail):
    '''
        Manually checking whether a mail is being sent.
        
        :param mail:    Email to check.
        
        :result:
    '''
    DNS.DiscoverNameServers()
    #print "checking %s..."%(mail)
    hostname = mail[mail.find('@')+1:]
    mx_hosts = DNS.mxlookup(hostname)
    failed_mx = True
    for mx in mx_hosts:
            smtp = smtplib.SMTP()
            try:
                    smtp.connect(mx[1])
                    # print "Stage 1 (MX lookup & connect) successful."
                    failed_mx = False
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((mx[1], 25))
                    s.recv(1024)
                    s.send("HELO %s\n"%(mx[1]))
                    s.recv(1024)
                    s.send("MAIL FROM:< test@test.com>\n")
                    s.recv(1024)
                    s.send("RCPT TO:<%s>\n"%(mail))
                    result = s.recv(1024)
                    #print result
                    if result.find('Recipient address rejected') > 0:
                            #print "Failed at stage 2 (recipient does not exist)"
                            pass
                    else:
                            #print "Adress valid."
                            failed_mx = False
                    s.send("QUIT\n")
                    break
            except smtplib.SMTPConnectError:
                    continue
    if failed_mx:
            #print "Failed at stage 1 (MX lookup & connect)."
            pass
    #print ""
    if not failed_mx:
            return True
    return False
"""

def weCanCheckTheseDomains(email):
    '''
    '''
    notWorking = ["@yahoo.", "@ymail", "@gmx.", "@inbox.", "@mail.ru", "@gandhi.net"]
    for n in notWorking:
        if n in email:
            return False
    emailDomains = ["gmail.com", "hushmail.com"]
    safe = False
    for e in emailDomains:
        if e in email:
            safe =  True
            break
    if not safe:
        print "WARNING: the domain of '" + email + "' will not be safely verified."
    return True

def performSearch(emails=[]):
    ''' 
        Method to perform the mail verification process.
        
        :param emails: List of emails.
        
        :return:
    '''   
    results = []

    for e in emails:
        if weCanCheckTheseDomains(e):
            if '_' not in e and "-" not in e:
                if emailahoy.verify_email_address(e):
                    email, alias, domain = getMoreInfo(e)                
                    aux = {}
                    aux["type"] = "i3visio.profile"
                    aux["value"] =  domain["value"]+ " - " +alias["value"]
                    aux["attributes"]= []                    
                    aux["attributes"].append(email)
                    aux["attributes"].append(alias)                    
                    aux["attributes"].append(domain)                    
                    results.append(aux)
                else:
                    pass
            else:
                pass
                """ try:
                    if not "gmail.com" in e and manualEmailCheck(e):
                        aux = {}
                        aux["type"] = "i3visio.email"
                        aux["value"] = e
                        aux["attributes"] = getMoreInfo(e)

                        results.append(aux)
                except:
                    # Probably a Timeout exception
                    pass"""
    return results

def grabEmails(emails=None, emailsFile=None, nicks=None, nicksFile=None, domains = ["gmail.com", "hushmail.com"]):
    '''
        Method that globally permits to grab the emails.
        
        :param emails:  list of emails.
        :param emailsFile: filepath to the emails file.
        :param nicks:   list of aliases.
        :param nicksFile:  filepath to the aliases file.
        :param domains: domains where the aliases will be tested.
        
        :result:    list of emails to check,
        
    '''
    email_candidates = []
    if emails != None:
        email_candidates = emails
    elif emailsFile != None:
        with open(emailsFile, "r") as iF:
            email_candidates = iF.read().splitlines()
    elif nicks != None:
        for n in nicks:
            for d in domains:
                email_candidates.append(n+"@"+d)
    elif nicksFile != None:
        with open(nicksFile, "r") as iF:
            nicks = iF.read().splitlines()    
            for n in nicks:
                for d in domains:
                    email_candidates.append(n+"@"+d)
    return email_candidates

def main(args):
    ''' 
        Main program.
        
        :param args: Arguments received in the command line.
    ''' 
    sayingHello = """mailfy.py Copyright (C) F. Brezo and Y. Rubio (i3visio) 2015
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions. For additional info, visit <http://www.gnu.org/licenses/gpl-3.0.txt>."""    
    if not args.quiet:
        print sayingHello
        print
        
    if args.create_emails:
        results = grabEmails(nicksFile = args.create_emails, domains = ["gmail.com"])
    else:
        emails = grabEmails(emails=args.emails, emailsFile = args.emails_file, nicks=args.nicks, nicksFile = args.nicks_file, domains = args.domains)

        results = performSearch(emails)

    # Trying to store the information recovered
    if args.output_folder != None:    
        if not os.path.exists(args.output_folder):
            os.makedirs(args.output_folder)
        # Grabbing the results 
        fileHeader = os.path.join(args.output_folder, args.file_header)                        
        for ext in args.extension:
            # Generating output files
            general.exportUsufy(results, ext, fileHeader)        

    # Showing the information gathered if requested                
    if not args.quiet:
        print "A summary of the results obtained are shown in the following table:"
        print unicode(general.usufyToTextExport(results))
        print

        print "You can find all the information collected in the following files:"                                                     
        for ext in args.extension:
            # Showing the output files
            print "\t-" + fileHeader + "." + ext        
                

def getParser():
    parser = argparse.ArgumentParser(description='mailfy.py - Checking the existence of a given mail.', prog='mailfy.py', epilog='Check the README.md file for further details on the usage of this program or follow us on Twitter in <http://twitter.com/i3visio>.', add_help=False)
    parser._optionals.title = "Input options (one required)"

    emailDomains = ["gmail.com", "hushmail.com"]

    # Defining the mutually exclusive group for the main options
    groupMainOptions = parser.add_mutually_exclusive_group(required=True)
    # Adding the main options
    groupMainOptions.add_argument('--license', required=False, action='store_true', default=False, help='shows the GPLv3+ license and exists.')    
    groupMainOptions.add_argument('-m', '--emails', metavar='<emails>', nargs='+', action='store', help = 'the list of emails to be checked.')
    groupMainOptions.add_argument('-M', '--emails_file', metavar='<emails_file>', action='store', help = 'the file with the list of emails.')    
    groupMainOptions.add_argument('-n', '--nicks', metavar='<nicks>', nargs='+', action='store', help = 'the list of nicks to be checked in the following platforms: ' +str(emailDomains))
    groupMainOptions.add_argument('-N', '--nicks_file', metavar='<nicks_file>', action='store', help = 'the file with the list of nicks to be checked in the following platforms: '+str(emailDomains))    
    groupMainOptions.add_argument('--create_emails', metavar='<nicks_file>',  action='store', help = 'the file with the list of nicks to be created in the following domains: '+str(emailDomains))    
    # Configuring the processing options
    groupProcessing = parser.add_argument_group('Processing arguments', 'Configuring the way in which mailfy will process the identified profiles.')
    #groupProcessing.add_argument('-L', '--logfolder', metavar='<path_to_log_folder', required=False, default = './logs', action='store', help='path to the log folder. If none was provided, ./logs is assumed.')        
    groupProcessing.add_argument('-e', '--extension', metavar='<sum_ext>', nargs='+', choices=['csv', 'gml', 'json', 'mtz', 'ods', 'png', 'txt', 'xls', 'xlsx' ], required=False, default = ['xls'], action='store', help='output extension for the summary files. Default: xls.')  
    groupProcessing.add_argument('-o', '--output_folder', metavar='<path_to_output_folder>', required=False, default = './results', action='store', help='output folder for the generated documents. While if the paths does not exist, usufy.py will try to create; if this argument is not provided, usufy will NOT write any down any data. Check permissions if something goes wrong.')
    groupProcessing.add_argument('-d', '--domains',  metavar='<candidate_domains>>',  action='store', help='list of domains where the nick will be looked for.', required=False, default = emailDomains)    
    # Getting a sample header for the output files
    groupProcessing.add_argument('-F', '--file_header', metavar='<alternative_header_file>', required=False, default = "profiles", action='store', help='Header for the output filenames to be generated. If None was provided the following will be used: profiles.<extension>.' )      
    groupProcessing.add_argument('--quiet', required=False, action='store_true', default=False, help='tells the program not to show anything.')        

    # About options
    groupAbout = parser.add_argument_group('About arguments', 'Showing additional information about this program.')
    groupAbout.add_argument('-h', '--help', action='help', help='shows this help and exists.')
    #groupAbout.add_argument('-v', '--verbose', metavar='<verbosity>', choices=[0, 1, 2], required=False, action='store', default=1, help='select the verbosity level: 0 - none; 1 - normal (default); 2 - debug.', type=int)
    groupAbout.add_argument('--version', action='version', version='%(prog)s ' +" " +__version__, help='shows the version of the program and exists.')

    return parser
                
if __name__ == "__main__":
    # Grabbing the parser
    parser = getParser()
    
    args = parser.parse_args()    

    # Calling the main function
    main(args)