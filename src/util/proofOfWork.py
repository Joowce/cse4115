import logging
import service.HashCalculator as HashCalculator
import time
import math


max_nonce = 2 ** 32


def proof_of_work(block_info, difficulty_bits, nonce_start, is_found):
    nonce = nonce_start
    # calculate the difficulty target
    target = 2 ** (256-difficulty_bits)

    logging.info("Target Value : ",hex(target))
    logging.info(" ")
    start_time = time.time()
    i = 1
    for nonce in range(nonce_start, max_nonce):
        if is_found():
            break

        hash_result = HashCalculator.get_hash(str(block_info)+str(nonce))
        if int(hash_result, 16) <= target:
            logging.info("Success with nonce %d" % nonce, "log2=", math.log(nonce,2))
            logging.info(" ")
            logging.info("Hash is %s" % hash_result)
            logging.info(" ")
            end_time = time.time()

            elapsed_time = end_time - start_time
            if elapsed_time > 0:
                # estimate the hashes per second
                hash_power = float(int(i) / elapsed_time)
                logging.info("Try %d" %i)
                logging.info("Hashing Power: %ld hashes per second" % hash_power)
            return hash_result, nonce, i
        i = i+1

    logging.info("Failed after %d (max_nonce) tries" % nonce)
    return None, nonce, -1


if __name__ == '__main__':
    block_hash, nonce_val, tries = proof_of_work('hello', 2, 0, lambda: False)
    print(block_hash)
