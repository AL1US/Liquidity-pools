// берём, туда сюда делаем, и токены обмениваются

// основной обмен должен просиходит тут или через контракт pols. 
// как обойти штуку что отправителем становится контракт, а не юзер (только если в функцию передавать отправителя?)

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
        address middleToken, // промежуточный токен. Например GERDA -> KRENDEL -> RTK
        address tokenOut,
        uint amount
    ) public {
        Pool firstPool = findPool(tokenIn, middleToken);
        Pool secondPool = findPool(middleToken, tokenOut);

        require(address(firstPool) != address(0), "first pool not found"); // address(0) - иcпользуется как "ничего не найден"
        require(address(secondPool) != address(0), "second pool not found");

        // меняем токен обмена на промежуточный токен
        // отправляем промежуточный токен на адрес роутера
        uint middleAmount = firstPool.swapFrom( // не испольуем апрув, потомучто владелец сам должен его дать
            msg.sender,
            tokenIn,
            amount,
            address(this)
        ); 

        // даём апрув на то, чтобы пул мог забрать токен у роутера
        Token(middleToken).approve(address(secondPool), middleAmount); // апрув именно для контракта

        // меняем промежуточный токен на окончательный
        secondPool.swapFrom(
            address(this),
            middleToken,
            middleAmount / 10 ** Token(middleToken).decimals(),
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