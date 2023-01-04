import os
import sys
import csv
import logging
import collections

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stderr))
log.setLevel(logging.WARNING)

def csv_reader_converter(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [cell for cell in row]

def csv_writer(filename, data, fields=None, delimiter=',', quoting=csv.QUOTE_MINIMAL):
    log.info('writing %s' % filename)
    rows = 0
    with open(filename, 'w') as f:
        if not fields:
            fields = data[0].keys()
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=delimiter, quoting=quoting)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
            rows += 1
    log.info('wrote %d rows' % rows)

def load_csv_columns(filename, column_names=None, skip=0, delimiter=',', quoting=csv.QUOTE_MINIMAL):
    r = []
    log.info('opening %s' % filename)
    try:
        with open(filename, 'r') as f:
            data_file = csv_reader_converter(f, delimiter=delimiter, quoting=quoting)
            for i in range(skip):
                next(data_file)
            headers = next(data_file, None)  # parse the headers
            columns = {}
            for (i, h) in enumerate(headers):
                h = h.strip()
                if (not column_names) or h in column_names:
                    columns[i] = h
            log.info("headers %s " % headers)
            log.info("columns %s" % column_names)

            for line in data_file:
                d = {}
                if not line:
                    continue
                for (column, index) in columns.items():
                    if column_names:
                        rename = column_names[index]
                    else:
                        rename = headers[column]
                    value = line[column].strip()
                    d[rename] = value
                r.append(d)
            log.info('read %d lines' % len(r))
            return r
    except FileNotFoundError:
        log.warning(f"unable to find {filename}")
        return []

def list_key_set(data, key):
    s = set()
    for d in data:
        try:
            s.add(d[key])
        except KeyError:
            print(d)
            break
    return s

def list_key_values(data, key):
    c = collections.defaultdict(list)
    for d in data:
        try:
            c[d[key]].append(d)
        except KeyError:
            print(d)
            break
    return c
