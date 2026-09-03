# SJSU Enterprise HW1 — Ansible Two-VM Webserver Deploy

Deploys a webserver to two VMs (VM1, VM2) with Ansible. Each serves a page on
port **8080** reading `Hello World from SJSU-1` / `Hello World from SJSU-2`.
The same playbook can fully un-deploy (tear down) the webserver resources.

## Architecture

- **Control node:** your Mac, running Ansible.
- **Managed nodes:** `vm1` and `vm2`, Ubuntu 22.04 VMs created with
  [Multipass](https://multipass.run) (works natively on Apple Silicon, unlike
  VirtualBox/Vagrant).
- **Webserver:** nginx, reconfigured to listen on 8080 instead of the default 80.
- One playbook (`playbook.yml`), two tagged plays: `deploy` and `undeploy`.

## Files

| File | Purpose |
|---|---|
| `cloud-init.yaml` | Injects your SSH public key into each VM at boot so Ansible can SSH in. |
| `inventory.ini` | Lists `vm1`/`vm2`, their IPs, and a `vm_number` var (1 or 2) used to render the right message per host. |
| `ansible.cfg` | Points Ansible at `inventory.ini` and disables interactive SSH host-key prompts (fine for disposable local VMs). |
| `playbook.yml` | The `deploy` play (install nginx, template config + page, start service) and the `undeploy` play (stop service, remove config/page, uninstall nginx). |
| `templates/index.html.j2` | Jinja2 template for the "Hello World from SJSU-X" page. |
| `templates/sjsu.conf.j2` | nginx site config, `listen 8080`. |

## Setup from scratch

```bash
# 1. Install tooling (macOS)
brew install --cask multipass
brew install ansible

# 2. Launch the two VMs, pre-loading your SSH key via cloud-init
multipass launch --name vm1 --cloud-init cloud-init.yaml jammy
multipass launch --name vm2 --cloud-init cloud-init.yaml jammy

# 3. Get their IPs
multipass list

# 4. Edit inventory.ini and replace the ansible_host IPs with the ones above

# 5. Confirm Ansible can reach both
ansible -i inventory.ini webservers -m ping
```

## Deploy the webserver

```bash
ansible-playbook -i inventory.ini playbook.yml --tags deploy
```

Verify:

```bash
curl http://<VM1_IP>:8080
curl http://<VM2_IP>:8080
```

Or open `http://<VM1_IP>:8080` and `http://<VM2_IP>:8080` in a browser —
should show "Hello World from SJSU-1" and "Hello World from SJSU-2" respectively.

## Un-deploy (tear down) the webserver

```bash
ansible-playbook -i inventory.ini playbook.yml --tags undeploy
```

This stops nginx, removes the site config and web root, and uninstalls the
nginx package. Re-running the `curl`/browser check afterward should fail
(connection refused) — that's the proof the teardown worked.

> Running `ansible-playbook playbook.yml` with **no** `--tags` runs both
> plays back to back (deploy immediately followed by undeploy) — always use
> `--tags deploy` or `--tags undeploy` explicitly.

## Tearing down the VMs entirely (optional, after the assignment)

```bash
multipass delete vm1 vm2
multipass purge
```

## Screenshot checklist (for the Word doc)

1. `multipass list` — showing vm1 and vm2 `Running` with their IPs.
2. `ansible -i inventory.ini webservers -m ping` — both hosts returning `pong`.
3. `ansible-playbook -i inventory.ini playbook.yml --tags deploy` — full output,
   `PLAY RECAP` line with `failed=0` for both hosts.
4. Browser tab showing `http://<VM1_IP>:8080` → "Hello World from SJSU-1".
5. Browser tab showing `http://<VM2_IP>:8080` → "Hello World from SJSU-2".
6. `ansible-playbook -i inventory.ini playbook.yml --tags undeploy` — full output,
   `PLAY RECAP` line with `failed=0`.
7. Browser (or `curl`) showing `http://<VM1_IP>:8080` now failing/refused,
   proving the un-deploy actually removed the webserver.

## Demo

Record or live-show, in order: VMs running → ping → deploy run → both pages
loading in the browser (side by side) → undeploy run → pages failing to load.
