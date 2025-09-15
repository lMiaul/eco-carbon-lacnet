// scripts/interact.js
const { ethers } = require("hardhat");
const deploymentAddresses = require("../lacnet-deployment-addresses.json");

async function main() {
    console.log("🔗 Interacting with deployed contracts on LACNet...");

    const [signer] = await ethers.getSigners();
    console.log("Using account:", signer.address);

    try {
        // 1. Interact with SimpleGreeting
        console.log("\n📝 Testing SimpleGreeting...");
        const greeting = await ethers.getContractAt(
            "SimpleGreeting", 
            deploymentAddresses.contracts.SimpleGreeting
        );

        // Update greeting
        const tx1 = await greeting.updateGreeting("¡Hola desde San Martín, Perú!");
        await tx1.wait();
        console.log("✅ Greeting updated");

        const newGreeting = await greeting.getGreeting();
        console.log("New greeting:", newGreeting);

        // 2. Interact with SimpleStorage
        console.log("\n💾 Testing SimpleStorage...");
        const storage = await ethers.getContractAt(
            "SimpleStorage",
            deploymentAddresses.contracts.SimpleStorage
        );

        // Store some carbon data
        const carbonData = {
            "families_participating": 127,
            "tons_processed": 1000,
            "tokens_minted": 11040,
            "co2_sequestered": 54000 // in kg
        };

        for (const [key, value] of Object.entries(carbonData)) {
            const tx = await storage.storeCarbonData(key, value);
            await tx.wait();
            console.log(`✅ Stored ${key}: ${value}`);
        }

        // 3. Interact with EcoCarbonToken
        console.log("\n🌱 Testing EcoCarbonToken...");
        const carbonToken = await ethers.getContractAt(
            "EcoCarbonToken",
            deploymentAddresses.contracts.EcoCarbonToken
        );

        // Get token info
        const name = await carbonToken.name();
        const symbol = await carbonToken.symbol();
        const decimals = await carbonToken.decimals();
        const totalSupply = await carbonToken.totalSupply();

        console.log(`Token Info: ${name} (${symbol})`);
        console.log(`Decimals: ${decimals}`);
        console.log(`Total Supply: ${totalSupply.toString()}`);

        // Test minting (would require MINTER_ROLE in real scenario)
        console.log("\n🔨 Testing token minting simulation...");

        const batchId = ethers.utils.keccak256(
            ethers.utils.toUtf8Bytes("batch_001_tocache")
        );

        console.log(`Simulated batch ID: ${batchId}`);
        console.log("Note: Actual minting requires MINTER_ROLE authorization");

        console.log("\n✅ All interactions completed successfully!");

    } catch (error) {
        console.error("❌ Interaction failed:", error);
        console.log("\nTroubleshooting tips:");
        console.log("1. Ensure contracts are deployed");
        console.log("2. Check your private key and network configuration");
        console.log("3. Verify you have sufficient gas");
    }
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
