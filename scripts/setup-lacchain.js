// scripts/setup-lacchain.js
const { ethers } = require("hardhat");
require("dotenv").config();

async function setupLACChainEnvironment() {
    console.log("⚙️ Setting up LACChain environment...");

    // LACChain specific configurations
    const lacchainConfig = {
        rpcUrl: process.env.RPC_URL || "https://writer.lacchain.net",
        nodeAddress: process.env.NODE_ADDRESS,
        expirationTime: process.env.EXPIRATION_TIME || Math.floor(Date.now() / 1000) + 86400,
        lacchainSigner: process.env.LACCHAIN_SIGNER
    };

    console.log("LACChain Configuration:");
    console.log("RPC URL:", lacchainConfig.rpcUrl);
    console.log("Node Address:", lacchainConfig.nodeAddress);
    console.log("Expiration Time:", new Date(lacchainConfig.expirationTime * 1000));

    // Validate private key format (elliptic curve)
    const privateKey = process.env.PRIVATE_KEY;
    if (!privateKey || privateKey.length !== 66) {
        throw new Error("Invalid private key format. Must be 64 hex characters with 0x prefix.");
    }

    console.log("✅ LACChain environment configured successfully");
    return lacchainConfig;
}

module.exports = { setupLACChainEnvironment };
