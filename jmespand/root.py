import sys
if sys.version_info[0] < 3:
    _stringtype = basestring
    RecursionError = RuntimeError
else:
    _stringtype = str
    
from ._formatter import _Formatter

class JmespandRoot(object):
    def __init__(self):
        self._docs = []

    def add(self, doc, meta=None):
        if not JmespandRoot._isdict(doc):
            raise ValueError("Can only add dictionaries to a JmespandRoot")
        self._docs.append((doc, meta))

    def expanded(self, scope=None):
        ret = self._merged()
        if scope:
            rscope = dict(ret)
            rscope.update(scope)
        else:
            rscope = ret
        return self._expanded(ret, rscope)

    def _expanded(self, d, scope):
        if JmespandRoot._isdict(d):
            ret = {}
            for key, value in d.items():
                ret[key] = self._expanded(value, scope)
            return ret
        elif isinstance(d, _stringtype):
            if "{" in d:
                try:
                    return _Formatter(False).format(d, **scope)
                except RecursionError as exc:
                    ex = ValueError("Encountered cyclic definition when expanding '" + str(d) + "' " + JmespandRoot._getcontext(d))
                    if sys.version_info[0] < 3:
                        if "maximum recursion depth exceeded" in str(exc):
                            raise ex
                        else:
                            raise
                    else:
                        exec("raise ex from None", globals(), locals())
                except:
                    exctype, exc = sys.exc_info()[:2]
                    s = [''.join(exc.args), " when expanding '" + str(d)+ "'"]
                    v = JmespandRoot._getcontext(d)
                    if v: s.append(v)
                    ex = exctype(''.join(s))
                    
                    if sys.version_info[0] < 3:
                        raise ex
                    else:
                        exec("raise ex from exc", globals(), locals())

        if type(d).__name__ == '_Wrapped' and hasattr(d, '_meta'):
            return type(d).__base__(d)
        else:
            return d
    
    @staticmethod
    def _getcontext(d):
        s = []
        if hasattr(d, '_meta'):
            meta = d._meta
            if isinstance(meta, dict):
                keypath = meta.get("keypath")
                if keypath:
                    s.append("at " + str(keypath))

                for k, v in meta.items():
                    if k == "keypath": continue
                    if v:
                        s.append(str(k) + " " + str(filename))
        if not s:
            return ''
        return '(' + ', '.join(s) + ')'

    def _merged(self):
        d = {}
        for (doc, meta) in self._docs:
            JmespandRoot._deepmerge(d, doc, meta)
        return d

    @staticmethod
    def _deepmerge(dest, src, meta):
        def wrapvalue(val, meta=None):
            if meta is None:
                return val
            t = type(val)
            class _Wrapped(t):
                _meta = None
            wrapped = _Wrapped(val)
            wrapped._meta = meta
            return wrapped

        for key, value in src.items():
            if JmespandRoot._isdict(value):
                d = dest.get(key)
                if not isinstance(d, dict):
                    d = dest[key] = wrapvalue({})
                
                JmespandRoot._deepmerge(d, value, meta)
            else:
                dest[key] = wrapvalue(value, meta)

    @staticmethod
    def _isdict(val):
        if val is None: return False
        return hasattr(val, 'items') and hasattr(val, '__getitem__')


def create_root(*args):
    root = JmespandRoot()
    for arg in args:
        root.add(arg)
    return root