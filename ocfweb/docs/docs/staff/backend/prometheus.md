[[!meta title="Prometheus"]]

We use Prometheus to provide real-time monitoring of our hardware. The master is [[dementors|doc staff/backend/servers]] which
uses the Node Exporter to collect data from other servers.

We monitor servers, desktops, and staff VMs, but not the hozer boxes.
Additionally, we don't receive email alerts for staff VMs. Monitoring for the networking switch, blackhole, is currently under development.

## Alerts

Alerts can be viewed at [prometheus.ocf.berkeley.edu/alerts](https://prometheus.ocf.berkeley.edu/alerts). They are configured at [this folder][prometheus-puppet] in the Puppet configs.

Alerts are currently under development and may not be fully comprehensive.

## Custom Queries

Prometheus supports querying a wide variety of metrics. (For a full list, go to [Prometheus](https://prometheus.ocf.berkeley.edu) and use the "insert metric at cursor" dropdown.) A basic query comes in the form:
```
metric{label="value", label2="value2", ...}
```
For example, if you would like to view the total RAM installed on each of the [[servers|doc staff/backend/servers]] you can query `node_memory_Active_bytes{host_type="server"}`.

To view the per-second rate of a metric, use
```
rate(metric{label="value",...})
```
For example, the data sent in bytes/second over the past 5 minutes by `fallingrocks` can be retrieved using `rate(node_network_transmit_bytes_total{instance="fallingrocks"}`.

Queries are best used in conjunction with Grafana, as to produce more readable results and save them for future reference. The next section will give more details on how to do this.

## Grafana

The frontend for Prometheus is [Grafana][grafana], which displays statistics collected by Prometheus in a user-friendly manner. Some of the more useful dashboards available are:
 - **[Servers](https://grafana.ocf.berkeley.edu/d/7n0r8PUWz/servers?orgId=1&refresh=10s):** Displays usage information for the physical servers and hypervisors (fallingrocks, riptide, etc).
 - **[Desktops](https://grafana.ocf.berkeley.edu/d/-VCUTE8Zk/desktops?orgId=1&refresh=10s):** Displays usage information for lab computers (cyclone, acid, etc).
 - **[Printers](https://grafana.ocf.berkeley.edu/d/SKl6_71iz/printers?orgId=1):** Displays printer usage and resource information.
 - **[Mirrors](https://grafana.ocf.berkeley.edu/d/Jo_bRsyiz/mirrors?orgId=1):** Displays information about mirror staleness.
 - **[HPC](https://grafana.ocf.berkeley.edu/d/N7Sb3nwik/hpc-slurm-dashboard?orgId=1&refresh=30s):** Displays usage information for the [[HPC cluster|doc services/hpc]].

Configuring Grafana dashboards does not require editing Puppet configs. Simply go to [Grafana][grafana], login using your OCF account, and click the plus icon on the left toolbar to begin visually creating a custom dashboard. Grafana uses [Prometheus queries](https://prometheus.io/docs/prometheus/latest/querying/basics/) to fetch data to be displayed.


[prometheus-puppet]: https://github.com/ocf/puppet/tree/master/modules/ocf_prometheus/files/rules.d
[grafana]: https://grafana.ocf.berkeley.edu
