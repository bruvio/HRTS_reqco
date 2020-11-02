#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 11/6/2018

@author: bruvio
"""
import sys
from getdat import getdat, getsca
import sys
from ppf import *
from sys import argv, exit
import requests
import pandas as pd
from datetime import date, timedelta
import logging
import pdb
from requests_kerberos import HTTPKerberosAuth
#import numpy as np
from numpy import size,linspace,arange,asscalar

ukaea_auth = HTTPKerberosAuth()

REQCO_API = "https://data.jet.uk/reqco/api/v1"
def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False
def waiting_requests_for_pulse(proc, pulse):
    """

    :param proc: process (lid3/lid4/lidall or any other registerd in Reqco)
    :param pulse:
    :return: returns requests for given inputs
    """
    url = "{}/processes/{}/requests/waiting?pulse={}".format(REQCO_API, proc, str(pulse))
    rsp = requests.get(url)
    return rsp.json()["data"]

def waiting_requests(proc):
    """

    :param proc:
    :return: returns request for given process
    """
    url = "{}/processes/{}/requests/waiting".format(REQCO_API, proc)
    rsp = requests.get(url)
    return rsp.json()["data"]


def writing_requests_pulse_list(proc,folder):
    """

    :param proc: process (hrts)
    :return: list of pulses that need to be validated for the input process idlist, \
     list of ids related to the pulses
    """

    url = "{}/processes/{}/requests/waiting".format(REQCO_API, proc)
    rsp = requests.get(url)
    # print(rsp.json())
    # pdb.set_trace()
    pulsesize = size(rsp.json()['data'])
    pulselist = []
    idlist = []
    requester = []
    daterequest = []
    if not rsp.json()['data']:
        # logging.info("List for process {} is empty".format(proc))
        # logging.info('no pulse to validate')
        return pulselist, idlist
    else:
        for ii in range(0, pulsesize):
            pulselist.append(rsp.json()["data"][ii]['pulse'])
            idlist.append(rsp.json()["data"][ii]['id'])
            requester.append(rsp.json()["data"][ii]['requester']['fullname'])
            daterequest.append(rsp.json()["data"][ii]['statushistory'][0]['date'])
            df = pd.DataFrame(
                list(zip(pulselist, requester, daterequest, idlist)),columns=['pulse','requester','date','id'])
            df.to_csv(folder+'reqco_list_' +proc+'_' + str(date.today()) + '.csv')

    proc = 'hrts'
    pulselist = []
    logging.info('writing to file pulses to process')

    logging.info('looking into process {}'.format(proc))
    url = "{}/processes/{}/requests/waiting".format(REQCO_API, proc)
    rsp = requests.get(url)
    # print(rsp.json())
    # pdb.set_trace()
    pulsesize = size(rsp.json()['data'])
    if not rsp.json()['data']:
        # logging.info("List for process {} is empty".format(proc))
        # logging.info('no pulse to validate')
        pass
    else:
        for ii in range(0, pulsesize):
            pulselist.append(rsp.json()["data"][ii]['pulse'])
    pulselist=set(pulselist)
    pulselist=set(pulselist)
    pulselist=list(pulselist)
    df = pd.DataFrame(list(pulselist),columns=['pulse'])
    df.to_csv(folder+'reqco_pulselist_' + str(date.today()) + '.csv',index=False)
    logging.info('pulselist written to ')






def waiting_requests_pulse_list(proc):
    """

    :param proc: process (lid3, lid4 or lidall)
    :return: list of pulses that need to be validated for the input process idlist, \
     list of ids related to the pulses
    """
    url = "{}/processes/{}/requests/waiting".format(REQCO_API, proc)
    rsp = requests.get(url)
    # print(rsp.json())
    # pdb.set_trace()
    pulsesize=size(rsp.json()['data'])
    pulselist=[]
    idlist=[]
    if not rsp.json()['data']:
        # logging.info("List for process {} is empty".format(proc))
        # logging.info('no pulse to validate')
        return pulselist, idlist
    else:
        for ii in range(0,pulsesize):
            pulselist.append(rsp.json()["data"][ii]['pulse'])
            idlist.append(rsp.json()["data"][ii]['id'])

        return pulselist,idlist




def set_request_done(id, ppf,message=None):
    """

    :param id: id of request
    :param ppf: dda (ppf) to be set done
    :param message: RO comments about the validation process
    :return: sets done the given request
    """
    if message is None:
        sms="Request DONE. " \
            "This is an automated message contact RO if you want more info."
    else:
        sms=message
    response = requests.patch("{}/requests/{}".format(REQCO_API, str(id)),
                              data={"status": "done",
                                    "datascheme": "ppf",
                                    "datalocation": ppf,
                                    "comment": sms},
                              auth=ukaea_auth)
    return response

def set_request_closed(id, ppf,message=None):
    """

    :param id: id of request
    :param ppf: dda (ppf) to be set done
    :param message: RO comments about the validation process
    :return: sets close the given request.Essentially "closed" means it's not done, but for non-physics reasons.

    """
    if message is None:
        sms="Request CLOSED. Due to external factors (e.g. lack of time or funding), the request will not be fulfilled. This is an automated message contact RO if you want more info"
    else:
        sms=message
    response = requests.patch("{}/requests/{}".format(REQCO_API, str(id)),
                              data={"status": "closed",
                                    "datascheme": "ppf",
                                    "datalocation": ppf,
                                    "comment": sms},
                              auth=ukaea_auth)
    return response

def set_request_impossible(id,message=None):
    """

    :param id: id of request
    :param ppf: dda (ppf) to be set done
    :param message: RO comments about the validation process
    :return: sets impossible the given request
    """

    if message is None:
        sms="Request IMPOSSIBLE. It is impossible to validate the provided shot and/or parameters. This is an automated message contact RO if you want more info"
    else:
        sms=message
    response = requests.patch("{}/requests/{}".format(REQCO_API, str(id)),
                              data={"status": "impossible",
                                    "comment": sms},
                              auth=ukaea_auth)
    return response

# def main(args):
#     process=args[0]
    # waiting_requests('lid3')
    # waiting_requests_pulse_list(process)

def GetSF(pulse, dda,dtype):
    """
    returns list of status flag for given,pulse,dda and dtype
    :param pulse:
    :param dda:
    :param dtype:
    :return:
    """


    # this sequence of instruction allows to extract status flag correctly for each pulse
    ihdat,iwdat,data,x,t,ier=ppfget(pulse,dda,dtype)
    pulse,seq,iwdat,comment,numdda,ddalist,ier=ppfinf(comlen=50,numdda=50)
    #info,cnfo,ddal,istl,pcom,pdsn,ier=pdinfo(pulse,seq) #commented lines, with this i get an error.
    istat,ier = ppfgsf(pulse,seq,dda,dtype,mxstat=1)

    # print('GETSF ok')

    return (istat)


def main(label):
    '''

    reads reqco database and looks for pulses that must be validated

    if dtype NE in the DDA HRTS is anything other than 0, pulse is validated

    '''
    # print(label)
    # pdb.set_trace()
    if len(label) < 2 :
        logging.error("Usage: %s <hrts> ",format(label[0]))
        exit()
        #
    if label[1] == 'hrts':
            process = 'hrts'
            pulselist = []
            idlist = []
            logging.info('process %s',format(process))
            ppf = "HRTS/NE"
            pulselist, idlist = waiting_requests_pulse_list(process)
            if not pulselist:
                logging.info("List for process {} is empty".format(process))
                logging.info('no pulse to validate')
                logging.info('DONE')
                return
            else:
                logging.info('this is the pulse list in Reqco database')
                logging.info('%s',str(pulselist))
                if size(pulselist) <2:
                    logging.info('only %s pulse in the list',str(size(pulselist)))
                if size(pulselist) >1:
                    logging.info('we have a total of %s pulses',str(size(pulselist)))
                pulselist_new = pulselist
                idlist_new = []
                for i, j in enumerate(pulselist):
                    for hh, kk in enumerate(pulselist_new):
                        if pulselist[i] == pulselist_new[hh]:
                            idlist_new.append(idlist[i])

                for i, pulse in enumerate(pulselist_new):

                    SF_list = []



                    id = idlist_new[i]
                    st_ch = GetSF(pulse, 'hrts', 'ne')
                    st_ch = asscalar(st_ch)
                    SF_list.append(st_ch)
                    logging.debug(
                        'processing pulse %s ',str(pulse))

                    if (st_ch > 0):
                        # set pulse as done
                        logging.info('%s has the following SF %s',str(pulse), SF_list)

                        logging.info('hrts for pulse %s will be set done',str(pulse))
                        reqs = waiting_requests_for_pulse(process, str(pulse))
                        if not reqs:
                            logging.error(
                                'the selected combination of process %s and pulse %s is not in Reqco database',
                                process, str(pulse))
                        else:

                            for req in reqs:
                                id = req["id"]
                                logging.info('marking JPN %s as done', str(pulse))

## commented out these lines to remove requests for persolanised message to requester

                                # if yes_or_no('set message to requester? Y/N') :
                                #     sms=input()
                                # else:
                                #     sms=None
                                sms = None
##
                                try:
                                    r = set_request_done(id, ppf,message=sms)
                                except:
                                    logging.error('error! check error message')

                                #
                                if r.status_code != 200:
                                    logging.ERROR("Server returned error:")
                                    logging.ERROR(r.text)
                                    return
                                else:
                                    logging.info('JPN %s marked as done\n',
                                                str(pulse))

                    else:
                            logging.info('%s needs to be validated \n', str(pulse))
                logging.info('DONE')
                return


    #
    else:

        logging.error("Usage: %s <hrts> ", str(label[0]))

        return


# Custom formatter
class MyFormatter(logging.Formatter):

    err_fmt  = "%(levelname)-8s %(message)s"
    dbg_fmt  = "%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
    info_fmt = "%(levelname)-8s %(message)s"

    # def __init__(self):
    #     super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style='%')

    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._style._fmt = MyFormatter.dbg_fmt

        elif record.levelno == logging.INFO:
            self._style._fmt = MyFormatter.info_fmt

        elif record.levelno == logging.ERROR:
            self._style._fmt = MyFormatter.err_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result


if __name__ == "__main__":
    # logging.basicConfig(
    #     # format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    #     format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    #     # datefmt='%d-%m-%Y:%H:%M:%S',
    #     level=logging.DEBUG)
    #
    # logger = logging.getLogger(__name__)
    fmt = MyFormatter()
    hdlr = logging.StreamHandler(sys.stdout)

    hdlr.setFormatter(fmt)
    logging.root.addHandler(hdlr)
    logging.root.setLevel(logging.INFO)
    main(argv)
