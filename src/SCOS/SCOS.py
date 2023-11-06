#!/usr/bin/env python3
import datetime

from bitstring import BitArray, BitStream

__version__ = "0.4.5"

accessFlag = {
    0: {'code': 0, 'description': "Inserted Packet"},
    1: {'code': 1, 'description': "Updated"},
}
simFlag = {
    0: {"flag": "00", "description": "Not Simulated Packet"},
    1: {"flag": "01", "description": "Simulated Packet"}
}
SpacecraftID = {
    816: {
        'id': 816,
        "Spacecraft": "BepiColombo",
        "Band": "X-Band"
    },
    817: {
        'id': 817,
        "Spacecraft": "BepiColombo",
        "Band": "Ka-Band"
    },
}
groundStation = {
    21: {'id': 21, 'station': "Kourou"},
    22: {'id': 22, 'station': "Perth"},
    23: {'id': 23, 'station': "New Norcia"},
    24: {'id': 24, 'station': "Cebreros"},
    25: {'id': 25, 'station': "Malargue"},
    30: {'id': 30, 'station': "Maspalomas"},
    97: {'id': 97, 'station': "Usuda"},
    98: {'id': 98, 'station': "Uchinoura"},
}
PacketType = {
    1: {'id': 1, 'description': "Telemetry Packet"},
    2: {'id': 2, 'description': "Telecommand Packet"},
    3: {'id': 3, 'description': "Event Packet"},
}
FilingFlag = {
    0: {'id': 0, 'description': "Packet not filed in MSC archive"},
    1: {'id': 1, 'description': "Packet filed in MSC archive"},
}
DistFlag = {
    0: {'id': 0, 'description': "Packet is not to be distributed to the MSC application"},
    1: {'id': 1, 'description': "Packet is to be distributed to the MSC application"},
}
TsPolicy = {
    0: {'id': 0, 'description': "Packet timestamped with creation time"},
    1: {'id': 1, 'description': "Packet timestamped with frame recived time"},
    2: {'id': 2, 'description': "Packet timestamped with SCET"},
}
timeQuality = {
    0: {'id': 0, 'description': "Good"},
    1: {'id': 1, 'description': "Inaccurate"},
    2: {'id': 2, 'description': "Bad"},
}
StreamID = {
    1: {'id': 1, 'description': "Telecommand Stream"},
    1000: {'id': 1000, 'description': "VC0 Real-Time Non-Science or Events (online)"},
    1001: {'id': 1001, 'description': "VC1 Playback Non-Science or Events (online)"},
    1002: {'id': 1002, 'description': "VC2 Science (online)"},
    1003: {'id': 1003, 'description': "VC3 File-Transfer (online)"},
    2000: {'id': 2000, 'description': "VC0 Real-Time Non-Science or Events (offline)"},
    2001: {'id': 2001, 'description': "VC1 Playback Non-Science or Events (offline)"},
    2002: {'id': 2002, 'description': "VC1 Playback Non-Science or Events (offline)"},
    2003: {'id': 2003, 'description': "VC2 Science (offline)"},
    65535: {'id': 65535, 'description': "Internal non Spacecraft Telemetry"},
}
MissionID = {
    816: {'id': 816, 'description': "BepiColombo"},
    0:  {'id': 0, 'description': "Not Decode"},
}
DataUnitType = {
    0: {'id': 0, 'description': "TM Transfer Frame"},
    1: {'id': 1, 'description': "TM Source Packet"},
    2: {'id': 2, 'description': "Internal MCS TM Packet"},
}
Qualifier = {
    '0': {'id': 0, 'description': "Good"},
    '1': {'id': 1, 'description': "Good"},
    '2': {'id': 2, 'description': "CLCW"},
    '10': {'id': 10, 'description': "Bad"},
    '11': {'id': 11, 'description': "Bad"},
    '12': {'id': 12, 'description': "User Defined Constant"},
    '20': {'id': 20, 'description': "Idle"},
    '21': {'id': 21, 'description': "Idle"},
    '22': {'id': 22, 'description': "Status Consistency Check"},
    '32': {'id': 32, 'description': "Dynamic Misc"},
    '42': {'id': 42, 'description': "Online MIB changes"},
    '52': {'id': 52, 'description': "SPPG"},
    '62': {'id': 62, 'description': "SPID Validity"},
    '72': {'id': 72, 'description': "TPKT Configuration"},
    '82': {'id': 82, 'description': "External Source"},
}


def Time(sec, mlsec):
    return datetime.datetime(1970, 1, 1, 0, 0, 0, 0)+datetime.timedelta(seconds=sec)+datetime.timedelta(microseconds=mlsec)


class SCOS:
    __version__ = "0.4.5"
    def __init__(self, data):
        self.CPH = SCOS_CPH(data[0:120])
        if self.CPH.PType['id'] == 1:
            self.TMPH = SCOS_TMPH(data[120:152])
            self.Data = data[152:]
        elif self.CPH.PType['id'] == 2:
            self.TCPH = SCOS_TCPH(data[120:208], self.CPH.SeqCounter)
            self.Data = data[208:]
        #     c = BitArray(hex=hexdata[208:])
        #     self.SPH=SPHeader(c[:48])
        #     self.SPH=SPHeader_new(hexdata[208:220])
        #     self.Data=TelecommandData(hexdata)
        else:
            print("Not Decoded")


class SCOS_TCPH:
    def __init__(self, data, SSC):
        # 0: Uplink seconds, 1: Uplink milliseconds, 2: Execution seconds, 3: Execution milliseconds
        # 4: Last update seconds, 5: Last Update milliseconds, 6: Request ID, 7: Request Element Index
        # 8: Variable address size, 9: PUS APID, 10: PUS SSC, 11: PUS Service Type, 12: PUS SunbService Type
        # 13: PUS Ack Flag, 14: Uplink Flag, 15: Source Host, 16: Source Type, 17: Request Detail Fixed Size
        dp = BitStream(hex=data).unpack(
            7*'uint:32,'+4*'uint:16,'+6*'uint:8,'+'uint:16')
        self.UplinkTime = Time(*dp[0:2])
        self.ExecTime = Time(*dp[2:4])
        self.LUTime = Time(*dp[4:6])
        self.RequestID = dp[6]
        self.ReqElemIdx = dp[7]
        self.VarAddSz = dp[8]
        self.PUSAPID = dp[9]
        self.PUSSSC = dp[10]
        self.PID, self.PCAT = BitStream(hex=data[64:68]).unpack(2*'uint:8,')
        self.PUSService = dp[11]
        self.PUSST = dp[11]
        self.PUSSubService = dp[12]
        self.PUSSST = dp[12]
        self.PUSAck = dp[13]
        self.UplinkFlag = dp[14]
        self.SourceHost = dp[15]
        self.SourceType = dp[16]
        self.ReqDetFixedSize = dp[17]


class SCOS_CPH:
    def __init__(self, data):
        # 0: cTree, 1: AccessFlag, 2: Spere, 3: SimFlag, 4: Filling Time seconds, 5: Filling Time milliseconds
        # 6: Creation Time seconds, 7: Creation Time milliseconds, 8: Create ID, 9: Spacecraft ID, 10: GroundStation
        # 11: Size of the packet, 12: Packet Type, 13: Version, 14-15: spere, 16: Filing Flag, 17: Distributed Flag
        # 18: Timestamp policy, 19: Time quality, 20: stream ID, 21 Sequence Counter, 22: SPID, 23 Retr key 1,
        # 24 Retr Key 2, 25: Mission ID, 26: Context ID, 27: Domain ID, 28: DB Rel, 29: DB Iss, 30: Spere
        dp = BitStream(hex=data[0:120]).unpack('bytes:2,uint:8,uint:6, uint:2,'+5*'uint:32,'+2 *
                                               'uint:16,'+'uint:32,'+2*'uint:4,'+4*'uint:1,'+2*'uint:2,'+'uint:16,'+2*'uint:32,'+8*'uint:16,')
        self.CTree = dp[0]
        self.AccessF = accessFlag[dp[1]]
        self.SimFlag = simFlag[dp[3]]
        self.FilingTime = Time(dp[4], dp[5])
        self.CreationTime = Time(dp[6], dp[7])
        self.CreateID = dp[8]
        if dp[9] in SpacecraftID:
            self.SCID = SpacecraftID[dp[9]]
        else:
            self.SCID = {
                'id': dp[9], "Spacecraft": "Not in DB", "Band": "Not in DB"}
        if dp[10] in groundStation:
            self.GSID = groundStation[dp[10]]
        else:
            self.GSID = {'id': dp[10], 'station': "Not in DB"}
        self.PSize = dp[11]
        self.PType = PacketType[dp[12]]
        self.Version = dp[13]
        self.FilingFlag = FilingFlag[dp[16]]
        self.DistFlag = DistFlag[dp[17]]
        self.TSPolicy = TsPolicy[dp[18]]
        self.TQ = timeQuality[dp[19]]
        self.StreamID = StreamID[dp[20]]
        self.SeqCounter = dp[21]
        self.SPID = dp[22]
        if dp[25] in MissionID:
            self.MissionID = MissionID[dp[25]]
        else:
            self.MissionID = {'id': dp[25], "description": "Not in DB"}
        self.MIB = f"{dp[28]}.{dp[29]}"


class SCOS_TMPH:
    def __init__(self, data):
        # 0: Not Used, 1: TPSD, 2: Unused, 3: data Unit Type, 4: Quealifier, 5: APID, 6: SSC
        # 7: PUS Service, 8: PUS SubService
        dp = BitStream(hex=data).unpack(2*'uint:32,'+'uint:8,' +
                                        2*'uint:4,'+2*'uint:16,'+2*'uint:8,')
        self.TPSD = dp[1]
        self.RouteID = {'DataUnitType': DataUnitType[dp[3]], 'Qualifier': Qualifier[str(
            dp[4])]}  # RouteID(data[16:20])
        self.PUSAPID = dp[5]
        self.PUSSSC = dp[6]
        self.PUSService = dp[7]
        self.PUSSubService = dp[8]
        self.PUSST = dp[7]
        self.PUSSST = dp[8]
