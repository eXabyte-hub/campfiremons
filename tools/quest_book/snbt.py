"""Minimal reader/writer for FTB Quests' SNBT (tabs, newline-separated, unquoted keys)."""
import re

class Raw(str):
    """A bare token kept as written (numbers with suffixes, true/false)."""

TOKEN = re.compile(r'\s*(?:(?P<str>"(?:[^"\\]|\\.)*")|(?P<punct>[{}\[\]:,;])|(?P<bare>[^\s{}\[\]:,;"]+))', re.S)

def tokens(text):
    pos = 0
    while True:
        m = TOKEN.match(text, pos)
        if not m or m.end() == pos:
            rest = text[pos:].strip()
            if rest:
                raise ValueError(f"bad SNBT at {pos}: {rest[:40]!r}")
            return
        pos = m.end()
        if m.group('str') is not None:
            yield ('str', m.group('str'))
        elif m.group('punct') is not None:
            yield ('p', m.group('punct'))
        else:
            yield ('bare', m.group('bare'))

def unquote(s):
    return s[1:-1].replace('\\"', '"').replace('\\\\', '\\')

def parse(text):
    toks = list(tokens(text)); i = 0
    def value():
        nonlocal i
        kind, tok = toks[i]
        if kind == 'p' and tok == '{':
            i += 1; d = {}
            while not (toks[i] == ('p', '}')):
                if toks[i] == ('p', ','): i += 1; continue
                k_kind, k = toks[i]; i += 1
                key = unquote(k) if k_kind == 'str' else k
                assert toks[i] == ('p', ':'), toks[i]; i += 1
                d[key] = value()
            i += 1; return d
        if kind == 'p' and tok == '[':
            i += 1; lst = []
            if i + 1 < len(toks) and toks[i][0] == 'bare' and toks[i + 1] == ('p', ';'):
                prefix = toks[i][1]; i += 2; lst = TypedList(prefix)
            while not (toks[i] == ('p', ']')):
                if toks[i] == ('p', ','): i += 1; continue
                lst.append(value())
            i += 1; return lst
        i += 1
        return unquote(tok) if kind == 'str' else Raw(tok)
    v = value(); return v

class TypedList(list):
    def __init__(self, prefix): super().__init__(); self.prefix = prefix

def quote(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

KEY_OK = re.compile(r'^[A-Za-z0-9_.+\-]+$')

def dump(v, indent=0):
    t = '\t' * indent
    if isinstance(v, dict):
        if not v: return '{ }'
        lines = ['{']
        for k in sorted(v):
            key = k if KEY_OK.match(k) else quote(k)
            lines.append(f"{t}\t{key}: {dump(v[k], indent + 1)}")
        lines.append(t + '}')
        return '\n'.join(lines)
    if isinstance(v, TypedList):
        return f"[{v.prefix}; " + ', '.join(dump(x) for x in v) + ']'
    if isinstance(v, list):
        if not v: return '[ ]'
        if all(isinstance(x, dict) for x in v) and len(v) == 1:
            return '[' + dump(v[0], indent) + ']'
        return '[\n' + '\n'.join(t + '\t' + dump(x, indent + 1) for x in v) + '\n' + t + ']'
    if isinstance(v, Raw): return str(v)
    if isinstance(v, bool): return 'true' if v else 'false'
    if isinstance(v, int): return str(v)
    if isinstance(v, float): return f"{v}d"
    if isinstance(v, str): return quote(v)
    raise TypeError(type(v))
