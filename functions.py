from rich.console import Console
from rich.table import Table

def dict_merge(a: dict, b: dict) -> dict:
    r = a
    for k, v in b.items():
        if k not in r:
            r[k] = v
    return r

def label_to_dict(k: str, v: any) -> dict:
    spl: list[str] = k.split('.')
    new_sub_k: str = spl.pop()
    new_k: str = '.'.join(spl)
    new_v: dict = { new_sub_k: v }
    return (new_k, new_v)

def merge_single_levels(a: dict) -> dict:
    r = dict()
    for k, v in a.items():
        kk, vv = label_to_dict(k, v)
        if kk not in r:
            r[kk] = vv
        else:
            r[kk] = dict_merge(r[kk], vv)
    return r

def merge_all(a: dict) -> dict:
    l = merge_single_levels(a)
    r = dict()
    for k, v in l.items():
        vv = v
        split_k = k.split('.')
        while len(split_k):
            split_k.pop()
            merge_key = '.'.join(split_k)
            if len(merge_key):
                vvv = l[merge_key]
                vv = dict_merge(vv, vvv)
        r[k] = vv
    return r

def filter_labels(a: dict) -> dict:
    r = list()
    for k, v in a:
        if k.startswith('cloudflare-dns'):
            r.append((k, v))
    return r

def print_potential_records(container_name: str, labels: dict) -> None:
    table = Table(title="Potential Records for {}".format(container_name))
    table.add_column("label")
    table.add_column("data")

    for k, v in labels.items():
        table.add_row(k, str(v))

    console = Console()
    console.print(table)

def print_existing_record(data: dict) -> None:
    table = Table(title="Existing DNS Record")
    table.add_column("label")
    table.add_column("data")

    for k, v in data.items():
        table.add_row(k, str(v))

    console = Console()
    console.print(table)