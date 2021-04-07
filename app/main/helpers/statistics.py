# Knolist
# Conner Delahanty
# Spring 2020
#
# File contains helper methods for computing relevant
# database statistics. Principally an organizational
# construct to keep helper methods out of endpoint file.

from urllib.parse import urlparse
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np

def compute_cluster_stats(clusters, depth, n_items, n_clusters, sum_item_depth):
    """
    Computes max depth of a cluster. Performed using
    a recursive approach, where on each push to the
    call stack, statistics are updated and returned
    to earlier calls.
    """
    depths = [depth]  # Depths holds the depths of all clusters below this
    for c in clusters:
        n_clusters += 1
        n_items += len(c.child_items)
        sum_item_depth += len(c.child_items) * (depth + 1)  # Record the number of items * how deep it is nested
        d, n_items, n_clusters, sum_item_depth = compute_cluster_stats(
            c.child_clusters, depth + 1, n_items, n_clusters, sum_item_depth)
        depths.append(d)
    return max(depths), n_items, n_clusters, sum_item_depth



def compute_source_dist(sources):
    """
    Compute source type breakdown. Sources are considered
    unique up to the .com, .org, or .edu. Returns
    distribution in a dictionary.
    """
    dist = {}
    for src in sources:
        # # Find first occurrence of .edu, .com, .org
        # com_ind = src.url.find('.com')
        # org_ind = src.url.find('.org')
        # edu_ind = src.url.find('.edu')
        # ind = max(com_ind, org_ind, edu_ind)
        # # If none of above types, just skip
        # if ind == -1:
        #     continue
        # url_front = src.url[: ind + 4]
        try:
            domain = urlparse(src.url).netloc
            if domain in dist:
                dist[domain] += 1
            else:
                dist[domain] = 1
        except Exception:
            continue

    return dist


def dictdot(x, y):
    """
    Computes the dot product of vectors x and y, represented as sparse dictionaries.
    """
    keys = list(x.keys()) if len(x) < len(y) else list(y.keys())
    return sum(x.get(key, 0) * y.get(key, 0) for key in keys)


def cosine_sim(x, y):
    """
    Computes the cosine similarity between two sparse term vectors represented as dictionaries.
    """
    num = dictdot(x, y)
    if (num == 0):
        return 0
    return num / (np.linalg.norm(list(x.values())) * np.linalg.norm(list(y.values())))


def cosine_after_stopwords(text_a, text_b):
    """
    Computes the cosine similarity between two texts, after removing stopwords,
    all words of length < 3, and accounting for case. Used frequency vector
    ( weighted by number of words in each document)
    """
    stop_words = set(stopwords.words('english'))
    text_a_tok = word_tokenize(text_a)
    text_b_tok = word_tokenize(text_b)

    a_filt = [w.upper() for w in text_a_tok if not w in stop_words and len(w) >= 3]
    b_filt = [w.upper() for w in text_b_tok if not w in stop_words and len(w) >= 3]

    total = set(a_filt).union(set(b_filt))

    word_dict_a = dict.fromkeys(total, 0)
    word_dict_b = dict.fromkeys(total, 0)

    for word in a_filt:
        word_dict_a[word] += 1. / len(a_filt) # Frequency
    for word in b_filt:
        word_dict_b[word] += 1. / len(b_filt) # Frequency
    return cosine_sim(word_dict_a, word_dict_b)


def set_intersection_after_stopwords(text_a, text_b):
    """
    Compute the set intersection to determine naive measure of
    overlap between two documents.
    """
    stop_words = set(stopwords.words('english'))
    text_a_tok = word_tokenize(text_a)
    text_b_tok = word_tokenize(text_b)

    a_filt = set([w for w in text_a_tok if not w in stop_words and len(w) >= 3])
    b_filt = set([w for w in text_b_tok if not w in stop_words and len(w) >= 3])

    intersection = a_filt.intersection(b_filt)

    return len(intersection) / min(len(a_filt), len(b_filt))


def similarity(text_a, text_b):
    """
    Compute source similarity through hybrid approach of term intersection
    and word-frequency cosine similarity. Cos similarity has been given
    a smaller weight to counteract effects of large sloppy corpi.
    text_a and text_b are large strings representing two documents
    """
    stop_words = set(stopwords.words('english'))
    text_a_tok = word_tokenize(text_a)
    text_b_tok = word_tokenize(text_b)

    a_filt = [w.upper() for w in text_a_tok if not w in stop_words and len(w) >= 3]
    b_filt = [w.upper() for w in text_b_tok if not w in stop_words and len(w) >= 3]

    a_set = set(a_filt)
    b_set = set(b_filt)

    # Set intersection score
    intersection = a_set.intersection(b_set)
    set_score = len(intersection) / min(len(a_set), len(b_set))

    # Cosine score
    total = set(a_filt).union(set(b_filt))
    word_dict_a = dict.fromkeys(total, 0)
    word_dict_b = dict.fromkeys(total, 0)
    for word in a_filt:
        word_dict_a[word] += 1. / len(a_filt) # Frequency
    for word in b_filt:
        word_dict_b[word] += 1. / len(b_filt) # Frequency

    cos_score = cosine_sim(word_dict_a, word_dict_b)

    return 0.7 * set_score + 0.3 * cos_score
