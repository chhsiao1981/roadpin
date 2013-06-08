# -*- coding: utf-8 -*-

import logging; 
import time
from urllib2 import urlopen
from fabric.api import *
from fabric.colors import *
from deploy import util
import re

PROJECT_NAME = "roadpin_backend"

@task    
def install_stage1(branch = 'master', n_proc = '4'):
    target_host = env.host_string
    _git_clone(target_host, branch)
    _install_production_ini(target_host, n_proc, 'production.ini')
    _set_virtualenv(target_host)
    _install_packages(target_host)
    _install_log_dir(target_host)
    _install_td_agent(target_host, 'td-agent.production.conf')
    _install_supervisor(target_host)

@task    
def install_staging(branch = 'master', n_proc = '4'):
    target_host = env.host_string
    _git_clone(target_host, branch)
    _install_production_ini(target_host, n_proc)
    _set_virtualenv(target_host)
    _install_packages(target_host)
    _install_log_dir(target_host)
    _install_td_agent(target_host)
    _install_supervisor(target_host)

@task
def update(branch = 'master', n_proc = '4'):
    target_host = env.host_string
    _git_pull(target_host, branch)
    _install_packages(target_host)
    _install_log_dir(target_host)
    _install_td_agent(target_host)
    _install_supervisor(target_host)

@task
def install_postinstall(n_proc = '4'):
    target_host = env.host_string
    _install_munin_node(target_host)
    _install_aphrodite(target_host)
    _install_node_balancer(target_host)

def _git_clone(target_host, branch = 'master'):    
    with cd("/srv"):
        try:
            sudo("git clone -b " + branch + " git@bitbucket.org:plaxieappier/" + PROJECT_NAME + ".git")
        except:
            print(red("[ERROR] unable to git clone"))

def _git_pull(target_host, branch = 'master'):    
    with cd("/srv/" + PROJECT_NAME):
        try:
            sudo("git pull origin " + branch)
        except:
            print(red("[ERROR] unable to git pull"))

def _set_virtualenv(target_host, virtualenv_dir='__'):
    with cd("/srv/" + PROJECT_NAME):
        sudo("./scripts/init_pcreate.sh " + virtualenv_dir)
        sudo("pip install --upgrade distribute")

def _install_packages(target_host, virtualenv_dir='__'):
    with cd("/srv/" + PROJECT_NAME), prefix("source " + virtualenv_dir + "/bin/activate"):
        sudo("pwd")
        sudo("which python")
        sudo("pip install -r requirements.txt")

def _install_production_ini(target_host, n_proc, ini_filename='staging.ini', virtualenv_dir='__'):
    target_host_no_dot = re.sub(ur'\.', '_', target_host, re.M | re.U)
    print(green('target_host:' + repr(target_host) + ' taregt_host_no_dot:' + repr(target_host_no_dot)))
    try:
        sudo("mkdir -p /etc/" + PROJECT_NAME)
    except:
        print(red("[ERROR] unable to mkdir -p /etc/" + PROJECT_NAME))

    with cd("/srv/" + PROJECT_NAME):
        sudo("cp " + ini_filename + " /etc/" + PROJECT_NAME + '/production.ini')

def _install_log_dir(target_host):
    try:
        sudo("mkdir -p /var/log/" + PROJECT_NAME)
    except:
        print(red("[ERROR] unable to mkdir -p /var/log/" + PROJECT_NAME))

def _install_supervisor(target_host, virtualenv_dir='__'):
    filename = PROJECT_NAME + ".conf"
    with cd("/srv/" + PROJECT_NAME), prefix("source " + virtualenv_dir + "/bin/activate"):
        sudo("cp deploy/supervisor/" + filename + " /etc/supervisor/conf.d")

    sudo("/etc/init.d/supervisor stop")
    time.sleep(5)
    sudo("/etc/init.d/supervisor start")

def _install_td_agent(target_host, filename='td-agent.staging.conf'):
    if not __is_install_td_agent(target_host):
        sudo('echo "include config.d/*.conf" >> /etc/td-agent/td-agent.conf')

    sudo("mkdir -p /etc/td-agent/config.d")
    with cd("/srv/" + PROJECT_NAME):
        try:
            sudo("cp deploy/td-agent/" + filename + " /etc/td-agent/config.d/" + PROJECT_NAME + ".conf")
        except:
            print(yellow("[WARNING] unable to cp deploy/td-agent/" + filename))

def __is_install_td_agent(target_host):
    return util.is_set("grep -P 'include config\.d' /etc/td-agent/td-agent.conf", 'install_td_agent')

def _install_munin_node(target_host):
    if __is_install_munin(target_host):
        return

    sudo("/bin/bash -c 'echo \"allow ^192\\.168\\.189\\.75$\" >> /etc/munin/munin-node.conf'")
    sudo("rm -f /etc/munin/plugins/nfs*")
    sudo("curl https://raw.github.com/arthur-debert/munin-httpresponse-plugin/master/httpresponsetime > /etc/munin/plugins/httpresponsetime")
    sudo("/bin/bash -c 'echo \"\" >> /etc/munin/plugin-conf.d/munin-node'")
    sudo("service munin-node restart")

def __is_install_munin(target_host):
    return util.is_set("grep '192\.168\.189\.75' /etc/munin/munin-node.conf", 'install_munin')

def _install_aphrodite(target_host):
    pass

def _install_node_balancer(target_host):
    pass
