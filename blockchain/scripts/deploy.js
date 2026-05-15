const { ethers } = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  const Factory = await ethers.getContractFactory("Factory");
  const factory = await Factory.deploy();

  await factory.waitForDeployment();

  const factoryAddress = await factory.getAddress();

  const Router = await ethers.getContractFactory("Router");
  const router = await Router.deploy(factoryAddress);

  await router.waitForDeployment();

  const routerAddress = await router.getAddress();

  const addresses = {
    factory: factoryAddress,
    router: routerAddress,

    tokens: {
      gerdaCoin: await factory.gerdaCoin(),
      krendelCoin: await factory.krendelCoin(),
      rtkCoin: await factory.rtkCoin(),
      professionalCoin: await factory.professionalCoin(),
    },

    pools: {
      poolGerKre: await factory.poolGerKre(),
      poolKreRtk: await factory.poolKreRtk(),
    },

    staking: await factory.staking(),
  };

  const outputDir = path.join(__dirname, "../addresses");
  const filePath = path.join(outputDir, "addresses.json");

  fs.mkdirSync(outputDir, { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(addresses, null, 2));

  console.log("Addresses saved to:", filePath);
  console.log(addresses);
}

main()
  .then(() => {
    process.exitCode = 0;
  })
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });