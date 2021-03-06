
import os
import csv, codecs, cStringIO
from datetime import datetime, time

def setDates(startDate, endDate):
    # Set dates
    quarterStart = datetime.strptime(startDate, '%d %b %Y')
    quarterStart = datetime.combine(quarterStart.date(), time(00, 00, 00))
    quarterEnd = datetime.strptime(endDate, '%d %b %Y')
    quarterEnd = datetime.combine(quarterEnd.date(), time(23, 59, 59))
    return quarterStart, quarterEnd

def writeCSV(filename, data):
    
    file = open('output/'+filename, 'wb')
    file.write(codecs.BOM_UTF8)
    writer = UnicodeWriter(file, delimiter=',')
    
    # Write CSV column headings
    writer.writerow(data[0].keys())
    
    # Write rows
    for row in data:
        writer.writerow(row.values())

    file.close()
    return True

def touch(filename, times=None):
    with file(filename, 'a'):
        os.utime(filename, times)

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)