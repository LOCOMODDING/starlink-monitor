"""
Use grpcurl to pull stats from the starlink router
"""
import os
import subprocess
import json


STARLINK_URI = os.getenv('STARLINK_URI', '192.168.100.1:9200')


def status():
    return _fetch('get_status')['dishGetStatus']


def history():
    h = _fetch('get_history')['dishGetHistory']
    # unroll circular buffers
    idx = int(h['current'])
    bufferlen = len(h['snr'])
    start = max(0, idx - bufferlen)
    unroll_idx = [
        i % bufferlen
        for i in range(start, idx)
    ]

    return {
        k: [v[idx] for idx in unroll_idx]
        for k, v in h.items()
        if k != 'current'
    }


def _fetch(cmd):
    return json.loads(
        subprocess.check_output(
            f'grpcurl -plaintext -d \'{{"{cmd}": {{}}}}\' {STARLINK_URI}  SpaceX.API.Device.Device/Handle',
            shell=True
        )
    )