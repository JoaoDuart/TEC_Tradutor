# 🧠 Tradutor de Máquinas de Turing — Modelos I ↔ S
## 📋 Descrição do Projeto

Este projeto implementa um tradutor automático entre dois modelos de Máquina de Turing compatíveis com o simulador online disponível em:

🔗 http://morphett.info/turing/turing.html

## ⚙️ Requisitos

Sistema operacional: Ubuntu 22.04.4 LTS (64 bits)

Linguagem: Python 3.8 ou superior

Verifique sua versão do Python com:
```
python3 --version
```
## 🚀 Execução
### 1️⃣ Clonar o repositório

Abra o terminal e execute:
```
git clone https://github.com/JoaoDuart/TEC_Tradutor.git
```
E depois execute:
```
cd TEC_Tradutor
```

### 2️⃣ Criar um arquivo de entrada

O trabalho ja ira conter um codigo.in contendo um programa de Máquina de Turing válido.

O programa contem uma máquina que aceita apenas cadeias terminadas em 11 (modelo infinito):


### 3️⃣ Executar o tradutor

No terminal:
```
python3 tradutor_mt.py codigo.in
```

Isso gerará o arquivo:
```
codigo.out
```
## 4️⃣ Testar no simulador

Acesse:
🔗 http://morphett.info/turing/turing.html

Cole o conteúdo do arquivo codigo.out no simulador.

Configure a fita de entrada, por exemplo:

011

Execute a simulação e observe:

halt_accept → a entrada foi aceita ✅

halt_reject → a entrada foi rejeitada ❌

## 🧪 Exemplos de teste

- 011	✅ halt_accept
- 1011	✅ halt_accept
- 111	✅ halt_accept
- 10	❌ halt_reject
- 01	❌ halt_reject
- 0	❌ halt_reject
