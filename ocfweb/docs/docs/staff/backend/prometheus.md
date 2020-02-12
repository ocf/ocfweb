[[!meta title="Prometheus"]]

We use Prometheus to provide real-time monitoring of our [[hardware|doc staff/backend]]. The master is [[dementors|doc staff/backend/servers]] which
uses the Node Exporter to collect data from other servers.

We monitor servers, desktops, and staff VMs, but not the hozer boxes.
Additionally, we don't receive email alerts for staff VMs. Monitoring for the networking switch, blackhole, is currently under development.

## Alerts

Alerts can be viewed at [prometheus.ocf.berkeley.edu/alerts](https://prometheus.ocf.berkeley.edu/alerts). They are configured at [this folder][prometheus-puppet] in the Puppet configs.

Alerts can additionally be configured using the [alert manager](prometheus.ocf.berkeley.edu/alertmanager). Alertmanager handles notifications for alerts via communication through email and Slack. Alerts can be inhibited or silenced. Alertmanager documentation can be found [here](https://prometheus.io/docs/alerting/alertmanager/).

Alerts are currently under development and may not be fully comprehensive.

## Metrics

Prometheus uses [metrics](https://prometheus.io/docs/concepts/metric_types/) to collect and visualize different types of data.

The main way Prometheus collects metrics in the OCF is [Node Exporter](https://github.com/prometheus/node_exporter). Another important exporter we use is the [SNMP Exporter](https://github.com/prometheus/snmp_exporter) which monitors information from printers, and possibly in the future, network switches.

A full list of exporters is available in the [Prometheus documentation](https://prometheus.io/docs/instrumenting/exporters/). In order to take advantage of these exporters, we define them in the [Puppet config for the Prometheus server][puppet-config].

### Custom Metrics

There are three main ways to generate custom metrics:

1. If metrics can be generated from a VM, run a script on a cronjob that writes to `/srv/prometheus`. These automatically get bundled into Node Exporter. We do this for CUPS monitoring - [here is an example of this in practice](https://github.com/ocf/puppet/blob/master/modules/ocf_printhost/manifests/monitor.pp).
2. Run a metrics server over HTTP and add them manually to the Puppet config. This is the most ideal method of using a prewritten exporter, like the Apache or Postfix exporters, both of which we use. An example of this is in the [Prometheus server config][puppet-config].
3. Run your exporter in Kubernetes if it doesn't matter which host it runs on. This is how we run the SNMP exporter. Again, this is done in the [Prometheus server config][puppet-config].

## Custom Queries

Prometheus supports querying a wide variety of metrics. (For a full list, go to [Prometheus](https://prometheus.ocf.berkeley.edu) and use the "insert metric at cursor" dropdown.) A basic query comes in the form:
```
metric{label="value", label2="value2", ...}
```

Some labels used frequently are:
 - **instance:** The name of the device that the data was collected from. Some examples are `papercut`, `avalanche`, or `supernova`.
 - **host_type:** The type of device that is being queried. Valid types are `desktop`, `server`, and `staffvm`.
 - **job:** The name of the job/exporter that collected the data. Some examples are `node`, `printer`, and `slurm`.

For example, if you would like to view the total RAM installed on each of the [[servers|doc staff/backend/servers]] you can query `node_memory_Active_bytes{host_type="server"}`.

To view the per-second rate of a metric, use
```
rate(metric{label="value",...})
```
For example, the data sent in bytes/second over the past 5 minutes by `fallingrocks` can be retrieved using `rate(node_network_transmit_bytes_total{instance="fallingrocks"}`.

For more info about querying, see the [official documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/).

Queries are best used in conjunction with Grafana, as to produce more readable results and save them for future reference. The next section will give more details on how to do this.

## Grafana

The frontend for Prometheus is [Grafana][grafana], which displays statistics collected by Prometheus in a user-friendly manner. Some of the more useful dashboards available are:
 - **[Servers](https://ocf.io/serverstats):** Displays usage information for the physical servers and hypervisors (fallingrocks, riptide, etc).
 - **[Desktops](https://ocf.io/desktopstats):** Displays usage information for lab computers (cyclone, acid, etc).
 - **[Printers](https://ocf.io/printerstats):** Displays printer usage and resource information.
 - **[Mirrors](https://ocf.io/mirrorstats):** Displays information about mirror staleness.
 - **[HPC](hhttps://ocf.io/hpcstats):** Displays usage information for the [[HPC cluster|doc services/hpc]].

There are more dashboards available, which can be accessed by clicking the dropdown arrow on the top left of the Grafana page.

Configuring Grafana dashboards does not require editing Puppet configs. Simply go to [Grafana][grafana], login using your OCF account, and click the plus icon on the left toolbar to begin visually creating a custom dashboard. Grafana uses [Prometheus queries](https://prometheus.io/docs/prometheus/latest/querying/basics/) to fetch data to be displayed.


[prometheus-puppet]: https://github.com/ocf/puppet/tree/master/modules/ocf_prometheus/files/rules.d
[grafana]: https://grafana.ocf.berkeley.edu
[puppet-config]: https://github.com/ocf/puppet/blob/master/modules/ocf_prometheus/manifests/server.pp
