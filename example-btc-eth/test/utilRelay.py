import math
import logging
from functools import partial

from bitcoin import *

#
# helper functions for relayTx testing
#

def makeMerkleProof(header, hashes, txIndex):
    proof = mk_merkle_proof(header, hashes, txIndex)  # from pybitcointools

    txHash = int(proof['hash'], 16)
    siblings = map(partial(int,base=16), proof['siblings'])
    txBlockHash = int(proof['header']['hash'], 16)

    return [txHash, txIndex, siblings, txBlockHash]


def randomMerkleProof(blocknum, txIndex=-1, withMerkle=False):
    header = get_block_header_data(blocknum)
    hashes = get_txs_in_block(blocknum)

    numTx = len(hashes)
    if numTx == 0:
        print('@@@@ empty blocknum='+str(blocknum))
        return

    index = random.randrange(numTx) if txIndex == -1 else txIndex

    print('txStr='+hashes[index])

    proof = mk_merkle_proof(header, hashes, index)

    print('@@@@@@@@@@@@@@@@ blocknum='+str(blocknum)+'\ttxIndex='+str(index))

    txHash = int(hashes[index], 16)
    siblings = map(partial(int,base=16), proof['siblings'])
    txBlockHash = int(header['hash'], 16)

    ret = [txHash, index, siblings, txBlockHash]  # note: just 'index' here
    if withMerkle:
        ret.append(int(proof['header']['merkle_root'], 16))
    return ret


def dblSha256Flip(rawBytes):
    return int(bin_sha256(bin_sha256(rawBytes))[::-1].encode('hex'), 16)


def disablePyethLogging():
    logging.getLogger('eth.pb').setLevel('INFO')
    logging.getLogger('eth.pb.msg').setLevel('INFO')
    logging.getLogger('eth.pb.msg.state').setLevel('INFO')
    logging.getLogger('eth.pb.tx').setLevel('INFO')
    logging.getLogger('eth.vm').setLevel('INFO')
    logging.getLogger('eth.vm.op').setLevel('INFO')
    logging.getLogger('eth.vm.exit').setLevel('INFO')
    logging.getLogger('eth.chain.tx').setLevel('INFO')
    logging.getLogger('transactions.py').setLevel('INFO')
    logging.getLogger('eth.msg').setLevel('INFO')
