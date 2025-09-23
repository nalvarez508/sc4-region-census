# uncompyle6 version 3.9.2
# Python bytecode version base 2.3 (62011)
# Decompiled from: Python 3.11.5 (v3.11.5:cce6ba91b3, Aug 24 2023, 10:50:31) [Clang 13.0.0 (clang-1300.0.29.30)]
# Embedded file name: sc4Dat.pyc
# Compiled at: 2004-01-25 21:38:17
from struct import *
import cStringIO
from array import array
stringDatID = 'DBPF'
stringDatHeader = '<4sLLLLLLLLLLLLLLLLLLLLLL'
stringIndexEntry = '<LLLLL'
stringDirectoryEntry = '<LLLL'
_DirectoryTGI = (3899334383L, 3899334383L, 678108931L)
lstIndexStruct = [
 9, 10, 11, 12, 13]
lstDirectoryStruct = [
 'typeID', 'groupID', 'instanceID', 'size']
_FH_IDENTIFIER = 0
_FH_VERSION_MAJOR = 1
_FH_VERSION_MINOR = 2
_FH_USER_VERSION_MAJOR = 3
_FH_USER_VERSION_MINOR = 4
_FH_OPTIONFLAGS = 5
_FH_CREATION_DATE = 6
_FH_MODIFIED_DATE = 7
_FH_INDEX_TYPE_VER = 8
_FH_INDEX_ENTRY_COUNT = 9
_FH_INDEX_LOCATION = 10
_FH_INDEX_SIZE = 11
_FH_HOLE_COUNT = 12
_FH_HOLE_LOCATION = 13
_FH_HOLE_SIZE = 14
_FH_RESERVED_1 = 15
_FH_RESERVED_2 = 16
_FH_RESERVED_3 = 17
_FH_RESERVED_4 = 18
_FH_RESERVED_5 = 19
_FH_RESERVED_6 = 20
_FH_RESERVED_7 = 21
_FH_RESERVED_8 = 22
_FH_RESERVED_9 = 23

class sc4DirectoryEntry:
    __module__ = __name__

    def __init__(self):
        self.typeID = 0
        self.groupID = 0
        self.instanceID = 0
        self.size = 0

    def __str__(self):
        return 'Type: %08X Group: %08X Instance: %08X Size: %12d' % (self.typeID, self.groupID, self.instanceID, self.size)


class sc4IndexEntry:
    __module__ = __name__

    def __init__(self):
        self.typeID = 0
        self.groupID = 0
        self.instanceID = 0
        self.location = 0
        self.size = 0

    def __str__(self):
        return 'Type: %08X Group: %08X Instance: %08X Location: %12d Size: %12d' % (self.typeID, self.groupID, self.instanceID, self.location, self.size)


class sc4Dat:
    __module__ = __name__
    fp = None

    def __init__(self, file):
        self.indexDir = {}
        self.directoryDir = {}
        self.header = []
        self.mode = 'rb'
        if isinstance(file, basestring):
            self._filePassed = 0
            self.filename = file
            self.fp = open(file, self.mode)
        else:
            self._filePassed = 1
            self.fp = file
            self.filename = getattr(file, 'name', None)
        self._readHeader()
        return

    def _readHeader(self):
        fp = self.fp
        fp.seek(0)
        header = unpack(stringDatHeader, fp.read(calcsize(stringDatHeader)))
        self.header = list(header)
        self._readIndex()

    def _readIndex(self):
        self.indexDir = {}
        fp = self.fp
        fp.seek(self.header[_FH_INDEX_LOCATION])
        for z in range(0, self.header[_FH_INDEX_ENTRY_COUNT]):
            entry = list(unpack(stringIndexEntry, fp.read(calcsize(stringIndexEntry))))
            ie = sc4IndexEntry()
            ie.typeID = entry[0]
            ie.groupID = entry[1]
            ie.instanceID = entry[2]
            ie.location = entry[3]
            ie.size = entry[4]
            self.indexDir[(ie.typeID, ie.groupID, ie.instanceID)] = ie

        if self.hasDirectory():
            dirInfo = self.indexDir[_DirectoryTGI]
            fp.seek(dirInfo.location)
            nEntries = dirInfo.size / calcsize(stringDirectoryEntry)
            for z in range(0, nEntries):
                entry = list(unpack(stringDirectoryEntry, fp.read(calcsize(stringDirectoryEntry))))
                de = sc4DirectoryEntry()
                de.typeID = entry[0]
                de.groupID = entry[1]
                de.instanceID = entry[2]
                de.size = entry[3]
                self.directoryDir[(de.typeID, de.groupID, de.instanceID)] = de

    def hasDirectory(self):
        return self.indexDir.has_key(_DirectoryTGI)

    def getRawData(self, typeID, groupID, instanceID):
        fp = self.fp
        key = (typeID, groupID, instanceID)
        if self.indexDir.has_key(key):
            fp.seek(self.indexDir[key].location)
            return fp.read(self.indexDir[key].size)

    def getDecompressedData(self, typeID, groupID, instanceID):
        fp = self.fp
        key = (typeID, groupID, instanceID)
        outbuf = array('B')
        outpos = 0
        if self.indexDir.has_key(key):
            if not self.directoryDir.has_key(key):
                return self.getRawData(typeID, groupID, instanceID)
            fp.seek(self.indexDir[key].location)
            inbuf = cStringIO.StringIO(fp.read(self.indexDir[key].size))
            inbuf.seek(0, 2)
            inbufLen = inbuf.tell()
            inbuf.seek(0)
            compSize = unpack('<L', inbuf.read(calcsize('<L')))[0]
            compSig = unpack('<H', inbuf.read(calcsize('<H')))[0]
            uncompSize = long(unpack('<B', inbuf.read(calcsize('<B')))[0]) << 16
            uncompSize += long(unpack('<B', inbuf.read(calcsize('<B')))[0]) << 8
            uncompSize += long(unpack('<B', inbuf.read(calcsize('<B')))[0])
            while inbuf.tell() < inbufLen:
                packcode = unpack('<B', inbuf.read(calcsize('<B')))[0]
                len1 = 0
                len2 = 0
                offset = 0
                if not packcode & 128:
                    len1 = packcode & 3
                    len2 = ((packcode & 28) >> 2) + 3
                    a = unpack('<B', inbuf.read(calcsize('<B')))[0]
                    offset = (packcode >> 5 << 8) + a + 1
                elif not packcode & 64:
                    a = unpack('<B', inbuf.read(calcsize('<B')))[0]
                    b = unpack('<B', inbuf.read(calcsize('<B')))[0]
                    len1 = a >> 6 & 3
                    len2 = (packcode & 63) + 4
                    offset = (a & 63) * 256 + b + 1
                elif not packcode & 32:
                    a = unpack('<B', inbuf.read(calcsize('<B')))[0]
                    b = unpack('<B', inbuf.read(calcsize('<B')))[0]
                    c = unpack('<B', inbuf.read(calcsize('<B')))[0]
                    len1 = packcode & 3
                    len2 = (packcode >> 2 & 3) * 256 + c + 5
                    offset = ((packcode & 16) << 12) + 256 * a + b + 1
                else:
                    len1 = (packcode & 31) * 4 + 4
                if len1 > 0:
                    s = inbuf.read(len1)
                    outbuf.fromstring(s)
                    outpos += len1
                if len2 > 0:
                    for z in range(0, len2):
                        outbuf.append(outbuf[outpos - offset + z])

                    outpos += len2

            outdata = outbuf.tostring()
            if len(outdata) != uncompSize:
                print 'Warning!  Uncompressed size incorrect!'
                print 'Should be %d, was %d' % uncompSize, len(outbuf.tostring())
            return outdata

    def __del__(self):
        self.close()

    def close(self):
        if self.fp == None:
            return
        if self._filePassed == False:
            self.fp.close()
        return


if __name__ == '__main__':
    _RegionViewTGI = (
     3389161179L, 3389161185L, 0L)
    t = sc4Dat('City - One.sc4')
    shell.clear()
    data = t.getDecompressedData(_RegionViewTGI[0], _RegionViewTGI[1], _RegionViewTGI[2])
    print len(data)
    fh = file('outpos', 'wb')
    fh.write(data)
    fh.close()
