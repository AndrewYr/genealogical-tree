# import copy
# from genealogical_tree.app.models import PersonModel
# from sqlalchemy.orm import Session
# from genealogical_tree.app.db import db_session
#
#
# @db_session(commit=False)
# def main(session: Session):
#     persons = session.query(PersonModel).order_by(PersonModel.columns.parent_id).all()
#     res = {}
#     for person in persons:
#
#         a = 1
#         # if person.parent_id:
#         #     a = session.query(PersonModel).filter(PersonModel.columns.family_id == person.parent_id).all()
#         #     person['parent'] = a
#     print(f'Hi, ')
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     main()

import string

# source = [
#     ('f0', 'f1'),
#     ('f1', 'f2'),
#     ('f10', 'f11'),
#     ('f2', 'f3'),
#     ('f3', 'f4'),
#     ('f4', 'f5'),
#     ('f5', 'f6'),
#     ('f6', 'f7'),
#     ('f7', 'f8'),
#     ('f8', 'f9'),
#     ('f9', 'f10')
# ]
    # [
    # (0, 1),
    # (1, 2),
    # (10, 11),
    # (2, 3),
    # (3, 4),
    # (4, 5),
    # (5, 6),
    # (6, 7),
    # (7, 8),
    # (8, 9),
    # (9, 10),
# ]

    # [
    # (None, 'a'),
    # (None, 'b'),
    # (None, 'c'),
    # ('a', 'a1'),
    # ('a', 'a2'),
    # ('a2', 'a21'),
    # ('a2', 'a22'),
    # ('b11', 'b111'),
    # ('b', 'b1'),
    # ('b1', 'b11'),
    # ('b', 'b2'),
    # ('c', 'c1'),
# ]

# for i in range(11):
#     source.append((i, i+1))

import re
import random

# def quicksort(nums):
#     if len(nums) <= 1:
#         return nums
#     else:
#         q = random.choice(nums)
#     l_nums = [n for n in nums if n < q]
#
#     e_nums = [q] * nums.count(q)
#     b_nums = [n for n in nums if n > q]
#     return quicksort(l_nums) + e_nums + quicksort(b_nums)

# for i in range(100):
#     source.append((f'q{i}', f'q{i+1}'))

source = [
    (None, 'a'),
    (None, 'b'),
    (None, 'c'),
    ('a', 'a1'),
    ('a', 'a2'),
    ('a2', 'a21'),
    ('a2', 'a22'),
    ('b11', 'b111'),
    ('b', 'b1'),
    ('b1', 'b11'),
    ('b', 'b2'),
    ('c', 'c1'),
]

expected = {
    'a': {
        'a1': {},
        'a2': {
            'a21': {},
            'a22': {}
        }
    },
    'b': {
        'b1': {
            'b11': {
                'b111': {}
            }
        },
        'b2': {}
    },
    'c': {
        'c1': {}
    },
}


def to_tree(source):
    list_source = []
    for k, v in source:
        if k is None:
            list_source.append((v, None))
        else:
            list_source.append((k, v))

    list_source.sort(key=lambda x: (x[0][0], 0 if len(x[0]) == 1 else int(x[0][1:])))

    result = {}
    for k, v in list_source[::-1]:
        if v:
            if v in result.keys():
                if k in result.keys():
                    result[k].update({v: result.pop(v)})
                else:
                    result[k] = {v: result.pop(v)}
            else:
                if k in result.keys():
                    result[k].update({v: {}})
                else:
                    result[k] = {v: {}}
        else:
            if k not in result.keys():
                result[k] = {}
    return result


assert to_tree(source) == expected


def remove_redundant(source, waste=None) -> list:
    """ Remove elements with None from source list """
    for el in source[:]:
        x, y = el
        if x is waste:
            source.remove(el)
    source.sort(key=lambda x: (x[0][0], 0 if len(x[0]) == 1 else int(x[0][1:])))
    # print(source)
    return source


def list2tree(source) -> dict:
    old = ('', '')
    tree = {}
    for el in source[::-1]:
        key, val = el
        old_key, old_val = old
        # print('new:', el, old)
        if len(tree) == 0 or key[0] not in old_key:
            # print('add new branch: ', end='')
            tree[key]={val: {}}
        else:
            if key != old_key:
                if val == old_key:
                    # print('rise: ', end='')
                    rise = {val: tree[val]}
                    del tree[val]
                    tree[key] = rise
                else:
                    # print('fork: ', end='')
                    fork = tree[old_key]
                    del tree[old_key]
                    tree[key] = {val: {}, old_key: fork}
            else:
                if val not in tree[key].keys():
                    # print('rise fork: ', end='')
                    fork = tree[key][old_val]
                    del tree[key]
                    tree[key] = {val: {}, old_val: fork}
        old = el
        # print(tree, 'step')
    return tree


def to_tree_1(source):
    source = remove_redundant(source)
    return list2tree(source)
# def to_tree(source):
#     res = {}
#     for k, v in source[::-1]:
#         for k_1, v_1 in source:
#             if v == k_1:
#                 if v in res.keys():
#                     res[v].update({v_1: res.pop(v_1, {})})
#                 elif v_1 in res.keys():
#                     res[v] = {v_1: res.pop(v_1)}
#                 else:
#                     res[v] = {v_1: {}}
#
#     return res


expected = {
    'a': {
        'a1': {},
        'a2': {
            'a21': {},
            'a22': {}
        }
    },
    'b': {
        'b1': {
            'b11': {
                'b111': {}
            }
        },
        'b2': {}
    },
    'c': {
        'c1': {}
    },
}


# def get_tree(source):
#     last = ('', '')
#     result = {}
#
#     for el in source[:]:
#         if el[0] is None:
#             source.remove(el)
#             result[el[1]] = {}
#     source.sort()
#
#     for el in source[::-1]:
#         k, v = el
#         last_key, last_val = last
#
#         if k not in last_key:
#             result[k] = {v: {}}
#         else:
#             if k != last_key:
#                 if v == last_key:
#                     rise = {v: result[v]}
#                     result.pop(v)
#                     result[k] = rise
#                 else:
#                     fork = result[last_key]
#                     result.pop(last_key)
#                     result[k] = {v: {}, last_key: fork}
#             else:
#                 if v not in result[k].keys():
#                     fork = result[k][last_val]
#                     result.pop(k)
#                     result[k] = {v: {}, last_val: fork}
#         last = el
#     return result


import sys
from datetime import datetime
# print(sys.getsizeof(to_tree(source)))
# print(sys.getsizeof(to_tree_1(source)))

# start_time = datetime.now()
# to_tree(source)
# end_time = datetime.now()
# print('Duration: {}'.format(end_time - start_time))
#
start_time = datetime.now()
to_tree_1(source)
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

# print("--- %s seconds ---" % (time.clock() - start_time))
# assert to_tree(source) == expected
