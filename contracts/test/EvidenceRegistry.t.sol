// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface Vm {
    function prank(address) external;
}

contract Test {
    Vm internal constant vm = Vm(address(uint160(uint256(keccak256("hevm cheat code")))));

    function assertTrue(bool condition) internal pure {
        require(condition, "assertTrue failed");
    }

    function assertFalse(bool condition) internal pure {
        require(!condition, "assertFalse failed");
    }

    function assertEq(bytes32 a, bytes32 b) internal pure {
        require(a == b, "assertEq(bytes32) failed");
    }

    function assertEq(uint256 a, uint256 b) internal pure {
        require(a == b, "assertEq(uint256) failed");
    }

    function assertEq(address a, address b) internal pure {
        require(a == b, "assertEq(address) failed");
    }
}

import "../src/EvidenceRegistry.sol";

contract EvidenceRegistryTest is Test {
    EvidenceRegistry public registry;
    address public deployer;
    address public nonOwner;

    function setUp() public {
        deployer = address(this);
        nonOwner = address(0x999);
        registry = new EvidenceRegistry();
    }

    function testOwnerIsDeployer() public view {
        assertEq(registry.owner(), deployer);
    }

    function testAnchorBatch() public {
        bytes32 root = keccak256("batch-1-root");
        uint256 leafCount = 42;
        string memory uri = "ipfs://QmLocalityLensBatch1Manifest";

        registry.anchorBatch(root, leafCount, uri);

        assertTrue(registry.isBatchAnchored(root));
        assertEq(registry.totalBatches(), 1);

        EvidenceRegistry.BatchRecord memory b = registry.getBatch(root);
        assertEq(b.root, root);
        assertEq(b.leafCount, leafCount);
        assertEq(b.submittedBy, deployer);
    }

    function testCannotAnchorZeroRoot() public {
        bytes32 zeroRoot = bytes32(0);
        try registry.anchorBatch(zeroRoot, 10, "uri") {
            assertTrue(false); // Should have reverted
        } catch {
            assertTrue(true);
        }
    }

    function testCannotAnchorDuplicateRoot() public {
        bytes32 root = keccak256("unique-root");
        registry.anchorBatch(root, 5, "uri");

        try registry.anchorBatch(root, 5, "uri2") {
            assertTrue(false); // Should have reverted
        } catch {
            assertTrue(true);
        }
    }

    function testVerifyInclusionProof() public view {
        bytes32 leaf1 = keccak256("leaf1");
        bytes32 leaf2 = keccak256("leaf2");

        bytes32 root;
        if (leaf1 <= leaf2) {
            root = keccak256(abi.encodePacked(leaf1, leaf2));
        } else {
            root = keccak256(abi.encodePacked(leaf2, leaf1));
        }

        bytes32[] memory proof = new bytes32[](1);
        proof[0] = leaf2;

        bool valid = registry.verifyInclusion(leaf1, proof, root);
        assertTrue(valid);

        bytes32 fakeLeaf = keccak256("fakeLeaf");
        bool invalid = registry.verifyInclusion(fakeLeaf, proof, root);
        assertFalse(invalid);
    }
}
