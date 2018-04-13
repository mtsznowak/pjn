import pickle
from collections import Counter
import math

def H(k):
    N = sum(k)
    q = [e / N * math.log(e/N if e/N != 0 else 1) for e in k]
    return sum(q)


if __name__ == "__main__":
    cfile = open('counter'+'.data','rb')
    (wordCounter, bigramCounter) = pickle.load(cfile)

    all_words = sum(wordCounter.values())
    all_bigrams = sum(bigramCounter.values())

    print("Najczęstrze bigramy:")
    print(bigramCounter.most_common(30))


    mpis = []

    for bigram in bigramCounter:
        p12 = bigramCounter[bigram] / all_bigrams
        (w1, w2) = bigram
        p1 = wordCounter[w1] / all_words
        p2 = wordCounter[w2] / all_words
        value = math.log(p12 / (p1*p2))
        mpis.append((value, bigram))

    mpis.sort(reverse=True)

    print("\n\nBigramy z najwięszkym MPI")
    print(mpis[:30])



    llrs = []
    for bigram in bigramCounter:
        (w1, w2) = bigram
        k11 = bigramCounter[bigram]
        k12 = wordCounter[w2] - k11
        k21 = wordCounter[w1] - k11
        k22 = all_bigrams - k11 - k12 - k21
        k = [k11, k12, k21, k22]
        kRowSums = [k11 + k12, k21 + k22]
        kColSums = [k11 + k21, k12 + k22]
        llr = 2 * all_bigrams * (H(k) - H(kRowSums) - H(kColSums))
        llrs.append((llr, bigram))


    llrs.sort(reverse=True)
    print("\n\nBigramy z największym LLR")
    print(llrs[:30])

    subst_occ = []

    i = 0
    while len(subst_occ) < 30:
        (_,(a,b)) = llrs[i]

        if a.split(':')[1] == 'subst' and b.split(':')[1] in ['adj', 'subst']:
            subst_occ.append(llrs[i])

        i = i+1

    print("\n\nPary z rzeczownikiem")
    print(subst_occ)










