import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

//import Blockchain from './Blockchain';
//import ConductTransaction from './ConductTransaction'

import logo from '../assets/logo.png';
import { API_BASE_URL } from '../config.js';


function App() {
  const [walletInfo, setWalletInfo] = useState({});

  useEffect(() => {
    fetch(`${API_BASE_URL}/wallet/info`)
      .then(res => res.json())
      .then(json => setWalletInfo(json))
  }, []);

  return (
    <div className="App">
      <h3>Welcome ot pychain</h3>
      <img className="logo" src={logo} alt="pentagon"/>
      <Link to="/blockchain">Blockchain</Link>
      <Link to="/conduct-transaction">ConductTransaction</Link>
      <Link to="/transaction-pool">TransactionPool</Link>
      <br />
      <div className="WalletInfo">
        <div>Address: {walletInfo.address}</div>
        <div>Balance: {walletInfo.balance}</div>
      </div>
    </div>
  );
}

export default App;
