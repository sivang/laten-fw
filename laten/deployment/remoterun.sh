#!/bin/bash -x

ansible-playbook $1 --user=ubuntu # \
                             # --extra-vars "ansible_sudo_pass=$PASSWORD"
