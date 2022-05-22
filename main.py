from functions import filter_labels
from functions import merge_all
from functions import print_potential_records, print_existing_record
from rich import print

from DockerApi import DockerApi
from CloudflareApi import CloudflareApi
from CloudflareApi import filter_valid_dns_records

cf = CloudflareApi()
d = DockerApi()

def process():
    r = dict()
    for container_name, labels in d.containers_labels().items():
        rr = dict()
        for label, value in filter_labels(labels):
            rr[label] = value
        merged = merge_all(rr)
        if merged:
            r[container_name] = merged

    for container_name, labels in r.items():
        print_potential_records(container_name, labels)
        dns_records = filter_valid_dns_records(list(labels.values()))
        for dns_record_data in dns_records:
            record = cf.build_dns_record(dns_record_data)
            existing = cf.find_existing_dns_record(record)
            if existing:
                print_existing_record(existing)
            else:
                cf.create_dns_record(record)

process()

for event in d.start_container_events():
    # reprocess all containers on any start event
    process()