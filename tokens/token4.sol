pragma solidity ^0.8.0;

contract MyToken {
  
  string public constant name = "Token 4";

  string public constant symbol = "ttt";

  uint256 public constant totalSupply = 1000000 * 10**18;

  mapping(address => uint256) public balancesOf;

  mapping(address => mapping(address => uint256)) public allowances;

  event Transfer(address indexed from, address indexed to, uint256 value);

  event Approval(address indexed owner, address indexed spender, uint256 value);

  constructor() {
    balancesOf[msg.sender] = totalSupply;
  }

  function transfer(address recipient, uint256 amount) public returns (bool) {
    require(balancesOf[msg.sender] >= amount, "Insufficient balance");
    balancesOf[msg.sender] -= amount;
    balancesOf[recipient] += amount;
    emit Transfer(msg.sender, recipient, amount);
    return true;
  }

  function transferFrom(address sender, address recipient, uint256 amount) public returns (bool) {
    require(allowances[sender][msg.sender] >= amount, "Insufficient allowance");
    balancesOf[sender] -= amount;
    balancesOf[recipient] += amount;
    allowances[sender][msg.sender] -= amount;
    emit Transfer(sender, recipient, amount);
    return true;
  }

  function approve(address spender, uint256 amount) public returns (bool) {
    allowances[msg.sender][spender] = amount;
    emit Approval(msg.sender, spender, amount);
    return true;
  }

  function balanceOf(address account) public view returns (uint256) {
    return balancesOf[account];
  }

  function allowance(address owner, address spender) public view returns (uint256) {
    return allowances[owner][spender];
  }
}
