import subprocess as s
import os

TARGET = "ourhouse.underarmour.com"
BASE_DIR = TARGET.replace(".", "_")
WORDLIST = "/usr/share/wordlists/common.txt"


def criar_pasta():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)


def run_cmd(cmd):
    s.call(cmd, stdout=s.DEVNULL, stderr=s.DEVNULL)


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


def ffuf_fuzz():
    output = f"{BASE_DIR}/{TARGET}_ffuf.txt"

    run_cmd(
        [
            "ffuf",
            "-u",
            f"https://{TARGET}/FUZZ",
            "-w",
            WORDLIST,
            "-mc",
            "200,204,301,302,307,401,403",
            "-t",
            "50",
            "-of",
            "txt",
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
    ffuf_fuzz()
