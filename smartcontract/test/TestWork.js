const Work = artifacts.require("./Work.sol")
const truffleAssert = require('truffle-assertions');

contract('Work', () => {
    it('Should init the Work', async () => {
        const instance = await Work.deployed();
        let balance = await instance.getBalance("shop");
        assert.equal(balance, 0);

    });
    it('The person with not enough money', async () => {
        const instance = await Work.deployed();
        instance.addPerson("buyer2", 50);

        await truffleAssert.reverts(
            instance.buyItem("buyer2", "item1"),
            "Not enough balance"
        );
    });
    it("The item is not avaliable, cause it doesn't exist", async () => {
        const instance = await Work.deployed();
        await truffleAssert.reverts(
            instance.buyItem("buyer1", "hz"),
            "Item not available"
        );
    });
    it('Should sell the item and check the balance', async () => {
        const instance = await Work.deployed();
        instance.buyItem("buyer", "item1");
        // wait for 1 second
        await new Promise(r => setTimeout(r, 1000));

        let balance = await instance.getBalance("shop");
        assert.equal(balance, 100);

        let buyerBalance = await instance.getBalance("buyer");
        assert.equal(buyerBalance, 0);

        assert.equal(balance, 100);
        assert.equal(await instance.getPrice("buyer", "item1"), 100);
    });
    it('The item is not avaliable after buying', async () => {
        const instance = await Work.deployed();
        instance.addPerson("buyer2", 50);

        await truffleAssert.reverts(
            instance.buyItem("buyer2", "item1"),
            "Item not available"
        );
    });
    it('Should sell the item and check the avaliable items', async () => {
        const instance = await Work.deployed();

        await instance.addItem("item2", 20);
        await instance.buyItem("buyer2", "item2");

        // assert.equal(await instance.getPrice("buyer2", "item2"), 20);
        assert.equal(await instance.hasItem("shop", "item2"), false);
        
    });
    it('The person has the item after buying', async () => {
        const instance = await Work.deployed();

        await instance.addItem("item2", 20);
        await instance.buyItem("buyer2", "item2");

        assert.equal(await instance.hasItem("buyer2", "item2"), true);
    });
    it('Check the price of the item', async () => {
        const instance = await Work.deployed();

        assert.equal(await instance.getPrice("buyer2", "item2"), 20);
    });
});