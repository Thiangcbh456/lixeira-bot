# 🚮 Lixeira Ultrassônica

Projeto Arduino para monitoramento de nível de lixo usando sensor ultrassônico **HC-SR04**.

## 🧠 Descrição
O sistema mede a distância entre o topo da lixeira e o lixo.  
Quando a distância fica menor que um limite definido, é exibida uma mensagem de **"Lixeira cheia"** no monitor serial.

## ⚙️ Componentes
- Arduino UNO
- Sensor ultrassônico HC-SR04
- Jumpers e protoboard
- Cabo USB

## 🧩 Funcionamento
1. O sensor envia pulsos sonoros e calcula a distância do lixo.  
2. Se a distância for menor ou igual a **10 cm**, a lixeira é considerada **cheia**.  
3. As leituras são feitas a cada **30 segundos**.

## 🔧 Código principal
Arquivo: codigo_arduino.txt
## 👤 Autor
**Thiago Patrício** — [Thiangcbh456](https://github.com/Thiangcbh456)
