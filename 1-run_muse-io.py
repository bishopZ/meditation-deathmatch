#!/usr/bin/env python

import subprocess

cfg = {
    'dev': '00:06:66:68:8D:1B',
    'port': '5001',
    'ip': '127.0.0.1',
    'muse_path': '/opt/Muse/',
    'muse_cmd': 'muse-io'
}


def museio_cmd(cfg):
    cmd = cfg['muse_path'] + cfg['muse_cmd']
    cmd += ' --device ' + cfg['dev']
    cmd += ' --osc osc.tcp://' + cfg['ip'] + ':' + cfg['port']
    return cmd

return_code = subprocess.call(museio_cmd(cfg), shell=True)
