// SPDX-License-Identifier: MIT
pragma solidity >=0.4.25 <0.9.0;

contract Work {
    // create a map for items with fields name, price
    struct Item {
        string name;
        uint price;
    }

    // create a map for people with fields name, balance, and items
    struct Person {
        uint balance;
        uint itemsCount;
        mapping(string => Item) items;
    }

    // 2 maps for people and items
    mapping(string => Person) people;

    constructor() {
        // init the shop people with 0 balance and 3 items
        people["shop"].balance = 0;
        people["shop"].items["item1"] = Item("item1", 100);
        people["shop"].itemsCount = 1;

        // init the buyer people with 100 balance and 0 items
        addPerson("buyer", 100);
    }

    function addPerson(string memory name, uint balance) public {
        // let's guess that the person doesn't have any items
        people[name].balance = balance;
        people[name].itemsCount = 0;
    }

    function addItem(string memory itemName, uint price) public {
        // add an item to the shop
        people["shop"].items[itemName] = Item(itemName, price);
    }

    function addItem(string memory name, string memory itemName, uint price) public {
        // add an item to the person
        people[name].items[itemName] = Item(itemName, price);
    }

    // check if the person has the item
    function hasItem(string memory name, string memory itemName) public view returns (bool) {
        return people[name].items[itemName].price > 0;
    }

    // function to get the balance of a person
    function getBalance(string memory _name) public view returns (uint) {
        return people[_name].balance;
    }

    function increaseBalance(string memory name, uint amount) public {
        people[name].balance += amount;
    }

    function getPrice(string memory itemName) public view returns (uint) {
        return people["shop"].items[itemName].price;
    }

    function getPrice(string memory name, string memory itemName) public view returns (uint) {
        return people[name].items[itemName].price;
    }

    function buyItem(string memory buyer, string memory itemName) public {
        // check if the item is available
        require(people["shop"].items[itemName].price > 0, "Item not available");

        // get the price of the item
        uint price = people["shop"].items[itemName].price;

        // check if the buyer has enough balance
        require(people[buyer].balance >= price, "Not enough balance");

        // deduct the price from the buyer's balance
        people[buyer].balance -= price;

        // add the price to the shop's balance
        people["shop"].balance += price;

        // add the item to the buyer's items
        people[buyer].items[itemName] = Item(itemName, price);

        // remove the item from the shop's items
        delete people["shop"].items[itemName];
    }
}