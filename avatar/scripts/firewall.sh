#!/usr/bin/env bash
# Create/update the firewall rule, restricted to MY_IP_CIDR only.
source "$(dirname "$0")/_common.sh"
[ -n "${MY_IP_CIDR:-}" ] || { echo "Set MY_IP_CIDR (e.g. \$(curl -s ifconfig.me)/32)"; exit 1; }
case "$MY_IP_CIDR" in 0.0.0.0/0|::/0) echo "Refusing open-to-world rule."; exit 1;; esac
ARGS=(--direction INGRESS --action ALLOW --source-ranges "$MY_IP_CIDR" --target-tags avatar-gpu
      --rules "tcp:${TCP_PORT},udp:${UDP_RANGE}")
if "${GC[@]}" compute firewall-rules describe avatar-webrtc >/dev/null 2>&1; then
  "${GC[@]}" compute firewall-rules update avatar-webrtc --source-ranges "$MY_IP_CIDR" --allow "tcp:${TCP_PORT},udp:${UDP_RANGE}"
else
  "${GC[@]}" compute firewall-rules create avatar-webrtc "${ARGS[@]}"
fi
echo "Allowed only $MY_IP_CIDR. Your IP changed? Re-run. Direct UDP failing? Add a TURN server."
