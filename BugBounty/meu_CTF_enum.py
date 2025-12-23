import subprocess as s
import os


def criar_pasta(ip):
    if not os.path.exists(ip):
        os.makedirs(ip)
    os.chdir(ip)


def ping(ip):
    s.call(["bash", "-c", f"ping -c 3 {ip} > {ip}_ping.txt"])


def nmap(ip):
    s.call(["nmap", "-Pn", "-sV", "-oN", f"{ip}_nmap.txt", ip])


def dns_enum(dominio):
    output = f"{dominio}_dns.txt"

    s.call(["bash", "-c", f'echo "====== A ======" > {output}'])
    s.call(["bash", "-c", f"dig A {dominio} >> {output}"])

    s.call(["bash", "-c", f'echo "\n\n====== AAAA ======" >> {output}'])
    s.call(["bash", "-c", f"dig AAAA {dominio} >> {output}"])

    s.call(["bash", "-c", f'echo "\n\n====== MX ======" >> {output}'])
    s.call(["bash", "-c", f"dig MX {dominio} >> {output}"])

    s.call(["bash", "-c", f'echo "\n\n====== NS ======" >> {output}'])
    s.call(["bash", "-c", f"dig NS {dominio} >> {output}"])


def whois(dominio):
    s.call(["bash", "-c", f"whois {dominio} > {dominio}_whois.txt"])


def gobuster(ip):
    s.call(
        [
            "gobuster",
            "dir",
            "-u",
            "www.google.com.br",
            "-w",
            "/usr/share/wordlists/common.txt",
            "-t",
            "50",
            "-o",
            f"{ip}_gobuster.txt",
            ip,
        ]
    )


criar_pasta("teste")
ping("teste.com.br")
nmap("teste.com.br")
dns_enum("teste.com.br")
whois("teste.com.br")
gobuster("localhost")
