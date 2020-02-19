#!/usr/bin/env python
from config import *
from scripts import *
import sys
import subprocess

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


def compare_data_listings(cruise):  # compares listings on different servers
    ship_abbreviation = get_ship_abbreviation(cruise.upper())
    org = ''
    if ship_abbreviation in org_from_cruise.keys():
        org = org_from_cruise[ship_abbreviation]
    elif cruise == 'ocport':
        org = 'OSU'
    if org == 'UAF':  # for Sikuliaq cruises
        UAF_process = subprocess.Popen(
            'rsync -r share.sikuliaq.alaska.edu::SKQDATA/{}'.format(cruise),
            stdout=subprocess.PIPE, shell=True)
        UAF_output, err = UAF_process.communicate()  # lists all UAF files
        SIO_process = subprocess.Popen(
            "ls -ltraR /mnt/gdc/data/r2r/scratch/edu.uaf/{} |egrep -v \
'\.$|\.\.|\.:|\.\/|total|^d' |sed '/^$/d'".format(
                cruise), stdout=subprocess.PIPE, shell=True)  # lists full tree
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
            log.write(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      'The data listings match up for {}\n'.format(cruise))
            log.write(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
            log.write(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on UAF system: {}'.format(cruise,
                      len(UAF_output.split('\n'))))
        else:  # runs if the number of files is NOT the same
            if '-v' in args:
                print('ERROR: ' +
                      datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      'The data listings \
                      DO NOT match up for {}'.format(cruise))
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
                print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on UAF system: {}'.format(cruise,
                      len(UAF_output.split('\n'))))
            log.write('ERROR: ' +
                      datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      'The data listings \
                      DO NOT match up for {}\n'.format(cruise))
            log.write(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
            log.write(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on UAF system: {}'.format(cruise,
                      len(UAF_output.split('\n'))))
    if org == 'OSU':  # for Oceanus cruises
        OSU_process = subprocess.Popen(
            'rsync -r \
r2r@untangle.coas.oregonstate.edu://{}/{}'.format(datadir_OSU, cruise),
            stdout=subprocess.PIPE, shell=True)
        OSU_output, err = OSU_process.communicate()  # lists all OSU files
        SIO_process = subprocess.Popen(
            "ls -ltraR /mnt/gdc/data/r2r/scratch/edu.oregonstate/{} |egrep -v \
'\.$|\.\.|\.:|\.\/|total|^d' |sed '/^$/d'".format(
                cruise),
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
            log.write(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      'The data listings match up for {}\n'.format(cruise))
            log.write(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
            log.write(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on OSU system: {}'.format(cruise,
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
            log.write('ERROR: ' +
                      datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      'The data listings \
                      DO NOT match up for {}\n'.format(cruise))
            log.write(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on local system: {}'.format(cruise,
                      len(SIO_output.split('\n'))))
            log.write(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                      '{} file count on OSU system: {}'.format(cruise,
                      len(OSU_output.split('\n'))))
    else:
        if '-v' in args:
            print('ERROR: ' + datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                  'Cannot compare data listings for {}'.format(cruise))
        log.write('ERROR: ' + datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                  'Cannot compare data listings for {}\n'.format(cruise))


def compare_from_list(list):  # compares a list of cruises
    file = open('/localdisk2/R2R/code/{}'.format(list), 'r')  # opens list
    list = [line.rstrip('\n') for line in file]  # splits cruises into a list
    if '-v' in args:
        print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
              "Running data listing comparison")
    log.write(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
              "Running data listing comparison\n")
    for each in list:
        compare_data_listings(each)
    if '-v' in args:
        print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
              "Script finished executing")
    log.write(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
              "Script finished executing\n")


cruise = ''

for i in range(len(args)):  # finds cruise in args
    if args[i][0] != '-' and args[i][0] != '.' and args[i][0] != '/':
        cruise = args[i]

log = open(log_dir + datetime.now().strftime('%Y-%m-%dT%H:%M:%S_')
           + 'compare_data_listings.py_' + cruise + '.txt', 'w+')
log.write(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
          'compare_data_listings.py executed\n')

if '-l' in args:  # checks to see if script needs to run from list
    list = 'list.txt'
    for i in range(len(args)):
        if args[i][0] != '-' and args[i][0] != '.' and args[i][0] != '/':
            list = args[i]
    compare_from_list(list)
else:
    compare_data_listings(cruise)
