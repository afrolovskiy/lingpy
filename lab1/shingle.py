# coding:utf-8
import string
import random
import codecs
import binascii

from Crypto.Hash import HMAC


stop_symbols = '.,!?:;-\n\r()'

# TODO: read from file
stop_words = (
    u'это', u'как', u'так',
    u'и', u'в', u'над',
    u'к', u'до', u'не',
    u'на', u'но', u'за',
    u'то', u'с', u'ли',
    u'а', u'во', u'от',
    u'со', u'для', u'о',
    u'же', u'ну', u'вы',
    u'бы', u'что', u'кто',
    u'он', u'она'
)


def gen_secret(min_size=10, max_size=20, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(min_size, max_size))


def gen_secrets(secrets_len=84):
    return [gen_secret() for _ in range(secrets_len)]


def hashfunc(secret, text):
    hmac = HMAC.new(secret)
    hmac.update(text)
    # return binascii.crc32(hmac.hexdigest())
    return int(hmac.hexdigest(), 16)


def vlog(title, value, verbose):
    if not verbose:
        return

    print title
    if hasattr(value, '__iter__'):
        for val in value:
            print val
    else:
        print value


def canonize(text, verbose=False):
    words = [y.strip(stop_symbols) for y in text.lower().split()]
    vlog('words:', words, verbose)

    fwords = [x for x in words if x and (x not in stop_words)]
    vlog('filtered words:', words, verbose)

    return fwords


def get_shingles(text, shingle_len, verbose=False):
    source = canonize(text, verbose)

    shingles = []
    for i in range(len(source) - (shingle_len - 1)):
        shingle = u' '.join([x for x in source[i:i + shingle_len]])
        shingles.append(shingle)

    vlog('shingles:', shingles, verbose)
    return shingles



def gen_sketch(text, secrets, shingle_len=10, verbose=False):
    shingles = get_shingles(text, shingle_len, verbose)

    sketch = []
    for secret in secrets:
        hashes = []
        for shingle in shingles:
            hashes.append(hashfunc(secret, shingle.encode('utf-8')))
        sketch.append(min(hashes))

    vlog('sketch:', sketch, verbose)
    return sketch


def compare(sketch1, sketch2):
    same = 0
    for i in range(len(sketch1)):
        if sketch1[i] == sketch2[i]:
            same = same + 1
    return same / float(len(sketch1)) * 100


def read_file(filename):
    with codecs.open(filename, encoding='utf-8') as fin:
        return fin.read()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename1')
    parser.add_argument('filename2')
    parser.add_argument('--verbose', help='increase output verbosity',
                        action='store_true')
    parser.add_argument('--len', help='shingle length', type=int, default=3,
                        action='store')
    args = parser.parse_args()

    text1 = read_file(args.filename1)
    text2 = read_file(args.filename2)

    secrets = gen_secrets()

    sketch1 = gen_sketch(text1, secrets, shingle_len=args.len, verbose=args.verbose)
    sketch2 = gen_sketch(text2, secrets, shingle_len=args.len, verbose=args.verbose)

    print 'equals: {}%'.format(compare(sketch1, sketch2))
