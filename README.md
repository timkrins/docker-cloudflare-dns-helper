# docker-cloudflare-dns-helper

[![Docker Stars](https://img.shields.io/docker/stars/timkrins/docker-cloudflare-dns-helper.svg?style=flat-square&logo=docker)](https://hub.docker.com/r/timkrins/docker-cloudflare-dns-helper/)
[![Docker Pulls](https://img.shields.io/docker/pulls/timkrins/docker-cloudflare-dns-helper.svg?style=flat-square&logo=docker)](https://hub.docker.com/r/timkrins/docker-cloudflare-dns-helper/)

This is a very simple tool to allow creation of Cloudflare DNS records using Docker labels.

It is inspired by `tiredofit/docker-traefik-cloudflare-companion` and `code5-lab/dns-flare`, using the config-by-label concept but does not require or use Traefik labels.

Notes:
 - There is no magic. You will need to define all configuration manually.
 - It does not currently update existing records.

I wrote this for my personal use, and I only use it for defined CNAME targets.

## Usage

Create a `.env` file containing the required Cloudflare API email and key (or define it directly in `environment:` in the next step, it is up to you):
```
CLOUDFLARE_EMAIL=example@email.com
CLOUDFLARE_API_KEY=your0secret0api0key000000000000000000
```

Run the service somewhere, and bind `/var/run/docker.sock` inside the container at the same location.

With `docker-compose`:

```
version: "3"

services:
  docker-cloudflare-dns-helper:
    image: timkrins/docker-cloudflare-dns-helper
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      - "CLOUDFLARE_EMAIL=${CLOUDFLARE_EMAIL}"
      - "CLOUDFLARE_API_KEY=${CLOUDFLARE_API_KEY}"
```

### Add labels to other services

To configure a DNS record, you can define labels on a service:
```
    labels:
      - cloudflare-dns.zone_name=example.com
      - cloudflare-dns.name=subdomain.example.com
      - cloudflare-dns.content=target.example.com
      - cloudflare-dns.type=CNAME
      - cloudflare-dns.proxied=true
```

Multiple records and high-level defaults are also possible by nesting keys underneath the root `cloudflare-dns` key.

For example,
```
    labels:
      - cloudflare-dns.zone_name=example.com
      - cloudflare-dns.content=target.example.com
      - cloudflare-dns.type=CNAME
      - cloudflare-dns.proxied=true
      - cloudflare-dns.1.name=one.example.com
      - cloudflare-dns.2.name=two.example.com
      - cloudflare-dns.3.content=target3.example.com
      - cloudflare-dns.3.name=three.example.com
```
would create three DNS entries, with the third entry having a different target.

Defaults can be supplied to the container via ENV variables.
ENV variable keys will be lowercased, with triple-underscores replaced by dashes, and double-underscores replaced by periods.
For example,

```
services:
  docker-cloudflare-dns-helper:
    image: timkrins/docker-cloudflare-dns-helper
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      - "CLOUDFLARE_EMAIL=${CLOUDFLARE_EMAIL}"
      - "CLOUDFLARE_API_KEY=${CLOUDFLARE_API_KEY}"
      - "CLOUDFLARE___DNS__ZONE_NAME=example.com"
      - "CLOUDFLARE___DNS__CONTENT=target.example.com"
      - "CLOUDFLARE___DNS__TYPE=CNAME"
      - "CLOUDFLARE___DNS__PROXIED=true"
```
