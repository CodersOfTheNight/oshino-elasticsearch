oshino-elasticsearch
=====================
ElasticSearch metric collector

For more info, refer to parent project [Oshino](https://github.com/CodersOfTheNight/oshino)

Installing
==========
Via pip:
`pip install oshino_elasticsearch`

Or via oshino-admin, if you already have oshino

`oshino-admin plugin install oshino_elasticsearch`

Config
======

`url` - elasticsearch base url

`fields` - array which defines what metric groups you want to receive. You can call [http://localhost:9200/_nodes/_all/stats](http://localhost:9200/_nodes/_all/stats) and see full listing.

Example config
---------------
```yaml
---
interval: 10
riemann:
  host: localhost
  port: 5555
agents:
  - name: cluster-health
    module: oshino_elasticsearch.agent.ElasticSearchAgent
    fields:
      - transport
      - http
      - jvm
      - thread_pool
    url: http://es.master.dev:9200
    tag: es
```
