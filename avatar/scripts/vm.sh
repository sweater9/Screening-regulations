#!/usr/bin/env bash
# Usage: vm.sh start|stop|status|ssh|ip   (stop the VM when idle: billing is hourly)
source "$(dirname "$0")/_common.sh"
case "${1:-}" in
  start)  "${GC[@]}" compute instances start "$VM_NAME" --zone "$ZONE";;
  stop)   "${GC[@]}" compute instances stop  "$VM_NAME" --zone "$ZONE";;
  status) "${GC[@]}" compute instances describe "$VM_NAME" --zone "$ZONE" --format='value(status)';;
  ip)     "${GC[@]}" compute instances describe "$VM_NAME" --zone "$ZONE" --format='value(networkInterfaces[0].accessConfigs[0].natIP)';;
  ssh)    "${GC[@]}" compute ssh "$VM_NAME" --zone "$ZONE";;
  *) echo "usage: $0 start|stop|status|ssh|ip"; exit 1;;
esac
