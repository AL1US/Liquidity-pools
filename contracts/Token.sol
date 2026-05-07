// contracts/GLDToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Token is ERC20 {

    uint8 constant _decimals = 12;
    uint price;
    uint initialSupply;

    constructor(string memory _name, string memory _symbol, uint _initialSupply, uint _price) ERC20(_name, _symbol) {
        _mint(msg.sender, _initialSupply * 10 ** _decimals);
        price = _price * 10 ** 18;
        initialSupply = _initialSupply;
    }

}