import csv
import json
from pathlib import Path
from json import JSONEncoder


def glob_files_in(directory, matches=["*"]):
    directory = Path(directory).resolve()
    paths = []
    for match in matches:
        paths.extend(list(directory.glob(match)))
    return paths


def glob_directories_in(directory):
    paths = glob_files_in(directory)
    return [p for p in paths if p.is_dir()]


def writer_json(obj, path, cls=JSONEncoder, default=None):
    with open(path, "w") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False, default=default, cls=cls)


def reader_json(path):
    with open(path) as f:
        return json.load(f)


def writer_csv(obj, path):
    keys = obj[0].keys()

    with open(path, "w") as f:
        w = csv.DictWriter(
            f, fieldnames=keys, delimiter="\t", quotechar='"', quoting=csv.QUOTE_ALL
        )
        w.writeheader()
        w.writerows(obj)


def reader_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f, delimiter="\t", quotechar='"'))


class FFSdb(object):
    """

    A Lightweight Flat-file system database inspired by SQLiteDict & TinyDB

    - Doesn't attempt to hand-hold on key names, types & locks



    """

    def __init__(self, directory, reader=reader_json, writer=writer_json):
        self.path = Path(directory)
        self.reader = reader
        self.writer = writer
        self.path.mkdir(parents=True, exist_ok=True)

    def iter_files(self):
        for path in self.path.iterdir():
            if path.is_dir():
                continue
            yield path

    def iter_dirs(self):
        for path in self.path.iterdir():
            if not path.is_dir():
                continue
            yield path

    def items(self):
        for path in self.iter_files():
            yield path.stem, self.reader(path)

    def keys(self):
        for path in self.iter_files():
            yield path.stem

    def values(self):
        for k, v in self.items():
            yield v

    def get_key_path(self, key):
        return self.path.joinpath(str(key))

    def __getitem__(self, key):
        return self.reader(self.get_key_path(key))

    def __setitem__(self, key, value):
        self.writer(value, self.get_key_path(key))

    def __len__(self):
        return len(list(self.iter_files()))

    def __bool__(self):
        return len(self) >= 1

    def __delitem__(self, key):
        self.get_key_path(key).unlink()

    __iter__ = keys

    @classmethod
    def create_table_in(
        cls, directory, tablename="unamed", reader=reader_json, writer=writer_json
    ):
        directory = Path(directory).joinpath(tablename)
        return cls(directory=directory, reader=reader, writer=writer)

    @classmethod
    def create_tables_in(
        cls, directory, tablenames=["unamed"], reader=reader_json, writer=writer_json
    ):
        return [
            cls.create_table_in(
                tablename=tablename, directory=directory, reader=reader, writer=writer
            )
            for tablename in tablenames
        ]
