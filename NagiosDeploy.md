Todo: Make this a Chef/Puppet recipe/manifest

Nagios Node:
`sudo yum -y install nagios nagios-plugins-all nrpe`

Add to the bottom of `/etc/nagios/nrpe.cfg`:

    command[check_wowza]=/usr/lib64/nagios/plugins/check_procs -w 2:2 -c 2:100 -C WowzaStreamingE
