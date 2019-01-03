Title: From zero to hero with ansible and django 
Date: 2015-02-25
Category: sysadmin
Tags: django, sysadmin, linux
Slug: from-zero-to-hero-with-ansible-and-django
Author: hernantz 
Summary: An opinationed set the best practices for deploying django with ansible.
Status: draft

Trying to put on paper an opinationed set the best practices for deploying django with ansible

## Get yourself into the party
This is to gain sudo access to the remote machine and be automatically identified.
For this to happen, this tree things need to be done:
1) Have the required ssh packages installed. `openssh-server` installed on the remote machine, 
and `openssh-client` installed on your machine. These packages should be installed by default 
on your distro.
2) Each host's fingerprint has to be added to your known_hosts file.
If you don't do this, the first time you try to access a host, you will be prompted to confirm
that you (human) recognize that host.
If you want to do this without interaction you could ship a `known_hosts` file with your repo, 
and put there the fingerprints of the hosts you want to make public.
For this you have to make ssh pick that file by passing it as an argument:
`ssh <user>@<host> -p <port> -o UserKnownHostsFile=/path/to/local_known_hosts_file`
in the repo I share an (empty) known_hosts.template
(https://juriansluiman.nl/article/151/managing-ssh-known-hosts-with-ansible)
3) Add your public key to each remote server, so that you don't have to enter password ever again.
This can be done by the following command: 
`ssh-copy-id "<user>@<host> -p <port> -o UserKnownHostsFile=/path/to/local_known_hosts_file"`
Your milage may vary, for instance Digital Ocean allows you to add public keys to your new droplets 
when they're created.

## Keep your secret vars separate
The strategy I'm folloing with private variables/data is to ship a `something.template` file
that will contain the data I want to make public (if any) and ask the user to copy that template
and put it in the same directory but with the name `something`, a file that is ignored by the VCS, 
and you would ask the users you trust to put whatever you need them to have in those files. 


create a deployer user with sudo privileges -> YOU SHOULN'T NEED SUDO TO RUN APP
copy your id-rsa.pub to the remote


## Bootstrap a secure initial setup
setup secure initialsetup.yaml
http://plusbryan.com/my-first-5-minutes-on-a-server-or-essential-security-for-linux-servers
http://lattejed.com/first-five-and-a-half-minutes-on-a-server-with-ansible
https://lextoumbourou.com/blog/posts/getting-started-with-ansible/#part-1


## bro tips
http://hakunin.com/six-ansible-practices#avoid-perpetually-changed-and-skipping-tasks
Separate your setup and deploy playbooks
your app has nothing to do with your server configuration



Teach Ansible to talk to Github on your behalf
Add Github to known_hosts properly and securely


## Nginx
https://serversforhackers.com/getting-started-with-ansible/
ssl certificates
disable default site 
html5boilerplate nginx settings


## Django
http://www.stavros.io/posts/example-provisioning-and-deployment-ansible/
collectstatic
bower install


view: https://github.com/makaimc/sf-django/blob/master/fabfile.py.template
https://github.com/jcalazan/ansible-django-stack/blob/master/env_vars/base.yml
https://github.com/tryolabs/metamon/blob/master/deploy/roles/dbserver/tasks/main.yml
https://github.com/tryolabs/metamon/blob/master/deploy/group_vars/vagrant.yml

systemd
https://github.com/Matt-Deacalion/systemd-django/tree/master/services
http://getpocket.com/a/read/846424367



PLACE VIRTUALENV IN /opt/project/venv

http://musings.tinbrain.net/django-deploy/?utm_source=Django+Round-up&utm_campaign=ccb0686e3c-Django_Round_Up_39&utm_medium=email&utm_term=0_2d6dd01daf-ccb0686e3c-320182857
