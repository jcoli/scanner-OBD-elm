"""
Version: 0a
Tecnocoli - @04/2022
Author: Jeferson Coli - jcoli@tecnocoli.com.br
OBD2 test
conn_serial
"""
import obd
from obd import Unit, OBDResponse
from obd import ECU
from obd.protocols.protocol import Message
from obd.utils import OBDStatus
from obd.OBDCommand import OBDCommand
from obd.decoders import noop
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('scanner.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def odb_scan_serial(window):
    if len(obd.scan_serial()) == 0:
        return 0
    else:
        lports = obd.scan_serial()
        #print(lports)
        return lports


def odb_status_elm(window):
    return OBDStatus.ELM_CONNECTED


def odb_status_car(window):
    return OBDStatus.CAR_CONNECTED


def support_command(window, cmd):
    print("support ", cmd)
    return window.var1.connection.supports(cmd)


def obd_connect(window):

    if len(obd.scan_serial()) == 0:
        window.var1.obdConnect = False
    else:
        lports = obd.scan_serial()
        print(lports)
        try:
            # obd.logger.setLevel(obd.logging.DEBUG)
            window.var1.connection = obd.OBD()
            window.var1.connect_car = window.var1.connection.supports(obd.commands[1][0x0C])
            # self.connection = obd.OBD(protocol="8")
            logger.info('Connect')
            if OBDStatus.ELM_CONNECTED:
                if window.var1.connect_car:
                    obdConnect = True
                    if OBDStatus.CAR_CONNECTED:
                        print("Connected to the Car")

                    else:
                        print("Not connected to the Car")

                else:
                    window.var1.obdConnect = False
        except Exception as e:
            print("Problem trying connecting OBD-II adapter")
            print("Exception: " + str(e))
        finally:
            print('End OBD2 Connection')
        return window.var1.connection

    def query_odb(window, cmd):
        return window.var1.connection.query(cmd)

    def clear_dtc(window):
        try:
            if window.var1.obdConnect:
                window.var1.connection.query(obd.commands.CLEAR_DTC)
        except Exception as e:
            print('Connection Error: ', e)

    def reading_dtc(window):
        try:
            if obdConnect:
                # call_dtc = self.connection.query(obd.commands.GET_DTC)
                call_dtc = window.var1.connection.query(obd.commands[3][1])
                if not call_dtc.is_null():
                    return call_dtc
        except Exception as e:
            print("Connection Error ", e)