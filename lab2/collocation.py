# coding: utf-8
import math
import codecs
import nltk


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

    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_detector.tokenize(text.strip())
    import ipdb
    pairs = []
    gwords = []
    for sentence in sentences:
        print "sentence: ", sentence
        words = nltk.PunktWordTokenizer().tokenize(sentence)
        words = filter(lambda x: len(x) > 3, words)
        print 'words: ', words
        gwords.extend(words)
        # stemmer = nltk.stem.snowball.EnglishStemmer()
        # words = map(stemmer.stem, words)
        # print 'after stemmer: ', words

        pairs.extend(get_pairs(words, args.window, args.verbose))

    upairs = set(pairs)
    freq = {p: 0 for p in upairs}
    for p in pairs:
        freq[p] += 1

    print freq

    collocations = []
    for p in upairs:
        smean = float(freq[p]) / len(pairs)
        h0 = float(gwords.count(p[0])) * gwords.count(p[0]) / len(pairs) / len(pairs)
        t = (smean - h0) / math.sqrt(smean / len(pairs))
        if t > 2.576:
            collocations.append(p)

    print 'collocations: ', collocations