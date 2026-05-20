#!/bin/bash

set -e # если любая команда завершилась с ошибкой — сразу остановить весь sh-скрипт

cd blockchain

echo "Cleaning Hardhat artifacts/cache..."
npx hardhat clean

echo "Installing dependencies..."
npm install

echo "Installing OpenZeppelin..."
npm install @openzeppelin/contracts

echo "Compiling contracts..."
npx hardhat compile

echo "Starting Hardhat local node..."

# Если старый hardhat node уже висит на 8545 — убиваем
lsof -ti:8545 | xargs -r kill -9

# Запускаем hardhat node в фоне
npx hardhat node > hardhat-node.log 2>&1 &

NODE_PID=$!

echo "Hardhat node started with PID: $NODE_PID"
echo "Waiting for node to start..."

sleep 5

echo "Deploying contracts..."
npx hardhat run --network localhost scripts/deploy.js

echo "Done."
echo "Hardhat node is still running."
echo "Logs: hardhat-node.log"
echo "To stop node: kill $NODE_PID"

# Чтобы скрипт не завершался и сеть не умирала
wait $NODE_PID