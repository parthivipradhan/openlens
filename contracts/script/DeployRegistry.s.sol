// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "../src/EvidenceRegistry.sol";

interface Vm {
    function startBroadcast() external;
    function stopBroadcast() external;
}

contract DeployRegistry {
    Vm internal constant vm = Vm(address(uint160(uint256(keccak256("hevm cheat code")))));

    function run() external returns (EvidenceRegistry) {
        vm.startBroadcast();
        EvidenceRegistry registry = new EvidenceRegistry();
        vm.stopBroadcast();
        return registry;
    }
}
