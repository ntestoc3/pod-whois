import datetime
import json
import logging
import sys
import traceback
from logging.handlers import RotatingFileHandler

import validators
import whois
from ipwhois import IPWhois
from retry import retry

import bcoding


def write(data):
    logging.info("write data: %s", data)
    sys.stdout.buffer.write(bcoding.bencode(data))
    sys.stdout.flush()

def read():
    r = bcoding.bdecode(sys.stdin.buffer)
    logging.info("read data: %s", r)
    return r

def format_nest_date(data):
    if isinstance(data, (datetime.date, datetime.datetime)):
        return data.isoformat()
    elif isinstance(data, list):
        return [format_nest_date(x) for x in data]
    elif isinstance(data, dict):
        return {k:format_nest_date(v) for k,v in data.items()}
    else:
        return data

@retry(Exception, delay=100, backoff=4, max_delay=280, tries=5)
def query(target):
    if validators.ipv4(target) or validators.ipv6(target):
        ip_whois = IPWhois(target)
        return ip_whois.lookup_rdap(asn_methods=["dns", "whois", "http"],
                                    inc_nir=True)
    elif validators.domain(target):
        result = whois.whois(target)
        return format_nest_date(result)
    else:
        logging.error(f"[whois query] not valid target: {target}")
        return None

lookup = {"pod.py-whois/query": query}

describe_map = {"format": "json",
                "namespaces": [{"name": "pod.py-whois",
                                "vars": [{"name": "query"}]}],
                "ops": {"shutdown": {}}}

logging.basicConfig(level=logging.WARN,
                    handlers=[
                        # RotatingFileHandler(filename=f"pod.whois_.log",
                        #                     maxBytes=5*1024*1024,
                        #                     backupCount=5),
                        logging.StreamHandler(sys.stderr)],
                    style="{",
                    format="{asctime} [{levelname}] {filename}({funcName})[{lineno}] {message}")

def main():
    while True:
        try:
            logging.info("start read.")
            msg = read()
            op = msg.get('op')
            id = msg.get('id', 'unknown')
            if op == 'describe':
                write(describe_map)
                continue
            elif op == 'invoke':
                var = msg.get('var')
                args = json.loads(msg.get('args'))
                f = lookup.get(var)
                try:
                    if f:
                        value = f(*args)
                        reply = {"value": json.dumps(value),
                                 "id": id,
                                 "status": ["done"]}
                        write(reply)
                    else:
                        raise Exception(f"Var not found: {var}")
                except Exception as e:
                    logging.error(f"error: {e}")
                    reply = {"ex-message": str(e),
                             "ex-data": json.dumps(None),
                             "id": id,
                             "status": ["done", "error"]}
                    write(reply)
                continue
            elif op == 'shutdown':
                sys.exit(0)
            else:
                write({"ex-message": "Unknown op",
                       "ex-data": json.dumps(op),
                       "id": id,
                       "status": ["done", "error"]})
                continue
        except Exception as e:
            logging.error(f"pod.py-whois exception:{e}" )
            return 1
