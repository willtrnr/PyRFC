#!/usr/bin/env python

# SPDX-FileCopyrightText: 2013 SAP SE Srdjan Boskovic <srdjan.boskovic@sap.com>
#
# SPDX-License-Identifier: Apache-2.0

# -*- coding: utf-8 -*-

import datetime
import socket
import unittest
from decimal import Decimal

import pyrfc
from tests.config import (
    CONFIG_SECTIONS as config_sections,
    PARAMS as params,
    UNICODETEST,
    get_error,
)


class TestConnection:
    def setup_method(self, test_method):
        self.conn = pyrfc.Connection(**params)
        assert self.conn.alive

    def teardown_method(self, test_method):
        self.conn.close()
        assert not self.conn.alive

    def test_version_and_options_getters(self):
        with open("VERSION", "r") as f:
            VERSION = f.read().strip()
            version = self.conn.version
            assert "major" in version
            assert "minor" in version
            assert "patchLevel" in version
            assert pyrfc.__version__ == VERSION
        assert all(
            k in self.conn.options for k in ("dtime", "return_import_params", "rstrip")
        )

    def test_connection_info(self):
        connection_info = self.conn.get_connection_attributes()
        info_keys = (
            "dest",
            "host",
            "partnerHost",
            "sysNumber",
            "sysId",
            "client",
            "user",
            "language",
            "trace",
            "isoLanguage",
            "codepage",
            "partnerCodepage",
            "rfcRole",
            "type",
            "partnerType",
            "rel",
            "partnerRel",
            "kernelRel",
            "cpicConvId",
            "progName",
            "partnerBytesPerChar",
            "partnerIP",
            "partnerIPv6"
            # 'reserved'
        )
        assert all(k in connection_info for k in info_keys)

    def test_connection_info_attributes(self):
        data = self.conn.get_connection_attributes()
        assert data["client"] == str(params["client"])
        assert data["host"] == str(socket.gethostname())
        assert data["isoLanguage"] == str(params["lang"].upper())
        # Only valid for direct logon systems:
        # self.assertEqual(data['sysNumber'], str(params['sysnr']))
        assert data["user"] == str(params["user"].upper())
        assert data["rfcRole"] == u"C"

    def test_connection_info_disconnected(self):
        self.conn.close()
        assert not self.conn.alive
        connection_info = self.conn.get_connection_attributes()
        assert connection_info == {}

    def test_reopen(self):
        assert self.conn.alive
        self.conn.reopen()
        assert self.conn.alive
        self.conn.close()
        assert not self.conn.alive
        self.conn.reopen()
        assert self.conn.alive

    def test_call_over_closed_connection(self):
        conn = pyrfc.Connection(config={"rstrip": False}, **config_sections["coevi51"])
        conn.close()
        assert conn.alive == False
        hello = u"Hällo SAP!"
        try:
            result = conn.call("STFC_CONNECTION", REQUTEXT=hello)
        except pyrfc.RFCError as ex:
            print(ex.args)
            assert (
                ex.args[0]
                == "Remote function module STFC_CONNECTION invocation rejected because the connection is closed"
            )

    def test_config_parameter(self):
        # rstrip test
        conn = pyrfc.Connection(config={"rstrip": False}, **config_sections["coevi51"])
        hello = u"Hällo SAP!" + u" " * 245
        result = conn.call("STFC_CONNECTION", REQUTEXT=hello)
        # Test with rstrip=False (input length=255 char)
        assert result["ECHOTEXT"] == hello
        result = conn.call("STFC_CONNECTION", REQUTEXT=hello.rstrip())
        # Test with rstrip=False (input length=10 char)
        assert result["ECHOTEXT"] == hello
        conn.close()
        # dtime test
        conn = pyrfc.Connection(config={"dtime": True}, **config_sections["coevi51"])
        dates = conn.call("BAPI_USER_GET_DETAIL", USERNAME="demo")["LASTMODIFIED"]
        assert type(dates["MODDATE"]) is datetime.date
        assert type(dates["MODTIME"]) is datetime.time
        del conn
        conn = pyrfc.Connection(**config_sections["coevi51"])
        dates = conn.call("BAPI_USER_GET_DETAIL", USERNAME="demo")["LASTMODIFIED"]
        assert type(dates["MODDATE"]) is not datetime.date
        assert type(dates["MODDATE"]) is not datetime.time
        del conn
        # no import params return
        result = self.conn.call("STFC_CONNECTION", REQUTEXT=hello)
        assert "REQTEXT" not in result
        # return import params
        conn = pyrfc.Connection(
            config={"return_import_params": True}, **config_sections["coevi51"]
        )
        result = conn.call("STFC_CONNECTION", REQUTEXT=hello.rstrip())
        assert hello.rstrip() == result["REQUTEXT"]
        conn.close()

    def test_ping(self):
        assert self.conn.alive
        self.conn.ping()
        self.conn.close()
        try:
            self.conn.ping()
        except pyrfc.ExternalRuntimeError as ex:
            error = get_error(ex)
            assert error["code"] == 13
            assert error["key"] == "RFC_INVALID_HANDLE"
            assert (
                error["message"][0]
                == "An invalid handle 'RFC_CONNECTION_HANDLE' was passed to the API call"
                or error["message"][0] == "An invalid handle was passed to the API call"
            )

    def test_RFM_name_string(self):
        result = self.conn.call("STFC_CONNECTION", REQUTEXT=UNICODETEST)
        assert result["ECHOTEXT"] == UNICODETEST

    def test_RFM_name_unicode(self):
        result = self.conn.call(u"STFC_CONNECTION", REQUTEXT=UNICODETEST)
        assert result["ECHOTEXT"] == UNICODETEST

    def test_RFM_name_invalid_type(self):
        try:
            self.conn.call(123)
        except Exception as ex:
            assert ex.args == (
                "Remote function module name must be unicode string, received:",
                123,
                int,
            )

    def test_STFC_returns_structure_and_table(self):
        IMPORTSTRUCT = {
            "RFCFLOAT": 1.23456789,
            "RFCCHAR1": "A",
            "RFCCHAR2": "BC",
            "RFCCHAR4": "DEFG",
            "RFCINT1": 1,
            "RFCINT2": 2,
            "RFCINT4": 345,
            "RFCHEX3": bytes(b"\x01\x02\x03"),
            "RFCTIME": "121120",
            "RFCDATE": "20140101",
            "RFCDATA1": "1DATA1",
            "RFCDATA2": "DATA222",
        }
        INPUTROWS = 10
        IMPORTTABLE = []
        for i in range(INPUTROWS):
            row = IMPORTSTRUCT
            row["RFCINT1"] = i
            IMPORTTABLE.append(row)
        result = self.conn.call(
            "STFC_STRUCTURE", IMPORTSTRUCT=IMPORTSTRUCT, RFCTABLE=IMPORTTABLE
        )
        # ECHOSTRUCT match IMPORTSTRUCT
        for k in IMPORTSTRUCT:
            assert result["ECHOSTRUCT"][k] == IMPORTSTRUCT[k]

        # check if row added
        assert len(result["RFCTABLE"]) == INPUTROWS + 1

        # output table match import table
        for i in range(INPUTROWS):
            row_in = IMPORTTABLE[i]
            row_out = result["RFCTABLE"][i]
            assert row_in == row_out

        # added row match incremented IMPORTSTRUCT
        added_row = result["RFCTABLE"][INPUTROWS]
        assert added_row["RFCFLOAT"] == IMPORTSTRUCT["RFCFLOAT"] + 1
        assert added_row["RFCINT1"] == IMPORTSTRUCT["RFCINT1"] + 1
        assert added_row["RFCINT2"] == IMPORTSTRUCT["RFCINT2"] + 1
        assert added_row["RFCINT4"] == IMPORTSTRUCT["RFCINT4"] + 1

    def test_STFC_STRUCTURE(self):
        # STFC_STRUCTURE Inhomogene Struktur
        imp = dict(
            RFCFLOAT=1.23456789,
            RFCINT2=0x7FFE,
            RFCINT1=0x7F,
            RFCCHAR4=u"bcde",
            RFCINT4=0x7FFFFFFE,
            RFCHEX3="fgh".encode("utf-8"),
            RFCCHAR1=u"a",
            RFCCHAR2=u"ij",
            RFCTIME="123456",  # datetime.time(12,34,56),
            RFCDATE="20161231",  # datetime.date(2011,10,17),
            RFCDATA1=u"k" * 50,
            RFCDATA2=u"l" * 50,
        )
        out = dict(
            RFCFLOAT=imp["RFCFLOAT"] + 1,
            RFCINT2=imp["RFCINT2"] + 1,
            RFCINT1=imp["RFCINT1"] + 1,
            RFCINT4=imp["RFCINT4"] + 1,
            RFCHEX3=b"\xf1\xf2\xf3",
            RFCCHAR1=u"X",
            RFCCHAR2=u"YZ",
            RFCDATE=str(datetime.date.today()).replace("-", ""),
            RFCDATA1=u"k" * 50,
            RFCDATA2=u"l" * 50,
        )
        table = []
        xtable = []
        records = ["1111", "2222", "3333", "4444", "5555"]
        for rid in records:
            imp["RFCCHAR4"] = rid
            table.append(imp)
            xtable.append(imp)
        # print 'table len', len(table), len(xtable)
        result = self.conn.call("STFC_STRUCTURE", IMPORTSTRUCT=imp, RFCTABLE=xtable)
        # print 'table len', len(table), len(xtable)
        assert result["RESPTEXT"].startswith("SAP")
        # assert result['ECHOSTRUCT'] == imp
        assert len(result["RFCTABLE"]) == 1 + len(table)
        for i in result["ECHOSTRUCT"]:
            assert result["ECHOSTRUCT"][i] == imp[i]
        del result["RFCTABLE"][5]["RFCCHAR4"]  # contains variable system id
        del result["RFCTABLE"][5]["RFCTIME"]  # contains variable server time
        for i in result["RFCTABLE"][5]:
            assert result["RFCTABLE"][5][i] == out[i]

    def test_STFC_CHANGING(self):
        # STFC_CHANGING example with CHANGING parameters
        start_value = 33
        counter = 88
        result = self.conn.call(
            "STFC_CHANGING", START_VALUE=start_value, COUNTER=counter
        )
        assert result["COUNTER"] == counter + 1
        assert result["RESULT"] == start_value + counter


"""
# old tests, referring to non static z-functions
#    def test_invalid_input(self):
#        self.conn.call('Z_PBR_EMPLOYEE_GET', IV_EMPLOYEE='100190', IV_USER_ID='')
#        self.conn.call('Z_PBR_EMPLOYEE_GET', IV_EMPLOYEE='', IV_USER_ID='HRPB_MNG01')
#        self.assertRaises(TypeError, self.conn.call, 'Z_PBR_EMPLOYEE_GET', IV_EMPLOYEE=100190, IV_USER_ID='HRPB_MNG01')
#
#    def test_xstring_output(self):
#        self.conn.call('Z_PBR_EMPLOYEE_GET_XSTRING', IV_EMPLOYEE='100190')
#
#    def test_xstring_input_output(self):
#        for i in 1, 2, 3, 1023, 1024, 1025:
#            s = 'X' * i
#            out = self.conn.call('Z_PBR_TEST_2', IV_INPUT_XSTRING=s)
#            self.assertEqual(s, out['EV_EXPORT_XSTRING'])

"""
if __name__ == "__main__":
    unittest.main()
