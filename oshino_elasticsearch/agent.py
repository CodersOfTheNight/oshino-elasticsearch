import aiohttp

from time import time

from oshino import Agent
from oshino.agents.http_agent import HttpAgent


def translate_cluster_status(status):
    if status == "green":
        return "ok"
    elif status == "yellow":
        return "warn"
    else:
        return "error"


async def _pull_data(path):
    async with aiohttp.ClientSession() as session:
        async with session.get(path) as resp:
            return await resp.json()


class ElasticSearchAgent(HttpAgent):
    MODE_CLUSTER = 0
    MODE_NODE = 1

    @property
    def api_version(self):
        return self._data.get("api_version", "5.6")

    @property
    def mode(self):
        mode = self._data.get("mode", "cluster")
        if mode == "cluster":
            return self.MODE_CLUSTER
        else:
            return self.MODE_NODE

    @property
    def fields(self):
        default_fields = [
                "transport",
                "http",
                "process",
                "jvm",
                "indices",
                "thread_pool"
        ]

        return self._data.get("fields", default_fields)

    async def retrieve_cluster_health(self):
        path = "{0}/_cluster/health".format(self.url)
        return await _pull_data(path)

    async def retrieve_node_info(self, node="_local"):
        path = ("{0}/_nodes/{1}/stats/{2}"
                .format(self.url, node, ",".join(self.fields)))
        return await _pull_data(path)

    async def process(self, event_fn):
        logger = self.get_logger()
        ts = time()

        # Parsing cluster health state
        cluster_health = await self.retrieve_cluster_health()
        logger.trace("Got content from ElasticSearch cluster health: {0}"
                     .format(cluster_health))
        state = translate_cluster_status(cluster_health["status"])

        te = time()
        span = int((te - ts) * 1000)
        event_fn(service=self.prefix + "health",
                 metric_f=span,
                 state=str(state),
                 description=self.url)

        # Other cluster info
        del cluster_health["cluster_name"]
        del cluster_health["timed_out"]
        del cluster_health["status"]


        for key, val in cluster_health.items():
            event_fn(service=self.prefix + key,
                     metric_f=float(val),
                     state="ok",
                     description=self.url)

        # Retrieving technical info


