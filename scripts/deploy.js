// scripts/deploy.js - Updated for LACNet BaseRelayRecipient
const { ethers } = require("hardhat");
require("dotenv").config();

async function main() {
    console.log("🚀 Starting Eco-Carbon San Martín deployment on LACNet...");

    // Get the deployer account
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with account:", deployer.address);

    // LACNet specific configuration
    const trustedForwarder = process.env.TRUSTED_FORWARDER;
    if (!trustedForwarder) {
        throw new Error("TRUSTED_FORWARDER must be set in .env file");
    }
    console.log("Using Trusted Forwarder:", trustedForwarder);

    // Check balance
    const balance = await deployer.getBalance();
    console.log("Account balance:", ethers.utils.formatEther(balance), "ETH");

    try {
        // 1. Deploy SimpleGreeting (with BaseRelayRecipient)
        console.log("\n📝 Deploying SimpleGreeting contract with BaseRelayRecipient...");
        const SimpleGreeting = await ethers.getContractFactory("SimpleGreeting");
        const greeting = await SimpleGreeting.deploy(trustedForwarder);
        await greeting.deployed();
        console.log("✅ SimpleGreeting deployed to:", greeting.address);

        // 2. Deploy SimpleStorage (with BaseRelayRecipient)
        console.log("\n💾 Deploying SimpleStorage contract with BaseRelayRecipient...");
        const SimpleStorage = await ethers.getContractFactory("SimpleStorage");
        const storage = await SimpleStorage.deploy(trustedForwarder);
        await storage.deployed();
        console.log("✅ SimpleStorage deployed to:", storage.address);

        // 3. Deploy main EcoCarbonToken contract (with BaseRelayRecipient)
        console.log("\n🌱 Deploying EcoCarbonToken contract with BaseRelayRecipient...");
        const EcoCarbonToken = await ethers.getContractFactory("EcoCarbonToken");
        const carbonToken = await EcoCarbonToken.deploy(trustedForwarder);
        await carbonToken.deployed();
        console.log("✅ EcoCarbonToken deployed to:", carbonToken.address);

        // 4. Verify BaseRelayRecipient integration
        console.log("\n🔍 Verifying BaseRelayRecipient integration...");

        // Test SimpleGreeting with meta-transaction capability
        const currentGreeting = await greeting.getGreeting();
        console.log("Current greeting:", currentGreeting);

        // Test SimpleStorage with meta-transaction capability
        await storage.storeCarbonData("pilot_tons_processed", 1000);
        const storedValue = await storage.getCarbonData("pilot_tons_processed");
        console.log("Stored carbon data:", storedValue.toString());

        // Test EcoCarbonToken BaseRelayRecipient features
        const tokenName = await carbonToken.name();
        const tokenSymbol = await carbonToken.symbol();
        const tokenDecimals = await carbonToken.decimals();
        console.log(`Token: ${tokenName} (${tokenSymbol}) - Decimals: ${tokenDecimals}`);

        // Verify trusted forwarder is set correctly
        const setForwarder = await carbonToken.isTrustedForwarder(trustedForwarder);
        console.log("Trusted Forwarder correctly set:", setForwarder);

        // 5. Save deployment addresses with LACNet specific info
        const deploymentInfo = {
            timestamp: new Date().toISOString(),
            network: "lacchain_testnet",
            deployer: deployer.address,
            trustedForwarder: trustedForwarder,
            lacnetFeatures: {
                baseRelayRecipient: true,
                metaTransactions: true,
                gaslessTransactions: true
            },
            contracts: {
                SimpleGreeting: greeting.address,
                SimpleStorage: storage.address,
                EcoCarbonToken: carbonToken.address
            }
        };

        console.log("\n📋 LACNet Deployment Summary:");
        console.log(JSON.stringify(deploymentInfo, null, 2));

        // Save to file
        const fs = require("fs");
        fs.writeFileSync("lacnet-deployment-addresses.json", JSON.stringify(deploymentInfo, null, 2));
        console.log("✅ LACNet deployment addresses saved to lacnet-deployment-addresses.json");

        // 6. Important notes for LACNet usage
        console.log("\n⚠️  IMPORTANT LACNet Notes:");
        console.log("1. All contracts inherit from BaseRelayRecipient");
        console.log("2. Use _msgSender() instead of msg.sender in contract interactions");
        console.log("3. Meta-transactions are enabled for gasless operations");
        console.log("4. Trusted Forwarder address:", trustedForwarder);
        console.log("5. See LACNet docs sections 8-9 for interaction details");

    } catch (error) {
        console.error("❌ LACNet deployment failed:", error);
        if (error.message.includes("BaseRelayRecipient")) {
            console.log("\n🔧 Troubleshooting BaseRelayRecipient issues:");
            console.log("1. Ensure @lacchain/relay-contracts is installed");
            console.log("2. Verify TRUSTED_FORWARDER address in .env");
            console.log("3. Check LACNet network configuration");
        }
        process.exit(1);
    }
}

main()
    .then(() => {
        console.log("🎉 LACNet deployment completed successfully!");
        console.log("📚 Next: Use scripts/interact-lacnet.js for meta-transaction testing");
        process.exit(0);
    })
    .catch((error) => {
        console.error("💥 LACNet deployment error:", error);
        process.exit(1);
    });
