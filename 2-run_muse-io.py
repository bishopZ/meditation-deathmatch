#!/usr/bin/env python

import platform
import subprocess

cfg = {
    'dev': '00:06:66:70:6C:94',
    'port': '5002',
    'ip': '127.0.0.1',
    'muse_path': '/opt/Muse/',
    'muse_cmd': 'muse-io'
}

if (platform.system() == 'Darwin'):
    cfg['muse_path'] = '/Applications/Muse/'
    cfg['dev'] = 'MuseD'


def museio_cmd(cfg):
    cmd = cfg['muse_path'] + cfg['muse_cmd']
    cmd += ' --device ' + cfg['dev']
    cmd += ' --osc osc.tcp://' + cfg['ip'] + ':' + cfg['port']
    return cmd


return_code = subprocess.call(museio_cmd(cfg), shell=True)
