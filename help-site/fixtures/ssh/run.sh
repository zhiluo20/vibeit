#!/bin/sh
set -eu
password=$(cat /run/demo/password)
printf 'student:%s\n' "$password" | chpasswd
unset password
ssh-keygen -A >/dev/null 2>&1
install -d -m 700 -o student -g student /home/student/.ssh
install -m 600 -o student -g student /run/demo/id_ed25519.pub /home/student/.ssh/authorized_keys
if [ ! -d /home/student/tutorials ]; then
  cp -R /run/examples /home/student/tutorials
  chown -R student:student /home/student/tutorials
  su student -c 'cd /home/student/tutorials && git init -b main && git config user.name "Tutorial Student" && git config user.email student@example.invalid && git add . && git commit -m "Start tutorial workspace"' >/dev/null
fi
exec /usr/sbin/sshd -D -e -o PermitRootLogin=no -o PasswordAuthentication=yes -o PubkeyAuthentication=yes -o AllowUsers=student
