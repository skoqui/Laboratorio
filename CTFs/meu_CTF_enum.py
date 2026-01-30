#!/usr/bin/env python3

import subprocess as s
import os
import sys

TARGET = "10.67.151.161"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.join(SCRIPT_DIR, TARGET.replace(".", "_"))


def criar_pasta():
    print("[DEBUG] Script rodando em:", SCRIPT_DIR)
    print("[DEBUG] Pasta de sa�da:", BASE_DIR)

    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
        print(f"[+] Pasta criada: {BASE_DIR}")
    else:
        print(f"[+] Pasta j� existe: {BASE_DIR}")


def run_cmd(cmd):
    print("[+] Executando:", " ".join(cmd))
    result = s.run(cmd)

    if result.returncode != 0:
        print("[!] Erro ao executar comando!")
        sys.exit(1)


def ping():
    output = f"{BASE_DIR}/{TARGET}_ping.txt"
    run_cmd(["bash", "-c", f"ping -c 3 {TARGET} > {output}"])


def nmap_scan():
    output = f"{BASE_DIR}/{TARGET}_nmap.txt"
    run_cmd(["nmap", "-Pn", "-sV", "-oN", output, TARGET])


def dns_enum():
    output = f"{BASE_DIR}/{TARGET}_dns.txt"

    cmds = [
        f'echo "====== A ======" > {output}',
        f"dig A {TARGET} >> {output}",
        f'echo "\n====== AAAA ======" >> {output}',
        f"dig AAAA {TARGET} >> {output}",
        f'echo "\n====== MX ======" >> {output}',
        f"dig MX {TARGET} >> {output}",
        f'echo "\n====== NS ======" >> {output}',
        f"dig NS {TARGET} >> {output}",
    ]

    for cmd in cmds:
        run_cmd(["bash", "-c", cmd])


def whois_lookup():
    output = f"{BASE_DIR}/{TARGET}_whois.txt"
    run_cmd(["bash", "-c", f"whois {TARGET} > {output}"])


def gobuster_scan():
    output = f"{BASE_DIR}/{TARGET}_gobuster.txt"

    run_cmd(
        [
            "gobuster",
            "dir",
            "-u",
            f"http://{TARGET}",
            "-w",
            "/usr/share/wordlists/dirb/common.txt",
            "-t",
            "50",
            "-o",
            output,
        ]
    )


if __name__ == "__main__":
    criar_pasta()
    ping()
    nmap_scan()
    dns_enum()
    whois_lookup()
    gobuster_scan()

    print("\n[\u2714] Recon finalizado com sucesso!")
