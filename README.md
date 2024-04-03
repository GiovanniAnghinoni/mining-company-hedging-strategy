# Mining Company Hedging Strategy
This repository provides a series of coding scripts used to develop a model which can be used by a cryptocurrency mining company in order to hedge itself against rising energy prices. In particular, this strategy could be implemented by a mining firm that produces its own energy. One important feature of this model is the fact that it can be applied to a wide range of different energy sources, given the fact that it uses a versatile tool such as the Raspberry Pi.
## Description
The scenario used to develop this project is the following: given the energy crisis that affected mainly the European Union starting from 2022, a cryptocurrency mining company decided to shift from paying an electricity provider for its energy demand to producing its own electricity; this strategy was taken into account given its obvious advantages in terms of the company's expenses reduction. The main issue characterizing this approach regards the upfront costs that the firm should face in building the necessary structure for producing electricity; furthermore, in the beginning the electricity produced would not be enough to satisfy the necessary energy amount for mining the cryptos. 

To tackle this last issue, a smart contract is provided. Given a certain quantity of electricity produced, the mining company can receive a compensation in terms of Ether: if the pre-specified threshold is not met, then, given that all the other conditions are respected, a certain amount of Ether is sent from the smart contract to the mining company's address; while, in the opposite case, the Ethers remain in the smart contract. Additionally, a withdraw function is present in order for the insurance company to retrieve the Ether amount still present in the smart contract (for example by the end of each month).

To conclude, the electricity values can be obtained through the use of a Raspberry Pi, which can be applied to many different sensors.
## Softwares
The following softwares were used to create, deploy and run the coding scripts:
Application | Software
-------- | --------
Smart contract creation and deployment | Solidity
Obtainment of the Raspberry Pi values | Python
Smart contract test in Ganache | Python
## Credits
* Giovanni Anghinoni <anghinonigiova@gmail.com>
## References
Antonopoulos, A. M., Wood, G. (2019). Mastering Ethereum. O’Reilly.

Monk, S. (2023). Raspberry Pi Cookbook. O’Reilly.

Spanner, G. (2017). Franzis Raspberry Pi Maker Kit Sensoren Handbuch. Franzis.
