# Eco-Carbon San Martín – LACNet Smart Contracts

Este proyecto implementa contratos inteligentes en la red **LACNet** para la tokenización de créditos de carbono, siguiendo el modelo de Eco-Carbon San Martín.

## 📦 Instalación
```bash
npm install
```

## ⚙️ Configuración
Copia `.env.example` en `.env` y completa tus credenciales LACNet:
```
PRIVATE_KEY=0x...
RPC_URL=https://writer.lacchain.net
NODE_ADDRESS=0x...
EXPIRATION_TIME=...
LACCHAIN_SIGNER=0x...
```

## 🚀 Despliegue en LACNet
```bash
npx hardhat compile
npx hardhat run scripts/deploy.js --network lacchain_testnet
```

## 🧪 Tests
```bash
npx hardhat test
```

## 🌐 Interfaz
```bash
cd interface
python -m http.server 8000
```
Visita: [http://localhost:8000](http://localhost:8000)
