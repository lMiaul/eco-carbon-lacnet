require("@nomiclabs/hardhat-ethers");
require("@lacchain/gas-model-provider");
require("dotenv").config();

module.exports = {
  solidity: {
    version: "0.8.19",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    lacchain_testnet: {
      url: process.env.RPC_URL || "https://writer.lacchain.net",
      gasPrice: 0,
      gas: 15000000,
      accounts: [process.env.PRIVATE_KEY],
      lacchain: true
    }
  }
};
