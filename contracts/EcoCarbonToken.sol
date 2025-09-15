// contracts/EcoCarbonToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract EcoCarbonToken is ERC20, AccessControl, ReentrancyGuard {
    // Constants from 's specifications
    string public constant NAME = "Eco-Carbon San Martin";
    string public constant SYMBOL = "ECOCO2";
    uint8 public constant DECIMALS = 3; // Sub-tonne precision

    // Roles
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant VERIFIER_ROLE = keccak256("VERIFIER_ROLE");
    bytes32 public constant RETIREMENT_ROLE = keccak256("RETIREMENT_ROLE");

    // Token Economics Structure (Claudio's Design)
    struct TokenEconomics {
        uint256 carbonSequestered;    // tCO2e with 3 decimals (11.040 = 11.04 tCO2e)
        uint256 biocharMass;          // Physical biochar mass in kg
        uint256 qualityMultiplier;    // Quality-based pricing multiplier (100-200)
        uint256 permanenceScore;      // Permanence rating (years guaranteed)
        string originGPS;             // GPS coordinates of origin
        string methodology;           // VCS/Gold Standard methodology
        uint256 timestamp;            // Block timestamp of creation
        bytes32 batchId;              // Unique batch identifier
        string ipfsHash;              // IPFS hash for off-chain documents
        bool isRetired;               // Retirement status
    }

    // Fee Structure (Claudio's Model)
    struct FeeStructure {
        uint256 mintingFee;      // 2% of token value at minting
        uint256 transferFee;     // 0.5% for standard transfers
        uint256 crossBorderFee;  // 1% for international transfers
        uint256 complianceFee;   // $50 fixed per compliance validation
        uint256 retirementFee;   // $25 fixed per retirement transaction
    }

    // State Variables
    mapping(bytes32 => TokenEconomics) public tokenBatches;
    mapping(address => uint256) public farmerRewards;
    FeeStructure public fees;
    uint256 public totalCarbonSequestered;
    uint256 public totalRetired;

    // Events
    event TokenMinted(
        bytes32 indexed batchId,
        address indexed farmer,
        uint256 amount,
        string gpsLocation
    );
    event TokenRetired(
        bytes32 indexed batchId,
        address indexed retirer,
        uint256 amount,
        string reason
    );
    event RevenueDistributed(
        address indexed farmer,
        uint256 farmerShare,
        uint256 platformShare,
        uint256 verificationShare,
        uint256 insuranceShare
    );

    constructor() ERC20("Eco-Carbon San Martin", "ECOCO2") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        _grantRole(VERIFIER_ROLE, msg.sender);

        // Initialize fee structure (Claudio's specifications)
        fees = FeeStructure({
            mintingFee: 200,        // 2%
            transferFee: 50,        // 0.5%
            crossBorderFee: 100,    // 1%
            complianceFee: 50 * 10**18,  // $50 in wei equivalent
            retirementFee: 25 * 10**18   // $25 in wei equivalent
        });
    }

    function decimals() public pure override returns (uint8) {
        return DECIMALS;
    }

    // Minting function with dMRV oracle validation
    function mintCarbonCredit(
        address farmer,
        uint256 amount,
        bytes32 batchId,
        string memory gpsLocation,
        string memory methodology,
        string memory ipfsHash,
        uint256 biocharMass,
        uint256 qualityScore
    ) external onlyRole(MINTER_ROLE) nonReentrant {
        require(amount > 0, "Amount must be greater than 0");
        require(biocharMass > 0, "Biochar mass must be greater than 0");
        require(qualityScore >= 85, "Quality score must be >= 85%");

        // Create token economics structure
        tokenBatches[batchId] = TokenEconomics({
            carbonSequestered: amount,
            biocharMass: biocharMass,
            qualityMultiplier: qualityScore > 90 ? 150 : 100,
            permanenceScore: 100, // 100+ years for biochar
            originGPS: gpsLocation,
            methodology: methodology,
            timestamp: block.timestamp,
            batchId: batchId,
            ipfsHash: ipfsHash,
            isRetired: false
        });

        // Mint tokens (11.04 ECOCO2 per ton of biochar)
        uint256 tokensToMint = (biocharMass * 11040) / 1000; // Convert to 3 decimal precision
        _mint(farmer, tokensToMint);

        totalCarbonSequestered += amount;

        emit TokenMinted(batchId, farmer, tokensToMint, gpsLocation);
    }

    // Revenue distribution according to Claudio's model
    function distributeTokenRevenue(uint256 totalRevenue) external nonReentrant {
        require(totalRevenue > 0, "Revenue must be greater than 0");

        uint256 farmerShare = totalRevenue * 60 / 100;      // 60% to farmers
        uint256 platformShare = totalRevenue * 20 / 100;    // 20% technology development
        uint256 verificationShare = totalRevenue * 10 / 100; // 10% MRV and compliance
        uint256 insuranceShare = totalRevenue * 10 / 100;   // 10% permanence guarantees

        // Distribution logic would be implemented here
        emit RevenueDistributed(msg.sender, farmerShare, platformShare, verificationShare, insuranceShare);
    }

    // Retirement function with on-chain receipt
    function retireCredits(
        bytes32 batchId,
        uint256 amount,
        string memory reason
    ) external onlyRole(RETIREMENT_ROLE) nonReentrant {
        require(tokenBatches[batchId].carbonSequestered > 0, "Invalid batch ID");
        require(balanceOf(msg.sender) >= amount, "Insufficient balance");
        require(!tokenBatches[batchId].isRetired, "Credits already retired");

        _burn(msg.sender, amount);
        tokenBatches[batchId].isRetired = true;
        totalRetired += amount;

        emit TokenRetired(batchId, msg.sender, amount, reason);
    }
}
