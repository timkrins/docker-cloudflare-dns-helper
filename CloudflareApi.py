import CloudFlare

def filter_valid_dns_records(dns_records: list[dict]):
    r = list()
    for i in dns_records:
        valid = True
        # ensure we have a minimum level of values
        if 'name' not in i or not i['name']:
            valid &= False
        if 'content' not in i or not i['content']:
            valid &= False
        if 'type' not in i or not i['type']:
            valid &= False
        if valid:
            r.append(i)
    return r

class CloudflareApi:
    def __init__(self):
        self.cf = CloudFlare.CloudFlare()
        self.zones_cache = dict()
        self.zone_dns_records_cache = dict()

    def zones(self) -> list[dict]:
        return self.cf.zones.get(params = {'per_page': 100})

    def zone(self, zone_name: str) -> dict:
        if zone_name in self.zones_cache:
            return self.zones_cache[zone_name]
        return self.lookup_zone(zone_name)

    def lookup_zone(self, zone_name: str) -> dict:
        # query for the zone name and expect only one value back
        try:
            zones = self.cf.zones.get(params = {'name':zone_name,'per_page':1})
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zones.get %d %s - api call failed' % (e, e))
        except Exception as e:
            exit('/zones.get - %s - api call failed' % (e))
        if len(zones) == 0:
            exit('No zones found')
        z = zones[0]
        self.zones_cache[zone_name] = z
        return z

    def zone_dns_records(self, zone_id: str) -> list[dict]:
        if zone_id in self.zone_dns_records_cache:
            return self.zone_dns_records_cache[zone_id]
        return self.get_dns_records_for_zone(zone_id)

    def get_dns_records_for_zone(self, zone_id: str) -> list[dict]:
        # request the DNS records from that zone
        try:
            dns_records = self.cf.zones.dns_records.get(zone_id)
            self.zone_dns_records_cache[zone_id] = dns_records
            return dns_records
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zones/dns_records.get %d %s - api call failed' % (e, e))

    def create_dns_record(self, new_dns_record: dict) -> dict:
        try:
            zone_id = new_dns_record.pop('zone_id')
            dns_record = self.cf.zones.dns_records.post(zone_id, data=new_dns_record)
            return dns_record
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zones.dns_records.post %s %s - %d %s' % (zone_name, dns_record['name'], e, e))

    def update_dns_record(self, update_dns_record: dict) -> dict:
        try:
            zone_id = update_dns_record.pop('zone_id')
            dns_record_id = update_dns_record.pop('id')
            dns_record = self.cf.zones.dns_records.put(zone_id, dns_record_id, data=update_dns_record)
            return dns_record
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zones/dns_records.put %d %s - api call failed' % (e, e))

    def find_existing_dns_record(self, data: dict) -> dict:
        if 'zone_id' in data:
            existing_records = self.zone_dns_records(data['zone_id'])
            matching_records = list()
            for e in existing_records:
                if 'name' in e and 'name' in data and e['name'] == data['name']:
                    matching_records.append(e)
            if len(matching_records) == 0:
                return None
            elif len(matching_records) == 1:
                return matching_records[0]
            else:
                exit('too many records for this dns match value')

    def build_dns_record(self, data: dict) -> dict:
        dns_record = dict()
        # find zone if it exists
        if 'zone_id' in data:
            dns_record['zone_id'] = data['zone_id']
        elif 'zone_name' in data:
            # lookup zone id
            zone = self.zone(data['zone_name'])
            if zone:
                dns_record['zone_id'] = zone['id']
        else:
            exit('no zone')

        if 'name' in data:
            dns_record['name'] = data['name']
        if 'content' in data:
            dns_record['content'] = data['content']
        if 'type' in data:
            dns_record['type'] = data['type']
        if 'proxied' in data:
            dns_record['proxied'] = data['proxied'] != "false"

        return dns_record