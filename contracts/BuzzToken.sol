// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;
// Importing OpenZeppelin's ERC-721 Implementation
import 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol';
// Importing OpenZeppelin's SafeMath Implementation
import 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/SafeMath.sol';


contract BuzzToken is ERC721 {
    using SafeMath for uint256;
    struct Buzz {
        uint8 genes;
        uint256 basedId;
        uint256 suitId;
    }
    
    Buzz[] public buzzes;

    // Event that will be emitted whenever a new buzz is created
    event Birth(
        address owner,
        uint256 buzzId,
        uint256 basedId,
        uint256 suitId,
        uint8 genes
    );

    // Initializing an ERC-721 Token named 'Buzzes' with a symbol 'VPR'
    constructor() ERC721("Buzzes", "BMN") public {
    }

    // Fallback function
    fallback() external payable {
    }

    receive() external payable {
        
    }

    /** @dev Function to determine a buzz's characteristics.
      * @param based ID of buzz's based (one parent)
      * @param suit ID of buzz's suit (other parent)
      * @return The buzz's genes in the form of uint8
      */
    function generateBuzzGenes(
        uint256 based,
        uint256 suit
    )
        internal
        pure
        returns (uint8)
    {
        return uint8(based.add(suit)) % 6 + 1;
    }

    /** @dev Function to create a new buzz
      * @param based ID of new buzz's based (one parent)
      * @param suit ID of new buzz's suit (other parent)
      * @param buzzOwner Address of new buzz's owner
      * @return The new buzz's ID
      */
    function createBuzz(
        uint256 based,
        uint256 suit,
        address buzzOwner
    )
        internal
        returns (uint)
    {
        require(buzzOwner != address(0));
        uint8 newGenes = generateBuzzGenes(based, suit);
        Buzz memory newBuzz = Buzz({
            genes: newGenes,
            basedId: based,
            suitId: suit
        });
        buzzes.push(newBuzz);
        uint256 newBuzzId = buzzes.length - 1;
        super._mint(buzzOwner, newBuzzId);
        emit Birth(
            buzzOwner,
            newBuzzId,
            newBuzz.basedId,
            newBuzz.suitId,
            newBuzz.genes
        );
        return newBuzzId;
    }
    
    /** @dev Function to allow user to buy a new buzz (calls createBuzz())
      * @return The new buzz's ID
      */
    function buyBuzz() external payable returns (uint256) {
        require(msg.value == 0.02 ether);
        return createBuzz(0, 0, msg.sender);
    }
    
    /** @dev Function to Create 2 buzzes to create a new one
      * @param basedId ID of new buzz's based (one parent)
      * @param suitId ID of new buzz's suit (other parent)
      * @return The new buzz's ID
      */
    function CreateBuzzs(uint256 basedId, uint256 suitId) external payable returns (uint256) {
        require(msg.value == 0.05 ether);
        return createBuzz(basedId, suitId, msg.sender);
    }
    
    /** @dev Function to retrieve a specific buzz's details.
      * @param buzzId ID of the buzz who's details will be retrieved
      * @return An array, [buzz's ID, buzz's genes, based's ID, suit's ID]
      */
    function getBuzzDetails(uint256 buzzId) external view returns (uint256, uint8, uint256, uint256) {
        Buzz storage buzz = buzzes[buzzId];
        return (buzzId, buzz.genes, buzz.basedId, buzz.suitId);
    }
    
    /** @dev Function to get a list of owned buzzes' IDs
      * @return A uint array which contains IDs of all owned buzzes
      */
    function ownedBuzzs() external view returns(uint256[] memory) {
        uint256 buzzCount = balanceOf(msg.sender);
        if (buzzCount == 0) {
            return new uint256[](0);
        } else {
            uint256[] memory result = new uint256[](buzzCount);
            uint256 totalBuzzs = buzzes.length;
            uint256 resultIndex = 0;
            uint256 buzzId = 0;
            while (buzzId < totalBuzzs) {
                if (ownerOf(buzzId) == msg.sender) {
                    result[resultIndex] = buzzId;
                    resultIndex = resultIndex.add(1);
                }
                buzzId = buzzId.add(1);
            }
            return result;
        }
    }
}
