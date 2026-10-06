# Real-time conversational avatar on GCE

Mic -> STT -> LLM -> TTS -> lip-sync video over WebRTC, on a cloud NVIDIA GPU. The Mac is only the browser client.
Engine: [LiveTalking](https://github.com/lipku/LiveTalking) (Wav2Lip first, then MuseTalk). This folder is
infra + glue; nothing here has been run against a real GPU yet, so treat it as unverified.

## Flow
1. `cp config.env.example config.env`; set `PROJECT_ID`, `ZONE`, `MY_IP_CIDR`. Request L4 GPU quota first.
2. `scripts/create_vm.sh` then `scripts/firewall.sh` (rule is limited to your IP; re-run if it changes).
3. Store the key: `printf %s "$KEY" | gcloud secrets create anthropic-api-key --data-file=-`; grant the VM service account `secretmanager.secretAccessor`.
4. `scripts/vm.sh ssh`, copy `scripts/` over, run `setup_vm.sh`, download weights as it instructs.
5. `scripts/run.sh wav2lip`, open `http://<vm-ip>:8010` (see `vm.sh ip`; exact page path per LiveTalking README).
6. `DURATION=120 scripts/benchmark.sh`. Acceptance: FPS >= 25 and per-stage latency reported.
7. `scripts/vm.sh stop` when idle.

## Cost (list prices from the handoff, verify current)
g2-standard-4 (L4) ~ $0.71/hr; 12-16 vCPU sizes ~ $1.00-1.15/hr; disk and egress extra. Stopped VMs still pay for disk.

## Open items / caveats
- LiveTalking has no stated license: confirm before commercial use (AvatarAI, MIT, is the fallback).
- Interrupting mid-speech and some polish may be commercial-only: test and document the result here.
- `integrations/` is not yet wired into LiveTalking's plugin points (needs its source on the VM to hook the chat/TTS modules); STT/TTS providers undecided.
- UDP range and DLVM image family are starting points; verify, and add TURN if direct UDP fails.
