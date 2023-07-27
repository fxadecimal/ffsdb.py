# FFSDB: Flat-File System Database

![logo.png](logo.png)

I was gathering the requirements on a project and they said:

> "We don't want a database" 

So, _FFS DB_ was born:

It is a very simple key/value file system storage class that could be used while I extol the benefits of a database.

You can customise the read/write middleware easily. CSV was the original requirement, but released here with JSON as default.

Very heavily inspired by [SqliteDict](https://github.com/RaRe-Technologies/sqlitedict) & [tinydb](https://tinydb.readthedocs.io/en/latest/), both I would recommend over this!




## Quickstart

```python

from ffsdb import FFSdb

db = FFSdb(tablename="test2")
# creates directory ./ffsdb/test2
db['item1'] = {"hello":"there 1"}
# writes a file ./ffsdb/test2/item1
db[1] = {"hello":"there 2"}
# writes a file ./ffsdb/test2/1

for k,v in db.items():
    print("key:",k, "value:", v)

# key: 1 value: {'hello': 'there 2'}
# key: item1 value: {'hello': 'there 1'}

for k in db.keys():
    print("keys:",k)

# keys: 1
# keys: item1

for i in range(0,3):
    db[i] = {"hello":f"there {i}"}

for k,v in db.items():
    print("key:",k, "value:", v)

# key: 0 value: {'hello': 'there 0'}
# key: 1 value: {'hello': 'there 1'}
# key: item1 value: {'hello': 'there 1'}
# key: 2 value: {'hello': 'there 2'}

```

## Custom read / write methods

```py

import csv

def writer(obj, path):
    with open(path,'w') as f:
        c = csv.DictWriter(f, fieldnames=obj[0].keys(),delimiter='\t')
        c.writeheader()
        c.writerows(obj)
        

def reader(path):
    with open(path) as f:
        rows = csv.DictReader(f, delimiter='\t')
        return list(rows)

db = FFSdb(tablename="test4", reader=reader, writer=writer)
db['csv_item'] = [{"hello":"there","I like":"hats and cats"}]

```

# Inspiration

- [SqliteDict](https://github.com/RaRe-Technologies/sqlitedict)
- [tinydb](https://tinydb.readthedocs.io/en/latest/)
- [zodb](https://zodb.org/en/latest/)
- [SQLAlchemy](https://www.sqlalchemy.org/)



