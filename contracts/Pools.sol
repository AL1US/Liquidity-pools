// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;


import "puls/Token.sol";
import "puls/Factory.sol";

contract Pool {
    
    address owner;
    string name;
    Token token1;
    Token token2;
    uint decimals = 12;

    constructor (string memory _name, address _owner, Token _token_first, Token _token_second) {
        name = _name;
        token1 = _token_first;
        token2 = _token_second;
        owner = _owner;
    }


    function swap_token(address _swapToken, address _pool, uint _amount) public  {
        uint amount = _amount * 10 ** uint(decimals);

        // проверка на то есть ли такое кол-во токенов у пользователя
        require(
            Token(_swapToken).balanceOf(msg.sender) >= amount,
            unicode"вы не можете поменять больше токенов, чем у вас в ноличии"
        );
        
        // проверка на то есть ли такие токены в пуле
        require(
            _swapToken == address(token1) || _swapToken == address(token2),
            "invalid token"
        );

        uint balanceToken1 = Token(token1).balanceOf(_pool);
        uint balanceToken2 =  Token(token2).balanceOf(_pool);
        
        if (_swapToken == address(token1)) {
            uint tokensOut = 
            (amount * token1.getPrice() * balanceToken2)
                            / 
            (token2.getPrice() * balanceToken1);
            
            require(Token(token2).balanceOf(_pool) >= tokensOut, "the pool doesn't have enough tokens to exchange");
            
            Token(token1).transferFrom(msg.sender, _pool, amount); // от пользователя к пулу
            Token(token2).transfer(msg.sender, tokensOut); // от пула к пользователю 
        } else {
            uint tokensOut = 
            (amount * token2.getPrice() * balanceToken1)
                            / 
            (token1.getPrice() * balanceToken2);
                    
            require(Token(token1).balanceOf(_pool) >= tokensOut, "the pool doesn't have enough tokens to exchange");
            
            Token(token2).transferFrom(msg.sender, _pool, amount);
            Token(token1).transfer(msg.sender, tokensOut);
        }
    }

    // поддержка ликвидности

}