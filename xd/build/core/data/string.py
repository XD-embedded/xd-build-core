import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .sequence import *


__all__ = ['String']


class String(Sequence):

    __slots__ = []

    basetype = str
    empty = ''

    def __str__(self):
        return self.get() or ''
