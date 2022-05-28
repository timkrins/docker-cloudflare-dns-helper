from functions import filter_labels
from functions import merge_all
from functions import print_potential_records, print_existing_record
from rich import print
from os import environ

from DockerApi import DockerApi
from CloudflareApi import CloudflareApi
from CloudflareApi import filter_valid_dns_records

cloudflare_api = CloudflareApi()
docker_api = DockerApi()

# can supply ENV variables for defaults
env_defaults = dict((k.replace("___", "-").replace("__", ".").lower(), v) for (k, v) in environ.items() if k.startswith("CLOUDFLARE___DNS"))
if env_defaults:
    print("Got env_defaults:")
    print(env_defaults)

container_cache = dict()

def process():
    merged_container_results = dict()
    for container_name, labels in docker_api.containers_labels().items():
        container_results = dict()
        for label, value in filter_labels(labels):
            container_results[label] = value
        for label, value in filter_labels(env_defaults):
            container_results[label] = value
        merged = merge_all(container_results)
        if merged:
            merged_container_results[container_name] = merged

    for container_name, labels in merged_container_results.items():
        container_labels_from_cache = container_cache.get(container_name, False)
        if container_labels_from_cache == labels:
            print("Skipping unchanged DNS configuration for {}".format(container_name))
            continue
        else:
            container_cache[container_name] = labels

        print_potential_records(container_name, labels)
        dns_records = filter_valid_dns_records(list(labels.values()))
        for dns_record_data in dns_records:
            record = cloudflare_api.build_dns_record(dns_record_data)
            existing = cloudflare_api.find_existing_dns_record(record)
            if existing:
                print_existing_record(existing)
            else:
                cloudflare_api.create_dns_record(record)

process()

for event in docker_api.start_container_events():
    # reprocess all containers on any start event
    process()