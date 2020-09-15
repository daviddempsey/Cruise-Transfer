#!/usr/bin/env python
import os
from config import *
from scripts import *
from datetime import datetime
import sys
import logging

# get_cruise.py
# Created by David Dempsey
# email: ddempsey@ucsd.edu
#
# ## Purpose:
# Pulls cruise data locally
#
# ## Usage:
# [cruise id] runs a cruise ID (ex: RR1801)
# -l [no argument] pulls all cruises off of a list (in /code/)
# (default list: list.txt)
# -a lists all cruises under an abbreviation (ex: "SP")
# -v will output logs to the console
# -h shows what each flag does
# -d will delete local files in same directory that were not pulled over

args = sys.argv
script_dir = os.getcwd()
delete = ''


def get_cruise(cruise):  # runs rsync based off of a cruise ID
    # finds ship and org based off of cruise
    ship, org = auto_identify(cruise)

    logging.info(cruise + ' labelled as ' + ship)

    # checks to see if already run
    exists = os.path.isdir(datadir_local + '/' + ship + '/' + cruise)
    # logs if cruise already exists
    if exists and '-o' not in args:
        logging.info(datadir_local + '/' + cruise + ' already exists')
    else:  # otherwise runs rsync
        rsync_cruises(cruise, ship, org)


def run_cruise_ID(cruise):  # verifies cruise ID before running rsync
    ship_abbreviation = get_ship_abbreviation(cruise)  # gets cruise identifier

    if '-v' in args:
        print("Running inputted cruise ID")

    # checks validity of cruise ID
    if ship_abbreviation.upper() in ships.keys():  # will run rsync if valid
        get_cruise(cruise)
        if '-v' in args:  # indicates that rsync is finished
            print("Finished running cruise ID")

    else:  # invalid cruise
        if '-v' in args:
            print("Incorrect cruise ID")


def identify_datadir(org):  # identifies cruise organization data directory
    datadir = ''
    if org == 'SIO':
        datadir = datadir_SIO
    if org == 'OSU':
        datadir = datadir_OSU
    if org == 'UAF':
        datadir = datadir_UAF
    if org == 'UW':
        datadir = datadir_UW
    return datadir  # returns string with organization data directory


def rsync_cruises(cruise, ship, org):  # runs rsync
    datadir = identify_datadir(org)  # finds org data directory

    rsync_txt_check, rsync_cruise_check = (0, 0)  # used to log errors

    # runs rsync for SIO
    if org == 'SIO':
        localdir = ship_directory[ship]
        rsync_txt_check = os.system(rsync_by_org[org][0].format(
            ship_title=ship, cruise_title=cruise, dir=localdir))
        rsync_cruise_check = os.system(
            rsync_by_org[org][1].format(ship_title=ship,
                                        cruise_title=cruise, dir=localdir)
            + delete
            + " | tee -a {}/{}.rsynclist.txt {}/{}".format(
                localdir, cruise, log_dir, logfile))

    # runs rsync for Oregon State
    if org == 'OSU':
        rsync_cruise_check = os.system(
            rsync_by_org[org][0].format(cruise_title=cruise, dir=datadir)
            + delete
            + " | tee -a {}/{}".format(log_dir, logfile) + " > /dev/null")


    # runs rsync for UAF
    if org == 'UAF':
        localdir = ship_directory[ship]
        rsync_cruise_check = os.system(
            rsync_by_org[org].format(ship_title=ship, dir=localdir,
                                     cruise_title=cruise)
            + delete
            + " | tee -a {}/{}.txt {}/{}".format(
                localdir, cruise, log_dir, logfile))

    # runs rsync for UW
    if org == 'UW':
        localdir = ship_directory[ship]
        if cruise[:2].upper() == 'TN':
            rsync_cruise_check = os.system(
                rsync_by_org[org][0].format(cruise_title=cruise, dir=datadir)
                + delete
                + " | tee -a {}/{}".format(log_dir, logfile) + " > /dev/null")
        else:
            rsync_cruise_check = os.system(
                rsync_by_org[org][1].format(cruise_title=cruise, dir=datadir)
                + delete
                + " | tee -a {}/{}".format(log_dir, logfile) + " > /dev/null")

    # logs that error occured
    if rsync_cruise_check != 0:
        if '-v' in args:
            print('ERROR: rsync error occurred running ' +
                  rsync_by_org[org][1].format(ship_title=ship,
                                              cruise_title=cruise,
                                              dir=datadir))
        logging.error('rsync error occurred running ' +
                      rsync_by_org[org][1].format(ship_title=ship,
                                                  cruise_title=cruise,
                                                  dir=datadir))

    # logs that rsync successfully ran
    if rsync_txt_check == 0 and rsync_cruise_check == 0:
        if '-v' in args:
            print('rsync successfully executed for cruise ' + cruise)
        logging.info('rsync successfully executed for cruise ' + cruise)

    errorlogfile = logfile + "_errors"
    os.system("grep -e error -e failed {}/{} >> {}".format(log_dir,
                                                           logfile, errorlogfile))


def read_list(list, function, args):
    os.chdir(script_dir)
    file = open('{}'.format(list), 'r')  # opens list of cruises
    os.chdir(log_dir)
    list = [line.rstrip('\n') for line in file]   # splits cruises into a list
    if '-v' in args:
        print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
              "Pulling cruises from list")
    for cruise in list:
        function(cruise)
    if '-v' in args:
        print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
              "Script finished executing")


cruise = ''
for i in range(len(args)):  # extracts cruise ID from arguments
    if "-l" in args:
        cruise = 'list.txt'
    elif args[i] not in unread_args and args[i] != 'get_cruise.py':
        cruise = args[i]


# parses command line arguments
if len(args) > 1:
    if '-h' in args:  # outputs usage information
        print('Input an argument: ')
        print('-l runs from list')
        print('[cruise_id] runs a cruise ID')
        print('-a [ship abbreviation] lists all logged cruises by ship')
        print('-v will output process updates to the console')
        print('-d will delete local files in same directory that were not pulled over')
        exit()

    os.chdir(log_dir)  # creates log file
    logfile = datetime.now().strftime('%Y-%m-%dT%H:%M:%S_') + \
        'get_cruise.py_' + cruise
    logging.basicConfig(format='%(asctime)s %(message)s', filename='%s' %
                        (logfile),
                        level=logging.INFO)
    logging.info('get_cruise.py executed')

    if '-d' in args:
        logging.info('Rsync flag --delete-after enabled')
        delete = " --delete-after"
    if '-l' in args:  # runs list of cruises
        logging.info('Reading from list')
        list = 'list.txt'
        for i in range(len(args)):
            if args[i] == "-l":
                list = args[i+1]
        read_list(list, get_cruise, args)

    elif '-a' in args:  # prints which cruises can be rsynced
        list_from_abbreviation(args)
    else:  # runs cruise ID if no other args
        run_cruise_ID(cruise)

else:  # outputs usage information if no args given
    print('Input an argument: ')
    print('-l runs from list')
    print('[cruise_id] runs a cruise ID')
    print('-a [ship abbreviation] lists all logged cruises by ship')
    print('-v will output process updates to the console')
    print('-d will delete local files that weren\'t found on the remote server')
    print('-d will delete local files in same directory that were not pulled over')
