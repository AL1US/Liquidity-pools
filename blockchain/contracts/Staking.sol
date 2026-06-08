// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;


import "./Token.sol";

contract Staking {
    
    Token public profi;

    mapping(address => uint) public stakes;
    mapping(address => uint) public lastRewardTime;
    
    uint public totalStaked;
    uint PRECISION = 1e18;
    
    uint constant public decimals = 10 ** 12;
    uint constant REWARD_PER_SECOND = 13 * decimals;
    
    constructor(Token professionalCoin) {
        profi = professionalCoin;
    }

    // положить на стэйк
    function stake(uint amount) public {
        require(amount > 0, "amount is zero");
        require(
            profi.balanceOf(msg.sender) >= amount,
            unicode"Недастаточно LP(profi) токенов на балансе"
        );
        
        if (stakes[msg.sender] > 0) {
            uint reward = calculateReward();

            if (reward > 0) {
                lastRewardTime[msg.sender] = block.timestamp;
                profi.mint(msg.sender, reward);
            }
        } else {
            lastRewardTime[msg.sender] = block.timestamp;
        }

        stakes[msg.sender] += amount;
        totalStaked += amount;               
        
        profi.transferFrom(msg.sender, address(this), amount);
    }

    // формула для подсчета
    function calculateReward() public view returns(uint) {
        
        // для того чтобы не писать каждый раз stakes[msg.sender]
        uint stakedAmount = stakes[msg.sender];

        // проверка на то не является ли его стэйкинг пустым
        if (stakedAmount == 0 || totalStaked == 0) {
            return 0;
        }

        // всё прошедшее время с последнего момента
        uint timeElapsed = block.timestamp - lastRewardTime[msg.sender];

        // проверка на то не является ли его стэйкинг пустым
        if (timeElapsed == 0) {
            return 0;
        }

        // countLP / allLP + 1
        uint stakeMultiplier = PRECISION + (stakedAmount * PRECISION) / totalStaked;

        // ((timeElapsed / 30 days) * 0.05) + 1
        uint timeMultiplier = PRECISION + ((timeElapsed * 5 * PRECISION) / (100 * 30 days));

        // окончательня награда
        uint reward = (
            stakedAmount *
            timeElapsed *
            REWARD_PER_SECOND *
            stakeMultiplier *
            timeMultiplier
        ) / (PRECISION * PRECISION * decimals);

        return reward;
    }

    // забрать со стэкинга
    function claimReward() public {
        uint reward = calculateReward();
        require(reward > 0, "No reward available");

        lastRewardTime[msg.sender] = block.timestamp;

        profi.mint(msg.sender, reward);
    }
}