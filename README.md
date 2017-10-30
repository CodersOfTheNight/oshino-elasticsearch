oshino-elasticsearch
=====================
ElasticSearch metric collector

For more info, refer to parent project [Oshino](https://github.com/CodersOfTheNight/oshino)

Example config
==============
```yaml
---
interval: 10
riemann:
  host: localhost
  port: 5555
agents:
  - name: cluster-health
    module: oshino_elasticsearch.agent.ElasticSearchAgent
    url: http://es.master.dev:9200
    tag: es
```
