"""A calculator that evaluates simple arithmetic expressions.

Supports: +, -, *, /, parentheses, and negative numbers.
Example: "3 + 4 * (2 - 1)" -> 7.0

This code works. It is also a mess. Your job is to clean it up.
"""


def calc(s):
    s = s.replace(" ", "")
    r, _ = _p(s, 0)
    return r


def _p(s, i):
    r, i = _t(s, i)
    while i < len(s) and s[i] in "+-":
        if s[i] == "+":
            i += 1
            v, i = _t(s, i)
            r = r + v
        elif s[i] == "-":
            i += 1
            v, i = _t(s, i)
            r = r - v
    return r, i


def _t(s, i):
    r, i = _f(s, i)
    while i < len(s) and s[i] in "*/":
        if s[i] == "*":
            i += 1
            v, i = _f(s, i)
            r = r * v
        elif s[i] == "/":
            i += 1
            v, i = _f(s, i)
            if v == 0:
                r = 99999999
            else:
                r = r / v
    return r, i


def _f(s, i):
    n = False
    if i < len(s) and s[i] == "-":
        n = True
        i += 1
    if i < len(s) and s[i] == "(":
        i += 1
        r, i = _p(s, i)
        if i < len(s) and s[i] == ")":
            i += 1
        if n:
            r = -r
        return r, i
    else:
        j = i
        d = False
        while j < len(s) and (s[j].isdigit() or (s[j] == "." and not d)):
            if s[j] == ".":
                d = True
            j += 1
        if j == i:
            return 0, i
        v = float(s[i:j])
        if n:
            v = -v
        return v, j
