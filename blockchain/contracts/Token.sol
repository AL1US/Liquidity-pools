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
        price = _price;
        initialSupply = _initialSupply;
    }


    function decimals() public pure override returns (uint8) {
        return _decimals;
    }

    function getPrice() public view returns (uint) {
        return price;
    }

    function mint(address to, uint amount) public {
        _mint(to, amount);
    }

    function getPriceInBuyToken(uint _amount) public view returns(uint) {
        return _amount * getPrice();
    }

    // function buyToken()
    function buyToken(uint _amount) public payable {
        // посчитать количество того, сколько пользователь должен заплатить за токен
        uint amount = _amount * 10 ** decimals();
        uint price = getPriceInBuyToken(_amount);

        // проверить, есть ли такое количество токенов у пользователя
        require(msg.value >= price, unicode"У вас не достаточно ETH для покупки данного количества токенов");
        
        if (msg.value > price) {
            payable(msg.sender).transfer(msg.value - price); // переводим остаток обратно, при его наличии
        }

        _mint(msg.sender, amount); // минтим новые токены пользователю
    }

}