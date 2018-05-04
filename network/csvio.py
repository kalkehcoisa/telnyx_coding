import csv
import os


class CsvIo:
    '''
    Class to handle the all input/output of data from the csv files.
    '''

    def __init__(self, filename, from_default=True):
        if from_default:
            self.filepath = os.path.join(os.path.realpath(
                os.path.dirname(__file__)), 'data/', filename
            )
        else:
            self.filepath = os.path.join(os.path.realpath(filename))

    def __iter__(self):
        for item in self.data:
            yield item

    def __len__(self):
        return len(self.data)

    def sort(self, headers=None, reverse=False):
        if headers is None:
            headers = self.headers
        self.data = sorted(
            self.data,
            key=lambda row: [int(row[h]) for h in headers],
            reverse=reverse
        )
        return self

    @property
    def headers(self):
        return self.data.fieldnames

    def read(self):
        with open(self.filepath, 'r') as csvfile:
            self.data = csv.DictReader(csvfile.readlines())
        return self

    def write(self, filename=None, data=None, headers=None):
        with open(filename or self.filepath, 'w') as csvfile:
            output = csv.DictWriter(csvfile, fieldnames=headers or self.headers)
            output.writeheader()
            output.writerows(data or self.data)
        return self

    def create_file(self):
        with open(self.filepath, 'w'):
            pass
        return self
