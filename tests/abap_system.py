# SPDX-FileCopyrightText: 2013 SAP SE Srdjan Boskovic <srdjan.boskovic@sap.com>
#
# SPDX-License-Identifier: Apache-2.0

abap_system = {
    "p7019s16": {
        "user": "demo",
        "passwd": "Welcome",
        "ashost": "10.117.19.101",
        "saprouter": "/H/203.13.155.17/W/xjkb3d/H/172.19.138.120/H/",
        "sysnr": "00",
        "lang": "EN",
        "client": "100",
    },
    "MME": {
        "user": "demo",
        "passwd": "welcome",
        "ashost": "10.68.110.51",
        "sysnr": "00",
        "client": "620",
        "lang": "EN",
    },
    "DSP": {
        "user": "demo",
        "passwd": "welcome",
        "ashost": "10.68.104.164",
        "sysnr": "00",
        "client": "620",
        "lang": "EN",
    },
    "QM7": {
        "user": "NWRFCTEST",
        "passwd": "Welcome1",
        "ashost": "ldciqm7.wdf.sap.corp",
        "sysnr": "20",
        "group": "PUBLIC",
        "client": "002",
        "lang": "EN",
    },
}


def connection_info(sid="MME"):
    return abap_system[sid]
