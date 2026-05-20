// contracts/GLDToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "./Token.sol";
import "./Pools.sol";
import "./Staking.sol";
import "./Router.sol";


contract Factory {

    // token objects
    Token public gerdaCoin;
    Token public krendelCoin;
    Token public rtkCoin;
    Token public professionalCoin;

    // poll objects
    Pool public poolGerKre;  
    Pool public poolKreRtk;

    Staking public staking;

    Router public router;

    struct user {
        string name;
        bool exists;
    }

    mapping (address => user) public users;

    uint decimals = 12;

    Pool[] public pools;

    function getPools() public view returns (Pool[] memory) {
        return pools;
    }

    function register(address _address, string memory _name) public {
        require(!users[_address].exists, "this user already exist");

        users[_address] =  user(_name, true);        
    }

    function getMyData()


    constructor() {
        gerdaCoin = new Token("GerdaCoin", "GERDA", 100_000, 1 ether);
        krendelCoin = new Token("KrendelCoin", "KRENDEL", 150_000, 15e17);
        rtkCoin = new Token("RTKCoin", "RTK", 300_000, 3 ether);
        professionalCoin = new Token("Professional", "PROFI", 0, 6 ether);
        
        staking = new Staking(professionalCoin);   

        // создание пользователей remix
        // address tom = 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4;
        // address ben = 0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2;
        // address rick = 0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB;

        // hardhat
        address tom = 0x70997970C51812dc3A010C7d01b50e0d17dc79C8;
        address ben = 0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC;
        address rick = 0x90F79bf6EB2c4f870365E785982E1f101E93b906;

        users[tom] = user("Tom", true);
        users[ben] = user("Ben", true);
        users[rick] = user("Rick", true);

        uint tokenAmount = 10000 * 10 ** 12;

        // перевод токенов
        gerdaCoin.transfer(tom, tokenAmount);
        krendelCoin.transfer(tom, tokenAmount);
        rtkCoin.transfer(tom, tokenAmount);

        gerdaCoin.transfer(ben, tokenAmount);
        krendelCoin.transfer(ben, tokenAmount);
        rtkCoin.transfer(ben, tokenAmount);

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

        // пуш пуллов в массив
        pools.push(poolGerKre);
        pools.push(poolKreRtk);

        // перевод токенов в пулы
        
        // GERDA-KRENDEL: 1500 ETH : 1500 ETH
        gerdaCoin.transfer(address(poolGerKre), 1500 * 10 ** 12);
        krendelCoin.transfer(address(poolGerKre), 1000 * 10 ** 12);

        // KRENDEL-RTK: 3000 ETH : 3000 ETH
        krendelCoin.transfer(address(poolKreRtk), 2000 * 10 ** 12);
        rtkCoin.transfer(address(poolKreRtk), 1000 * 10 ** 12);
    }

}