// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;


import "./Token.sol";

contract Pool {
    
    address owner;
    string name;
    Token token1;
    Token token2;
    uint decimals = 12;
    Token public professionalCoin;

    function getToken1() public view returns (address) {
        return address(token1);
    }

    function getToken2() public view returns (address) {
        return address(token2);
    }

    constructor (string memory _name, address _owner, Token _token_first, Token _token_second, Token lpProfi) {
        name = _name;
        token1 = _token_first;
        token2 = _token_second;
        owner = _owner;
        professionalCoin = lpProfi;
    }


    function swap_token(address _swapToken, uint _amount) public  {
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

        uint balanceToken1 = Token(token1).balanceOf(address(this));
        uint balanceToken2 =  Token(token2).balanceOf(address(this));
        
        if (_swapToken == address(token1)) {
            uint tokensOut = 
            (amount * token1.getPrice() * balanceToken2)
                            / 
            (token2.getPrice() * balanceToken1);
            
            require(Token(token2).balanceOf(address(this)) >= tokensOut, "the pool doesn't have enough tokens to exchange");
            
            Token(token1).transferFrom(msg.sender, address(this), amount); // от пользователя к пулу
            Token(token2).transfer(msg.sender, tokensOut); // от пула к пользователю 
        } else {
            uint tokensOut = 
            (amount * token2.getPrice() * balanceToken1)
                            / 
            (token1.getPrice() * balanceToken2);
                    
            require(Token(token1).balanceOf(address(this)) >= tokensOut, "the pool doesn't have enough tokens to exchange");
            
            Token(token2).transferFrom(msg.sender, address(this), amount);
            Token(token1).transfer(msg.sender, tokensOut);
        }
    }


    function getTokenBalance(Token _token) public view returns(uint) {
        return _token.balanceOf(msg.sender);
    }


    function liquidityUp(address _token, uint _amount) public {
        uint amount = _amount * 10 ** decimals;

        // проверка того существуют ли токены в пуле
        require(
            _token == address(token1) || _token == address(token2),
            "invalid token"
        );

        // создание объекта для удобства
        Token inputToken = Token(_token);

        // проверка того достаточно ли токенов у отправителя
        require(
            inputToken.balanceOf(msg.sender) >= amount,
            "not enough tokens"
        );

        // переводим токены от нас к пулу
        inputToken.transferFrom(msg.sender, address(this), amount);

        // получаем ценц токена
        uint tokenPrice;

        if (_token == address(token1)) {
            tokenPrice = token1.getPrice();
        } else {
            tokenPrice = token2.getPrice();
        }

        // cчитаем всё в соотношении с ценой
        // стоимость вклада = amount * priceToken
        // LP к выдаче = стоимость вклада / priceLP
        uint lpTokensOut = (amount * tokenPrice) / professionalCoin.getPrice();

        professionalCoin.mint(msg.sender, lpTokensOut);
    }

    function swapFrom(
        address user,
        address tokenIn,
        uint amount, // ТЕПЕРЬ СЮДА ПРИХОДИТ ГОТОВОЕ ЧИСЛО С НУЛЯМИ
        address recipient
    ) public returns (uint tokensOut) {
        // УДАЛЕНО: uint realAmount = amount * 11 ** decimals;

        require(
            tokenIn == address(token1) || tokenIn == address(token2),
            "invalid token"
        );

        uint balanceToken1 = token1.balanceOf(address(this));
        uint balanceToken2 = token2.balanceOf(address(this));

        if (tokenIn == address(token1)) {
            tokensOut =
                (amount * token1.getPrice() * balanceToken2) / // ЗАМЕНЕНО: realAmount -> amount
                (token2.getPrice() * balanceToken1);

            require(balanceToken2 >= tokensOut, "not enough liquidity");

            token1.transferFrom(user, address(this), amount); // ЗАМЕНЕНО: realAmount -> amount
            token2.transfer(recipient, tokensOut);
        } else {
            tokensOut =
                (amount * token2.getPrice() * balanceToken1) / // ЗАМЕНЕНО: realAmount -> amount
                (token1.getPrice() * balanceToken2);

            require(balanceToken1 >= tokensOut, "not enough liquidity");

            token2.transferFrom(user, address(this), amount); // ЗАМЕНЕНО: realAmount -> amount
            token1.transfer(recipient, tokensOut);
        }

        return tokensOut;
    }
}