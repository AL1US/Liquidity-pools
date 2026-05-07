// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;


import "puls/Token.sol";

contract Pool {
    
    string name;
    address token1;
    address token2;

    constructor (string memory _name, address _token_first, address _token_second) {
        name = _name;
        token1 = _token_first;
        token2 = _token_second;
    }

    


}