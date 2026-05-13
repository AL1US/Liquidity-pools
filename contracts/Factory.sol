// contracts/GLDToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "./Token.sol";
import "./Pools.sol";

contract Factory {

    // token objects
    Token public gerdaCoin;
    Token public krendelCoin;
    Token public rtkCoin;
    Token public professionalCoin;

    // poll objects
    Pool public poolGerKre;  
    Pool public poolKreRtk;


    struct user {
        string name;
    }

    mapping (address => user) public users;

    uint decimals = 12;


    constructor() {
        gerdaCoin = new Token("GerdaCoin", "GERDA", 100_000, 1);
        krendelCoin = new Token("KrendelCoin", "KRENDEL", 150_000, 2);
        rtkCoin = new Token("RTKCoin", "RTK", 300_000, 3);
        professionalCoin = new Token("Professional", "PROFI", 0, 6);

        // создание пользователей
        users[0x5B38Da6a701c568545dCfcB03FcB875f56beddC4] = user("Tom");
        users[0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2] = user("Ben");
        users[0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB] = user("Rick");

        gerdaCoin.transfer(address(0x5B38Da6a701c568545dCfcB03FcB875f56beddC4), 10000 * 10 ** 12);

        // создание пулов
        poolGerKre = new Pool(
            "poolGerKre",
            0x5B38Da6a701c568545dCfcB03FcB875f56beddC4,
            gerdaCoin,
            krendelCoin,
            professionalCoin
        ); // владелец том
        poolKreRtk = new Pool(
            "poolKreRtk",
            0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2,
            krendelCoin,
            rtkCoin,
            professionalCoin
        ); // владелец бен

        // перевод токенов в пулы
        gerdaCoin.transfer(address(poolGerKre), 50000 * 10 ** 12);
        krendelCoin.transfer(address(poolGerKre), 50000 * 10 ** 12);
        rtkCoin.transfer(address(poolKreRtk), 50000 *10 ** 12);
        krendelCoin.transfer(address(poolKreRtk), 50000 * 10 ** 12);
    }

}