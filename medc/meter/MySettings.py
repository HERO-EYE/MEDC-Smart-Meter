from gurux_dlms.enums import InterfaceType, Authentication, Security, Standard, Conformance
from gurux_dlms import GXDLMSClient
from gurux_dlms.secure import GXDLMSSecureClient
from gurux_dlms.GXByteBuffer import GXByteBuffer
from gurux_dlms.objects import GXDLMSObject
from gurux_common.enums import TraceLevel
from gurux_common.io import Parity, StopBits, BaudRate
#from gurux_net.enums import NetworkType
#from gurux_net import GXNet
from gurux_serial.GXSerial import GXSerial
from GXCmdParameter import GXCmdParameter
import os

class MySettings:
    #
    # Constructor.
    #
    def __init__(self):
        self.media = None
        self.trace = TraceLevel.INFO
        self.iec = False
        self.invocationCounter = None
        self.client = GXDLMSSecureClient(True)
        
        self.POWER   = "1.0.1.7.0.255:2"
        self.POWER_IMPORT   = "1.0.1.7.0.255:2"
        self.POWER_EXPORT   = "1.0.2.7.0.255:2"
        self.VOLTAGE = "1.0.0.6.4.255:2"
        self.KWH     = "1.0.15.8.0.255:2"
        self.DEVICEID_1 = "0.0.96.1.0.255:2"
        self.DEVICE_SN = "0.0.96.1.1.255:2"
        self.DEVICE_LDN = "0.0.42.0.0.255:2"
        self.BILL       = "0.0.98.1.0.255:2"
        self.BILL_CAPTURE = "0.0.98.1.0.255:3"
        self.DATE_TIME = "0.0.1.0.0.255:2"

    def Parameters(self):
        defaultBaudRate = True
        self.client.useLogicalNameReferencing = True
        #self.trace = TraceLevel.VERBOSE
        self.iec = False

        self.invocationCounter = "0.0.43.1.2.255"
        GXDLMSObject.validateLogicalName(self.invocationCounter)

        #dev_port = "/dev/ttyUSB0"
        print("Available serial ports:")
        print(GXSerial.getPortNames())
        #for PO in GXSerial.getPortNames():
        #    if ("ttyS1" in PO):
        #        dev_port = PO
        #        break
           
        dev_port = "/dev/ttyS1" 
        #os.system("sudo chown pi " + dev_port)
        self.media = GXSerial(None)
        self.media.port = dev_port
        #self.media.port = "/dev/ttyUSB0"
        self.media.baudrate = BaudRate.BAUD_RATE_9600
        self.media.bytesize = 8
        self.media.parity = Parity.NONE
        self.media.stopbits = StopBits.ONE

        self.client.authentication = Authentication.HIGH_GMAC
        self.client.settings.increaseInvocationCounterForGMacAuthentication = True
        self.client.ciphering.security = Security.AUTHENTICATION_ENCRYPTION

        self.client.ciphering.systemTitle = GXByteBuffer.hexToBytes("0F0E0D0C0B0A0908")
        self.client.ciphering.authenticationKey = GXByteBuffer.hexToBytes("D0D1D2D3D4D5D6D7D8D9DADBDCDDDEDF")
        self.client.ciphering.blockCipherKey = GXByteBuffer.hexToBytes("000102030405060708090A0B0C0D0E0F")
        self.client.ciphering.dedicatedKey = GXByteBuffer.hexToBytes("00112233445566778899AABBCCDDEEFF")
        self.client.ctoSChallenge = "00000001".encode()

        self.client.proposedConformance = Conformance.ACTION | Conformance.SELECTIVE_ACCESS | Conformance.SET | Conformance.GET | Conformance.MULTIPLE_REFERENCES | Conformance.BLOCK_TRANSFER_WITH_ACTION | Conformance.BLOCK_TRANSFER_WITH_SET_OR_WRITE | Conformance.BLOCK_TRANSFER_WITH_GET_OR_READ | Conformance.ATTRIBUTE_0_SUPPORTED_WITH_GET | Conformance.ATTRIBUTE_0_SUPPORTED_WITH_SET
        self.client.maxReceivePDUSize = 65535

        self.client.clientAddress = 2
        self.client.serverAddress = 144

        return 0
