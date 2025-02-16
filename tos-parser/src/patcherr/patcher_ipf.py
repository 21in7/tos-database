import logging
import os
import shutil
import subprocess

import constants
from utils import fileutil

IPF_BLACKLIST = [
    'animation.ipf',
    'bg_hi.ipf',
    'bg_hi2.ipf',
    'bg_hi3.ipf',
    'bg_lightcell.ipf',
    'bg_texture.ipf',
    'char_hi.ipf',
    'char_texture.ipf',
    'char_texture_low.ipf',
    'deadslice.ipf',
    'decal.ipf',
    'effect.ipf',
    'etc.ipf',
    'item_hi.ipf',
    'item_texture.ipf',
    'item_texture_low.ipf',
    'shader.ipf',
    'sound.ipf',
    'sprite.ipf',
    'SumAni.ipf',
    'templatepc.ipf',
]


def unpack(ipf):
    ipf = os.path.join(constants.PATH_INPUT_DATA_PATCH, ipf)
    ipf_extract = os.path.join(os.path.dirname(ipf), 'extract')
    ipf_revision = os.path.basename(ipf)[:-4]
    logging.debug('Unpacking %s...', ipf)

    # Decrypt and extract ipf file
    if ipf_revision not in ['29_001001']:  # HotFix: these specific patches aren't encrypted for some reason
        subprocess.check_call(
            [constants.PATH_UNPACKER_EXE, ipf, "decrypt"],
            stdin=None, stdout=None, stderr=None, shell=False
        )
    subprocess.check_call(
        [constants.PATH_UNPACKER_EXE, ipf, "extract"],
        stdin=None, stdout=None, stderr=None, shell=False
    )

    if os.path.exists(ipf_extract):
        # Remove blacklisted IPF files from extracted result
        for file_name in os.listdir(ipf_extract):
            if any(file_name == s for s in IPF_BLACKLIST):
                shutil.rmtree(os.path.join(ipf_extract, file_name))

        # Make all files lower case
        fileutil.to_lower(ipf_extract)

        # Move extracted IPF files to data directory
        fileutil.move_tree(ipf_extract, constants.PATH_INPUT_DATA)

        # Remove extract directory
        shutil.rmtree(ipf_extract)
