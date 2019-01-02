import string
import jmespath
import sys
if sys.version_info[0] < 3:
    _stringtype = basestring
else:
    _stringtype = str

class _Formatter(string.Formatter):
    def __init__(self, quoted):
        super(_Formatter, self).__init__()
        self._quoted = quoted
        
    def get_field(self, field_name, args, kwargs):
        if field_name in kwargs:
            field_name = '"' + field_name + '"'
        v = jmespath.search(field_name, kwargs)
        if v is None:
            raise KeyError("Unable to resolve '" + field_name + "'")
        if isinstance(v, dict):
            raise ValueError("Not a scalar value")
        elif isinstance(v, list):
            v = (' '.join((self._resolve_recursive(x, kwargs) for x in v))).strip()
        elif v is None:
            v = ''
        elif isinstance(v, _stringtype):
            v = self._resolve_recursive(v, kwargs)
        else:
            v = str(v)
        if self._quoted:
            v = '"' + v + '"'
        return v, field_name

    def _resolve_recursive(self, s, scope):
        if "{" in s:
            return self.format(s, **scope)
        return s
        