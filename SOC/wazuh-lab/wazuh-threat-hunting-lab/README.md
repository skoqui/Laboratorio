# 🛡️ Wazuh Threat Hunting – Correção de Coleta de Eventos WFP (Windows Filtering Platform)

> **Projeto de Portfólio – Blue Team / SOC Analyst**  
> Ambiente de laboratório com **Kali Linux (Atacante)**, **Windows 10/Server (Alvo)** e **Ubuntu (Wazuh Manager/SIEM)**

---

## 📌 Resumo Executivo

Durante a implementação de um laboratório SOC com Wazuh, foi identificado que os eventos de **conexão e bloqueio de firewall do Windows (WFP – Event IDs 5156 e 5157)** não estavam sendo exibidos no SIEM, mesmo sendo gerados corretamente no **Windows Event Viewer**.

A causa raiz foi um **filtro no agente Wazuh Windows (`ossec.conf`) que descartava explicitamente esses eventos antes do envio ao manager**.

Este documento descreve o diagnóstico, correção e validação do problema, além de fornecer um procedimento reutilizável para futuras instalações.

---

## 🎯 Objetivo

Garantir que o Wazuh capture e permita **Threat Hunting de atividades de rede e reconhecimento (MITRE T1046)** por meio dos eventos:

- **5156** – Windows Filtering Platform Allowed Connection
- **5157** – Windows Filtering Platform Blocked Connection

---

## 🏗️ Arquitetura do Lab

| Máquina | Sistema | Função | IP |
|---------|----------|--------|----|
| Kali Linux | Debian-based | Atacante | `192.168.122.210` |
| Windows | Windows 10 / Server 2022 | Endpoint Monitorado | `192.168.122.180` |
| Ubuntu | Ubuntu Desktop | Wazuh Manager + SIEM | `192.168.122.1` |

Rede:
- **NAT / Libvirt (virbr0 – 192.168.122.0/24)**

---

## 🔍 Sintoma

- Nmap e tentativas de conexão geravam eventos no Windows:

```powershell
Get-WinEvent -LogName Security | Where-Object { $_.Id -eq 5156 -or $_.Id -eq 5157 }
```

- Porém:
  - Nada aparecia no Wazuh Dashboard
  - Nada era registrado em `alerts.json`

---

## 🧠 Diagnóstico

### 1. Confirmação da Conectividade do Agente

No Windows:

```text
INFO: Connected to the server ([192.168.122.1]:1514/tcp)
```

No Ubuntu:

```bash
sudo tail -f /var/ossec/logs/ossec.log
```

Resultado:
- Agente autenticado
- Comunicação TCP ativa

---

### 2. Verificação do Filtro no `ossec.conf`

Trecho problemático encontrado:

```xml
<localfile>
  <location>Security</location>
  <log_format>eventchannel</log_format>
  <query>
    Event/System[EventID != 5145 and EventID != 5156 and EventID != 5157]
  </query>
</localfile>
```

### ⚠️ Impacto

Esse filtro:
- Exclui os eventos **5156 e 5157**
- Impede que eles sejam enviados ao Wazuh Manager

Mesmo que o Windows registre corretamente, o agente **descarta localmente**.

---

## ✅ Solução

### Opção 1 – Coleta Total (Recomendado – SOC Real)

Remove o filtro e permite caçar no SIEM:

```xml
<localfile>
  <location>Security</location>
  <log_format>eventchannel</log_format>
</localfile>
```

### Opção 2 – Coleta Focada em Firewall (Threat Hunting)

```xml
<localfile>
  <location>Security</location>
  <log_format>eventchannel</log_format>
  <query>
    Event/System[EventID=5156 or EventID=5157]
  </query>
</localfile>
```

---

## 🔄 Aplicação da Correção

No Windows:

```powershell
notepad "C:\Program Files (x86)\ossec-agent\ossec.conf"
```

Após salvar:

```powershell
Restart-Service WazuhSvc
```

---

## 🧪 Validação

### Geração de Evento (Kali)

```bash
nmap -sS -p 445,5985,3389 192.168.122.180
```

### Monitoramento no Manager

```bash
sudo tail -f /var/ossec/logs/alerts/alerts.json
```

### Resultado Esperado

Campos visíveis:
- `agent.name`: WINDOWS2022
- `srcip`: IP do Kali
- `dstport`: 445 / 5985 / 3389
- `rule.mitre.id`: **T1046**
- `event.action`: allowed / blocked

---

## 🧭 Mapeamento MITRE ATT&CK

| Técnica | Nome | Evento |
|----------|--------|---------|
| T1046 | Network Service Discovery | 5156 / 5157 |

Esses eventos indicam:
- Reconhecimento de rede
- Enumeração de serviços
- Tentativas de movimento lateral

---

## 📊 Uso em Threat Hunting

Consultas no Wazuh / OpenSearch:

- Filtrar por agente
- Agrupar por porta
- Detectar varreduras (múltiplas portas em curto período)
- Correlacionar IP de origem

---

## 🧱 Boas Práticas

- Não filtrar eventos no agente — filtrar no SIEM
- Manter coleta ampla no endpoint
- Criar dashboards para:
  - Recon
  - Brute force
  - Lateral movement
  - Firewall drops

---

## 🏁 Conclusão

Este problema demonstra um cenário real de SOC:
> Eventos existem, conectividade existe, mas **a coleta falha por causa de filtros mal configurados no endpoint**.

A correção permite:
- Threat Hunting em tempo real
- Mapeamento MITRE
- Detecção de reconhecimento e ataque de rede

Este laboratório representa um **ambiente prático de Blue Team nível júnior/pleno** e pode ser usado como portfólio técnico.

---

## 👤 Autor

**Luis Scoqui**  
Estudante de Segurança da Informação / Blue Team / SOC Lab  
Ano: 2026
