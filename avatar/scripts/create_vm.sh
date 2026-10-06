#!/usr/bin/env bash
# Create the GPU VM. Override via config.env or env: MACHINE_TYPE, ZONE, IMAGE_FAMILY.
source "$(dirname "$0")/_common.sh"
"${GC[@]}" compute instances create "$VM_NAME" \
  --zone "$ZONE" --machine-type "$MACHINE_TYPE" \
  --image-family "$IMAGE_FAMILY" --image-project "$IMAGE_PROJECT" \
  --boot-disk-size "${BOOT_DISK_GB}GB" --boot-disk-type pd-balanced \
  --maintenance-policy TERMINATE --restart-on-failure \
  --metadata install-nvidia-driver=True \
  --tags avatar-gpu
echo "Created $VM_NAME. If creation failed with a quota error, request GPU quota first."
echo "Next: scripts/firewall.sh, then scripts/vm.sh ssh, then run scripts/setup_vm.sh on the VM."
