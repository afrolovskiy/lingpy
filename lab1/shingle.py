# coding:utf-8
import codecs
import binascii


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


def gen_shingle(text, shingle_len=10, verbose=False):
    vlog('source text:', text, verbose)

    source = canonize(text, verbose)
    vlog('canonized text:', source, verbose)

    shingles = []
    for i in range(len(source) - (shingle_len - 1)):
        line = u' '.join([x for x in source[i:i + shingle_len]])
        shingle = binascii.crc32(line.encode('utf-8'))
        shingles.append(shingle)

    vlog('shingles:', shingles, verbose)
    return shingles


def compare(source1, source2):
    same = 0
    for i in range(len(source1)):
        if source1[i] in source2:
            same = same + 1

    return same * 2 / float(len(source1) + len(source2)) * 100


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

    cmp1 = gen_shingle(text1, shingle_len=args.len, verbose=args.verbose)
    cmp2 = gen_shingle(text2, shingle_len=args.len, verbose=args.verbose)

    print compare(cmp1, cmp2)
