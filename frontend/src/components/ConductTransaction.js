import React, { useState, useEffect } from 'react';
import {FormGroup, FormControl, Button } from 'react-bootstrap';
import {Link} from 'react-router-dom';

import { API_BASE_URL } from '../config';
import history from '../history';

function ConductTransaction() {
  const [amount, setAmount] = useState(0);
  const [recipient, setRecipient] = useState('');
  const [knownAddresses, setKnownAddresses] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE_URL}/known-addresses`)
      .then(res => res.json())
      .then(json => setKnownAddresses(json))
  }, []);

  const updateRecipient = (e) => {
    setRecipient(e.target.value);
  }

  const updateAmount = (e) => {
    setAmount(Number(e.target.value));
  }

  const submitTransaction = () => {
    fetch(`${API_BASE_URL}/wallet/transact`,
      { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({recipient, amount})})
      .then(res => res.json())
      .then(json => {
        console.log('submit transaction json', json);
        alert('Success!');
        history.push('/transaction-pool');
      })
  }

  return (
    <div className="ConductTransaction">
      <h3>Conduct a Transaction</h3>
        <Link to="/">Homepage</Link>
        <br />
        <Link to="/blockchain">Blockchain</Link>
      <br />
      <FormGroup>
        <FormControl
          input="text"
          placeholder="recipient"
          value={recipient}
          onChange={updateRecipient}
        />
      </FormGroup>
      <FormGroup>
        <FormControl
          input="number"
          placeholder="amount"
          value={amount}
          onChange={updateAmount}
        />
      </FormGroup>
      <div>
        <Button
          variant="danger"
          onClick={submitTransaction}
        >
          Submit
        </Button>
      </div>
      <br />
      <h4>Known Address</h4>
      <div>
        {
          knownAddresses.map((ka, i) => (
            <span key={ka}><u>{ka}</u>{i !== ka.length - 1 ? ', ' : ''}</span>
          ))
        }
      </div>
    </div>

  )
}

export default ConductTransaction;