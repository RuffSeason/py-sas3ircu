from collections import namedtuple
import shlex
import subprocess
import os
import sys
from glob import iglob

def shell_exec(command, shell=False):
    """ Runs a shell command via subprocess module. Input is
    a string shell command. Function will split into list for
    you. Returns a named tuple with attributes of
    stdout | stderr | exitcode. """
    if shell:
        shexec = subprocess.Popen( command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=shell )
    else:
        cmd = shlex.split(command)
        shexec = subprocess.Popen( cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE )
    shout = shexec.communicate(), shexec.returncode
    stdout,stderr,exitcode = shout[0][0],shout[0][1],shout[1]
    resp = namedtuple("resp", ["stdout","stderr","exitcode"])
    return resp(stdout,stderr,exitcode)

def zfs_list_pools():
    cmd = "zpool list"
    resp = shell_exec(cmd)
    if resp.exitcode != 0:
        #TODO: Raise some shit
        return False
    lines = [l.split() for l in resp.stdout.splitlines()]
    headers,pools = lines[0],lines[1:]
    return [ dict(zip(headers,d)) for d in pools ]

def get_disk_device_map():
    mapdict = dict()
    for d in iglob('/dev/disk/by-id/*'):
        name = os.readlink(d).replace('../../', '/dev/')
        serial = d.split('/')[-1]
        if serial.startswith('wwn-') or "-part" in serial:
            continue
        else:
            mapdict[name] = serial
    return mapdict

def get_disk_serial_map():
    mapdict = dict()
    for d in iglob('/dev/disk/by-id/*'):
        serial = d.split('/')[-1]
        name = os.readlink(d).replace('../../', '/dev/')
        if serial.startswith('wwn-') or "-part" in serial:
            continue
        else:
            mapdict[serial] = name
    return mapdict

