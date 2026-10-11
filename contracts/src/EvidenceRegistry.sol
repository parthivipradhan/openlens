// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title EvidenceRegistry
 * @dev Stores Merkle roots of LocalityLens evidence batches on-chain.
 *
 * Critical Rules (AGENTS.md):
 * - Store only Merkle roots on-chain. Never put personal data or raw evidence on-chain.
 * - Blockchain verification confirms digest integrity, not truth of underlying claims.
 * - Private keys stay server-side only.
 */
contract EvidenceRegistry {
    address public owner;

    struct BatchRecord {
        bytes32 root;
        uint256 leafCount;
        uint256 timestamp;
        address submittedBy;
        string manifestUri;
    }

    // Merkle root => BatchRecord
    mapping(bytes32 => BatchRecord) public batches;

    // List of all recorded batch roots
    bytes32[] public batchRoots;

    event BatchAnchored(
        bytes32 indexed root,
        uint256 leafCount,
        uint256 timestamp,
        address indexed submittedBy,
        string manifestUri
    );

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == owner, "EvidenceRegistry: caller is not the owner");
        _;
    }

    constructor() {
        owner = msg.sender;
        emit OwnershipTransferred(address(0), msg.sender);
    }

    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "EvidenceRegistry: new owner is zero address");
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }

    /**
     * @notice Anchor a batch Merkle root to the blockchain.
     * @param root The 32-byte Merkle root hash.
     * @param leafCount Number of evidence records included in this batch.
     * @param manifestUri Off-chain reference URI to the batch manifest.
     */
    function anchorBatch(
        bytes32 root,
        uint256 leafCount,
        string calldata manifestUri
    ) external onlyOwner {
        require(root != bytes32(0), "EvidenceRegistry: root cannot be zero");
        require(batches[root].root == bytes32(0), "EvidenceRegistry: batch already anchored");

        batches[root] = BatchRecord({
            root: root,
            leafCount: leafCount,
            timestamp: block.timestamp,
            submittedBy: msg.sender,
            manifestUri: manifestUri
        });

        batchRoots.push(root);

        emit BatchAnchored(root, leafCount, block.timestamp, msg.sender, manifestUri);
    }

    /**
     * @notice Check whether a Merkle root exists in the registry.
     */
    function isBatchAnchored(bytes32 root) external view returns (bool) {
        return batches[root].root != bytes32(0);
    }

    /**
     * @notice Retrieve batch details by Merkle root.
     */
    function getBatch(bytes32 root) external view returns (BatchRecord memory) {
        require(batches[root].root != bytes32(0), "EvidenceRegistry: batch not found");
        return batches[root];
    }

    /**
     * @notice Total number of batches anchored.
     */
    function totalBatches() external view returns (uint256) {
        return batchRoots.length;
    }

    /**
     * @notice Verify standard sorted-pair Merkle inclusion proof against a known root.
     * @param leaf The leaf hash to verify.
     * @param proof Sibling node hashes forming the Merkle branch.
     * @param root The expected Merkle root.
     */
    function verifyInclusion(
        bytes32 leaf,
        bytes32[] calldata proof,
        bytes32 root
    ) public pure returns (bool) {
        bytes32 computed = leaf;

        for (uint256 i = 0; i < proof.length; i++) {
            bytes32 sibling = proof[i];
            if (computed <= sibling) {
                computed = keccak256(abi.encodePacked(computed, sibling));
            } else {
                computed = keccak256(abi.encodePacked(sibling, computed));
            }
        }

        return computed == root;
    }
}
