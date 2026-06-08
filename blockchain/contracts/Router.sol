// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "./Factory.sol";
import "./Pools.sol";
import "./Token.sol";

contract Router {
    Factory public factory;

    constructor(Factory _factory) {
        factory = _factory;
    }

    function swapTwoPools(
        address tokenIn,
        address middleToken,
        address tokenOut,
        uint amount
    ) public {
        // ДОБАВЛЕНО: Сразу скейлим число с фронта до нужных нулей
        uint realAmount = amount * 10 ** 12; 

        Pool firstPool = findPool(tokenIn, middleToken);
        Pool secondPool = findPool(middleToken, tokenOut);

        require(address(firstPool) != address(0), "first pool not found"); 
        require(address(secondPool) != address(0), "second pool not found");

        uint middleAmount = firstPool.swapFrom(
            msg.sender,
            tokenIn,
            realAmount, // ПЕРЕДАЕМ УЖЕ С НУЛЯМИ
            address(this)
        ); 

        Token(middleToken).approve(address(secondPool), middleAmount); 

        secondPool.swapFrom(
            address(this),
            middleToken,
            middleAmount, // ПЕРЕДАЕМ КАК ЕСТЬ (УЖЕ С НУЛЯМИ ИЗ ПЕРВОГО ПУЛА)
            msg.sender
        );
    }

    function findPool(address tokenA, address tokenB) public view returns (Pool) {
        Pool[] memory pools = factory.getPools(); // массив всев пулов для удобного поиска
        
        // если в пуле есть tokenA и tokenB в любом порядке — вернуть этот пул
        for (uint i = 0; i < pools.length; i++) {
            address t1 = pools[i].getToken1();
            address t2 = pools[i].getToken2();
            
            if (
                (t1 == tokenA && t2 == tokenB) ||
                (t1 == tokenB && t2 == tokenA)
            ) {
                return pools[i];
            }
        }

        return Pool(address(0)); // если такого нету, то возвращаем пустой адрес
    }
}