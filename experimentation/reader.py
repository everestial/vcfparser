
class file_reader:

    def __init__(self, file_name):

        self._file  = open(file_name, 'rt')
        self._curr = 0

    def reader(self):

        count = 5

        self._file.seek(self._curr)
        for line in self._file:
            count-=1
            print(line)
            self._curr = self._curr + len(line) + 1
            if count == 0:
                break
        

f = file_reader('sample1.txt')

f.reader()
f.reader()