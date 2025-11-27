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
- 2 Resistores um para o Led e um para o sensor HC-SR04
- LED

## 🧩 Funcionamento
1. O sensor envia pulsos sonoros e calcula a distância do lixo.  
2. Se a distância for menor ou igual a **10 cm**, a lixeira é considerada **cheia**.  
3. O dispositivo está medindo a distância em tempo integral (constantemente). Contudo, ele só irá enviar uma notificação para o Telegram e alertar o usuário quando for detectado que um objeto ou pessoa está muito perto, especificamente a uma distância inferior a 10 centímetros.

## 🔧 Código principal
Arquivo: codigo_arduino.txt
## 👤 Autor
**Thiago Patrício** — [Thiangcbh456](https://github.com/Thiangcbh456)
