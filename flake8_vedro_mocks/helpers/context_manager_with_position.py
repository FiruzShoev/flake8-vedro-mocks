from collections import namedtuple

CtxManagerWithPosition = namedtuple('CtxManager', ('node', 'lineno', 'col_offset'))
