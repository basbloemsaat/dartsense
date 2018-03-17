

class List_C():

    def __init__(
            self,
            size=0,
    ):
        self.size = size
        self._elements = None

    def __iter__(self):
        self._pos = -1
        self._search()
        return self

    def __next__(self):
        self._pos += 1
        if self._pos < len(self._elements):
            return self._elements[self._pos]
        else:
            raise StopIteration

    # contract
    def _search(self):
        pass

    def _get_length(self):
        self._search()
        if self._elements == None:
            return 0
        return len(self._elements)

    def _get_elements(self):
        self._search()
        return self._elements

    def __getitem__(self,index):
        self._search()
        return self._elements[index]

    def __len__(self):
        return self.length

    length = property(_get_length)
    elements = property(_get_elements)


