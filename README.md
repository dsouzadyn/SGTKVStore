# SGTKVStore

A work-in-progress simple SGT(Set-Get-Truncate) in-memory Key-Value store server written in python.

## Requirements

- Python 3.7+

## Operations

```
SET <KEY> <VALUE>

GET <KEY>

TRUNCATE <KEY>
```

## Usage

- This script:

```sh
$ python kvstore.py 8888
```

- Client (netcat example):

```sh
$ nc localhost 8888
SET testkey 1
+OK

$ nc localhost 8888
GET testkey
1

$ nc localhost 8888
GET unknown_key
-ERROR

```

