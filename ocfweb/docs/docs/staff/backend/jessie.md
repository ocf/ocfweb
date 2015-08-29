[[!meta title="jessie migration"]]
# jessie migration

This table lists all servers and whether they have been upgraded to jessie. In
general, we prefer to rebuild new servers using jessie, rather than upgrading
from wheezy. There are a few exceptions (marked as "upgrade" in the table).

We don't list the desktops (all are jessie already).

<table>
    <tr><th>Server</th> <th>Status</th> <th>Comment</th></tr>

    <!-- public-facing servers -->
    <tr><td>death</td>	<td>wheezy</td>	<td>rebuild - complicated (rt#3524)</td></tr>
    <tr><td>tsunami</td>	<td>wheezy</td>	<td>rebuild - same time as death (public)</td></tr>
    <tr><td>biohazard</td>	<td>wheezy</td>	<td>rebuild - same time as death (public)</td></tr>

    <tr><td>pollution</td>	<td>wheezy</td>	<td>rebuild - pykota not compatible with jessie on last attempt, not well puppeted</td></tr>


    <!-- already upgraded -->
    <tr><td>jaws</td>	<td>jessie</td>	<td>upgrade - kvm host</td></tr>
    <tr><td>hal</td>	<td>jessie</td>	<td>upgrade - kvm host</td></tr>
    <tr><td>pandemic</td>	<td>jessie</td>	<td>upgrade - kvm host</td></tr>

    <tr><td>anthrax</td>	<td>jessie</td>	<td>rebuild (no known issues)</td></tr>
    <tr><td>blight</td>	<td>jessie</td>	<td>rebuild</td></tr>
    <tr><td>dementors</td>	<td>jessie</td>	<td>rebuild - need to transfer some data (printer csv logs, munin data)</td></tr>
    <tr><td>earthquake</td>	<td>jessie</td>	<td>rebuild - need to update ocflib with new path to kadmin at same time</td></tr>
    <tr><td>fallingrocks</td>	<td>jessie</td>	<td>upgrade - mirrors</td></tr>
    <tr><td>firestorm</td>	<td>jessie</td>	<td>upgrade - ldap/kerberos, needs careful testing</td></tr>
    <tr><td>lightning</td>	<td>jessie</td>	<td>upgrade - puppet host</td></tr>
    <tr><td>maelstrom</td>	<td>jessie</td>	<td>upgrade - mysql host, needs testing first</td></tr>
    <tr><td>pestilence</td>	<td>jessie</td>	<td>rebuild - need to puppet first (want to move dns to git)</td></tr>
    <tr><td>sandstorm</td>	<td>jessie</td>	<td>upgrade - replacing with new mail service (rt#3068) which will be rebuilt</td></tr>
    <tr><td>supernova</td>	<td>jessie</td>	<td>upgrade - atool not well puppeted - still want to rebuild (rt#3676)</td></tr>
    <tr><td>typhoon</td>	<td>jessie</td>	<td>rebuild</td></tr>
    <tr><td>zombies</td>	<td>jessie</td>	<td>upgrade - some config not puppeted (csgo)</td></tr>

    <tr><td>blackrain</td>	<td>jessie</td>	<td>upgrade - hozer</td></tr>
    <tr><td>blacksheep</td>	<td>jessie</td>	<td>upgrade - hozer</td></tr>
    <tr><td>despair</td>	<td>jessie</td>	<td>upgrade - hozer</td></tr>
    <tr><td>flood</td>	<td>jessie</td>	<td>upgrade - hozer (irc)</td></tr>
    <tr><td>gnats</td>	<td>jessie</td>	<td>upgrade - hozer</td></tr>
    <tr><td>kamikaze</td>	<td>jessie</td>	<td>upgrade - hozer</td></tr>
    <tr><td>limniceruption</td>	<td>jessie</td>	<td>upgrade - hozer</td></tr>
    <tr><td>locusts</td>	<td>jessie</td>	<td>upgrade - hozer</td></tr>
    <tr><td>meltdown</td>	<td>jessie</td>	<td>upgrade - hozer</td></tr>
    <tr><td>meteorstorm</td>	<td>jessie</td>	<td>upgrade - hozer</td></tr>
    <tr><td>mudslide</td>	<td>jessie</td>	<td>upgrade - hozer</td></tr>
    <tr><td>quicksand</td>	<td>jessie</td>	<td>upgrade - hozer</td></tr>
    <tr><td>raptors</td>	<td>jessie</td>	<td>upgrade - hozer</td></tr>
    <tr><td>revolution</td>	<td>jessie</td>	<td>upgrade - hozer</td></tr>
    <tr><td>smallpox</td>	<td>jessie</td>	<td>upgrade - hozer</td></tr>
</table>

<!-- vim: ts=20
-->
