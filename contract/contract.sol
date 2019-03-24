pragma solidity ^0.4.25;
pragma experimental ABIEncoderV2;

contract Ownerable {
    address internal _owner;

    constructor() public{
        _owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == _owner);
        _;
    }

    function owner() public view returns (address) {
        return _owner;
    }

    function isOwner() public view returns (bool) {
        return msg.sender == _owner;
    }

    function changeOwnerAddress (address newOwner) public onlyOwner {
        _owner = newOwner;
    }
}

contract SexVerifier is Ownerable {
    event AgreementsReturn(uint[] AgreementsData);
    event SpecialAgreementReturn(uint[] Signatures);
    struct Agreement {
        address[] addresses;
        uint[] signatures;
        uint time;
        uint id;
    }

    modifier onlyActorOwner(address[] addresses) {
        bool _allowed = false;
        for (uint i = 0; i < addresses.length; i++) {
            if (addresses[i] == msg.sender) {
                _allowed = true;
            }
        }
        require(_allowed == true || msg.sender == _owner);
        _;
    }

    uint private mappingSize = 0;
    mapping(uint => Agreement) private _agreements;

    constructor() public Ownerable() {}

    function createAgreement(uint id, address[] addresses, uint[] signatures, uint timestamp) public onlyOwner returns (bool) {
        if (addresses.length != signatures.length) {
            return false;
        } else {
            _agreements[mappingSize] = Agreement(addresses, signatures, timestamp, id);
            mappingSize += 1;
            return true;
        }
    }

    function getSpecialAgreementResult(uint id, address[] addresses, uint timestamp) public onlyActorOwner(addresses) returns (uint[] signatures) {
        for (uint i = 0; i < mappingSize; i++) {
            if (_agreements[i].id == id && timestamp == _agreements[i].time) {
                emit SpecialAgreementReturn(_agreements[i].signatures);
                return (_agreements[i].signatures);
            }
        }
    }

    function getAgreementResult(uint id, address[] addresses) public onlyActorOwner(addresses) returns (uint[]) {
        uint _size = 0;
        for (uint i = 0; i < mappingSize; i++) {
            if ( _agreements[i].id == id) {
                _size += (1 + addresses.length);
            }
        }
        uint[] memory result = new uint[](_size);
        uint elementNum = 0;
        uint j;
        for (i = 0; i < mappingSize; i++) {
            if (_agreements[i].id == id) {
                for (j = 0;j < addresses.length;j++){
                    result[elementNum] = _agreements[i].signatures[j];
                    elementNum += 1;
                }
            }
            result[elementNum] = _agreements[i].time;
            elementNum += 1;
        }
        emit AgreementsReturn(result);
        return result;
    }
}


contract SexVerifier2 is Ownerable {
    event AgreementsReturn(string[] AgreementsData);
    event SpecialAgreementReturn(string[] Signatures);
    struct Agreement {
        address[] addresses;
        string[] signatures;
        uint time;
        uint id;
    }

    modifier onlyActorOwner(address[] addresses) {
        bool _allowed = false;
        for (uint i = 0; i < addresses.length; i++) {
            if (addresses[i] == msg.sender) {
                _allowed = true;
            }
        }
        require(_allowed == true || msg.sender == _owner);
        _;
    }

    uint private mappingSize = 0;
    mapping(uint => Agreement) private _agreements;

    constructor() public Ownerable() {}

    function createAgreement(uint id, address[] addresses, string[] signatures, uint timestamp) public onlyOwner returns (bool) {
        if (addresses.length != signatures.length) {
            return false;
        } else {
            _agreements[mappingSize] = Agreement(addresses, signatures, timestamp, id);
            mappingSize += 1;
            return true;
        }
    }

    function getSpecialAgreementResult(uint id, address[] addresses, uint timestamp) public onlyActorOwner(addresses) returns (string[] signatures) {
        for (uint i = 0; i < mappingSize; i++) {
            if (_agreements[i].id == id && timestamp == _agreements[i].time) {
                emit SpecialAgreementReturn(_agreements[i].signatures);
                return (_agreements[i].signatures);
            }
        }
    }

    function getAgreementResult(uint id, address[] addresses) public onlyActorOwner(addresses) returns (string[]) {
        uint _size = 0;
        for (uint i = 0; i < mappingSize; i++) {
            if ( _agreements[i].id == id) {
                _size += (1 + addresses.length);
            }
        }
        string[] memory result = new string[](_size);
        uint elementNum = 0;
        uint j;
        for (i = 0; i < mappingSize; i++) {
            if (_agreements[i].id == id) {
                for (j = 0;j < addresses.length;j++){
                    result[elementNum] = _agreements[i].signatures[j];
                    elementNum += 1;
                }
            }
        }
        emit AgreementsReturn(result);
        return result;
    }
}
