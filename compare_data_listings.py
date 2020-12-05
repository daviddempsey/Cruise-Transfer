#!/usr/bin/env python
from config import *
from scripts import *
import sys
import subprocess
import os
import logging

# compare_data_listings.py
# Created by David Dempsey
# email: ddempsey@ucsd.edu
#
# ## Purpose:
# Compares data listings on two different servers
#
# ## Usage:
# [cruise ID] will compare data listings for the cruise ID
# -v will output process updates to the console


args = sys.argv
script_dir = os.getcwd()

def compare_data_listings(cruise):  # compares listings on different servers
    ship_abbreviation = get_ship_abbreviation(cruise.upper())
    org = ''
    if ship_abbreviation in org_from_cruise.keys():
        org = org_from_cruise[ship_abbreviation]
    elif cruise == 'ocport':
        org = 'OSU'
    if org == 'UAF':  # for Sikuliaq cruises
        UAF_process = subprocess.Popen(
            uaf_full_listings_remote + cruise,
            stdout=subprocess.PIPE, shell=True)
        UAF_output, err = UAF_process.communicate()  # lists all UAF files
        SIO_process = subprocess.Popen(
            uaf_full_listings_local + cruise + " |egrep -v \
'\.$|\.\.|\.:|\.\/|total|^d' |sed '/^$/d'", stdout=subprocess.PIPE, shell=True)  # lists full tree
        SIO_output, err = SIO_process.communicate()  # lists all SIO files
        if len(UAF_output.split('\n')) == len(SIO_output.split('\n')):
            if '-v' in args:
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      'The data listings match up for {}'.format(cruise))
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on UAF system: {}'.format(cruise,
                       len(UAF_output.split('\n'))))
            logging.info(
                      'The data listings match up for {}\n'.format(cruise))
            logging.info(
                      '{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
            logging.info(
                      '{} file count on UAF system: {}'.format(cruise,
                      len(UAF_output.split('\n'))))
        else:  # runs if the number of files is NOT the same
            if '-v' in args:
                print('ERROR: ' +
                      datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      'The data listings DO NOT match up for {}'.format(cruise))
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on UAF system: {}'.format(cruise,
                      len(UAF_output.split('\n'))))
            logging.error('ERROR: The data listings \
                      DO NOT match up for {}\n'.format(cruise))
            logging.info('{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
            logging.info('{} file count on UAF system: {}'.format(cruise,
                      len(UAF_output.split('\n'))))
    if org == 'OSU':  # for Oceanus cruises
        OSU_process = subprocess.Popen(
        osu_full_listings_remote + '{}/{}'.format(datadir_OSU, cruise),
            stdout=subprocess.PIPE, shell=True)
        OSU_output, err = OSU_process.communicate()  # lists all OSU files
        SIO_process = subprocess.Popen(
            osu_full_listings_local + cruise + " |egrep -v \
'\.$|\.\.|\.:|\.\/|total|^d' |sed '/^$/d'",
            stdout=subprocess.PIPE, shell=True)  # lists full tree
        SIO_output, err = SIO_process.communicate()  # lists all SIO files
        if len(OSU_output.split('\n')) == len(SIO_output.split('\n')):
            if '-v' in args:
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      'The data listings match up for {}'.format(cruise))
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on OSU system: {}'.format(cruise,
                      len(OSU_output.split('\n'))))
            logging.info('The data listings match up for {}\n'.format(cruise))
            logging.info('{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
            logging.info('{} file count on OSU system: {}'.format(cruise,
                      len(OSU_output.split('\n'))))
        else:
            if '-v' in args:
                print('ERROR: ' +
                      datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      'The data listings \
                      DO NOT match up for {}'.format(cruise))
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on OSU system: {}'.format(cruise,
                      len(OSU_output.split('\n'))))
            logging.error('ERROR: The data listings DO NOT match up for {}\n'.format(cruise))
            logging.info('{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
            logging.info('{} file count on OSU system: {}'.format(cruise,
                      len(OSU_output.split('\n'))))
    if org == 'UW':  # for University of Washington cruises
        UW_process = subprocess.Popen(uw_full_listings_remote + cruise,
            stdout=subprocess.PIPE, shell=True)
        UW_output, err = UW_process.communicate()  # lists all UW files
        SIO_process = subprocess.Popen(
            uw_full_listings_local + cruise + " |egrep -v \
'\.$|\.\.|\.:|\.\/|total|^d' |sed '/^$/d'",
            stdout=subprocess.PIPE, shell=True)  # lists full tree
        SIO_output, err = SIO_process.communicate()  # lists all SIO files
        if len(UW_output.split('\n')) == len(SIO_output.split('\n')):
            if '-v' in args:
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      'The data listings match up for {}'.format(cruise))
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on UW system: {}'.format(cruise,
                      len(UW_output.split('\n'))))
            logging.info('The data listings match up for {}\n'.format(cruise))
            logging.info('{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
            logging.info('{} file count on UW system: {}'.format(cruise,
                      len(UW_output.split('\n'))))
        else:
            if '-v' in args:
                print('ERROR: ' +
                      datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      'The data listings \
                      DO NOT match up for {}'.format(cruise))
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on UW system: {}'.format(cruise,
                      len(UW_output.split('\n'))))
            logging.error('ERROR: The data listings DO NOT match up for {}\n'.format(cruise))
            logging.info('{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
            logging.info('{} file count on UW system: {}'.format(cruise,
                      len(UW_output.split('\n'))))
    else:
        if '-v' in args:
            print('ERROR: ' + datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                  'Cannot compare data listings for {}'.format(cruise))
        logging.error('ERROR: Cannot compare data listings for {}\n'.format(cruise))


def compare_from_list(list):  # compares a list of cruises
    os.chdir(script_dir)
    file = open(os.getcwd() + '/{}'.format(list), 'r')  # opens list
    list = [line.rstrip('\n') for line in file]  # splits cruises into a list
    os.chdir(log_dir)
    if '-v' in args:
        print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
              "Running data listing comparison")
    logging.info("Running data listing comparison\n")
    for each in list:
        compare_data_listings(each)
    if '-v' in args:
        print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
              "Script finished executing")
    logging.info("Script finished executing\n")


cruise = ''

for i in range(len(args)):  # finds cruise in args
    if args[i][0] != '-' and args[i][0] != '.' and args[i][0] != '/':
        cruise = args[i]

os.chdir(log_dir)
logfile = datetime.now().strftime('%Y-%m-%dT%H:%M:%S_') + 'compare_data_listings.py_' + cruise
logging.basicConfig(format='%(asctime)s %(message)s', filename='%s' %
                    (logfile),
                    level=logging.INFO)
logging.info('compare_data_listings.py executed')


if '-l' in args:  # checks to see if script needs to run from list
    list = 'list.txt'
    for i in range(len(args)):
        if args[i][0] != '-' and args[i][0] != '.' and args[i][0] != '/':
            list = args[i]
    compare_from_list(list)
else:
    compare_data_listings(cruise)
