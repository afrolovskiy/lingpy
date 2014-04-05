# coding: utf-8
import math
import codecs
import nltk

stop_symbols = '.,;:?! -\'"'


def vlog(title, value=None, verbose=False):
    if not verbose:
        return

    print title

    if not value:
        return

    if hasattr(value, '__iter__'):
        for val in value:
            print val
    else:
        print value


def read_file(filename):
    with codecs.open(filename, encoding='utf-8') as fin:
        return fin.read()


def get_collocations(text, window, verbose=False, status=False):
    pairs = sorted(get_pairs(text, window, verbose, status))
    word_map1, word_map2 = construct_word_maps(pairs, verbose, status)
    pair_map = construct_pair_map(pairs, verbose, status)

    count = 0
    collocations = []
    upairs = set(pairs)
    for pair in upairs:
        fr1 = word_map1.get(pair[0], 0)
        fr2 = word_map2.get(pair[1], 0)
        fr = pair_map[pair]
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
            collocations.append((pair, t))
            vlog('added collocation:', (pair, t), verbose)

        vlog('pairs analysed {}%'.format(count / float(len(upairs)) * 100),
             verbose=status)
        count += 1

    return collocations


def get_pairs(text, window, verbose=False, status=False):
    pairs = []

    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_detector.tokenize(text.strip())
    vlog('sentences:', sentences, verbose)

    count = 0
    stemmer = nltk.stem.snowball.EnglishStemmer()
    for sentence in sentences:
        vlog('sentence:', sentence, verbose)

        words = nltk.PunktWordTokenizer().tokenize(sentence)

        # remove stop words
        words = [w for w in words if not w in
                 nltk.stem.snowball.stopwords.words('english')]

        # strip stop symbols
        words = [w.strip(stop_symbols) for w in words]

        # remove very short words
        words = [w for w in words if len(w) > 3]

        # normalize words
        words = map(stemmer.stem, words)
        vlog('words:', words, verbose)

        spairs = construct_pairs(words, args.window, args.verbose)

        # remove pairs with repeated words
        spairs = filter(lambda p: p[0] != p[1], spairs)

        pairs.extend(spairs)
        vlog('pairs:', spairs, verbose)

        vlog('sentences parsed {}%'.format(count / float(len(sentences)) * 100),
             verbose=status)
        count += 1

    return pairs


def construct_pairs(words, window, verbose=False):
    pairs = []
    for i1 in range(0, len(words)):
        for i2 in range(i1 + 1, min(len(words), i1 + window)):
            pairs.append((words[i1], words[i2]))
    vlog('pairs:', pairs, verbose)
    return pairs


def construct_word_maps(pairs, verbose=False, status=False):
    word_map1, word_map2 = {}, {}

    count = 0
    for pair in pairs:
        if pair[0] not in word_map1:
            word_map1[pair[0]] = 0
        word_map1[pair[0]] += 1

        if pair[1] not in word_map2:
            word_map2[pair[1]] = 0
        word_map2[pair[1]] += 1

        vlog('word maps builded {}%'.format(float(count) / len(pairs) * 100),
             verbose=status)
        count += 1

    return word_map1, word_map2


def construct_pair_map(pairs, verbose=False, status=False):
    pair_map = {}

    count = 0
    for pair in pairs:
        if pair not in pair_map:
            pair_map[pair] = 0
        pair_map[pair] += 1

        vlog('pair map builded {}%'.format(float(count) / len(pairs) * 100),
             verbose=status)
        count += 1

    return pair_map


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', help='increase output verbosity',
                        action='store_true')
    parser.add_argument('--status', help='print processing status',
                        action='store_true')
    parser.add_argument('--window', help='window length', type=int,
                        default=4, action='store')
    args = parser.parse_args()

    text = read_file(args.filename)
    collocations = get_collocations(text, args.window, args.verbose, args.status)
    vlog('collocations:', collocations, True)
