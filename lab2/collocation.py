# coding: utf-8
import math
import codecs
import nltk

stop_symbols = '.,;:?! -'

def vlog(title, value, verbose):
    if not verbose:
        return

    print title
    if hasattr(value, '__iter__'):
        for val in value:
            print val
    else:
        print value


def read_file(filename):
    with codecs.open(filename, encoding='utf-8') as fin:
        return fin.read()


def get_pairs(words, window, verbose=False):
    pairs = []
    for i1 in range(0, len(words)):
        for i2 in range(i1 + 1, min(len(words), i1 + window)):
            pairs.append((words[i1], words[i2]))
    vlog('pairs:', pairs, verbose)
    return pairs


def get_collocations(text, window, verbose=True):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_detector.tokenize(text.strip())
    vlog('sentences:', sentences, verbose)

    pairs = []
    stemmer = nltk.stem.snowball.EnglishStemmer()
    count = 0
    for sentence in sentences:
        vlog('sentence:', sentence, verbose)

        words = nltk.PunktWordTokenizer().tokenize(sentence)
        words = filter(lambda x: len(x) > 3, words)
        words = map(stemmer.stem, words)
        words = [w.strip(stop_symbols) for w in words]
        vlog('words:', words, verbose)

        pairs.extend(get_pairs(words, args.window, args.verbose))
        vlog('pairs:', pairs, verbose)

        print 'sentences parsed {}%'.format(count / float(len(sentences)) * 100)
        count += 1

    collocations = []
    count = 0
    for pair in set(pairs):
        fr1 = len(filter(lambda p: p[0] == pair[0] or p[1] == pair[0], pairs))
        fr2 = len(filter(lambda p: p[0] == pair[1] or p[1] == pair[1], pairs))
        fr = len(filter(lambda p: p == pair, pairs))
        vlog('pair={}:'.format(pair),
             'fr1={}, fr2={}, fr={}'.format(fr1, fr2, fr),
             verbose)

        smean = float(fr) / len(pairs)
        vlog('smean:', smean, verbose)

        h0 = float(fr1) * fr2 / len(pairs) / len(pairs)
        vlog('h0:', h0, verbose)

        t = (smean - h0) / math.sqrt(smean / len(pairs))
        vlog('t:', t, verbose)

        if t > 2.576:
            collocations.append(pair)

        print 'pairs analysed {}%'.format(count / float(len(pairs)) * 100)
        count += 1

    return collocations


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', help='increase output verbosity',
                        action='store_true')
    parser.add_argument('--window', help='window length', type=int,
                        default=10, action='store')
    args = parser.parse_args()

    text = read_file(args.filename)
    print 'collocations:', get_collocations(text, args.window, args.verbose)
