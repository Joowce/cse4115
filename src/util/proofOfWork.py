import logging
import service.HashCalculator as HashCalculator
import time
import math


logger = logging.getLogger('monitoring')
max_nonce = 2 ** 32


def proof_of_work(block_info, difficulty_bits, nonce_start, is_found):
    nonce = nonce_start
    # calculate the difficulty target
    target = 2 ** (256-difficulty_bits)

    logger.info("log.Target Value : %s", hex(target))
    logger.info("log. ")
    start_time = time.time()
    i = 1
    for nonce in range(nonce_start, max_nonce):
        if is_found():
            break

        hash_result = HashCalculator.get_hash(str(block_info)+str(nonce))
        if int(hash_result, 16) <= target:
            logger.info("log.Success with nonce %d log2= %f", nonce, math.log(nonce,2))
            logger.info("log. ")
            logger.info("log.Hash is %s" % hash_result)
            logger.info("log. ")
            end_time = time.time()

            elapsed_time = end_time - start_time
            if elapsed_time > 0:
                # estimate the hashes per second
                hash_power = float(int(i) / elapsed_time)
                logger.info("log.Try %d" %i)
                logger.info("log.Hashing Power: %ld hashes per second" % hash_power)
            return hash_result, nonce, i
        i = i+1

    logger.info("log.Failed after %d (max_nonce) tries" % nonce)
    return None, nonce, -1


if __name__ == '__main__':
    block_hash, nonce_val, tries = proof_of_work('hello', 2, 0, lambda: False)
    print(block_hash)
