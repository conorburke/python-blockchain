import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button } from 'react-bootstrap';

import Transaction from './Transaction';
import { API_BASE_URL } from '../config';
import history from '../history';

function TransactionPool() {
  const [transactions, setTransactions] = useState([]);

  const fetchTransactions = () =>  {
    fetch(`${API_BASE_URL}/transactions`)
      .then(res => res.json())
      .then(json => {
        console.log('transactions json', json);
        setTransactions(json);
    })

  }

  useEffect(() => {
//    fetch(`${API_BASE_URL}/transactions`)
//      .then(res => res.json())
//      .then(json => setTransactions(json));

    fetchTransactions();
    const intervalId = setInterval(fetchTransactions, 10000)

    return () => clearInterval(intervalId);
  }, [])

  const fetchMineBlock = () => {
    fetch(`${API_BASE_URL}/blockchain/mine`)
      .then(() => {
        alert('Success');
        history.push('/blockchain');
      })
  }

  return (
    <div className="TransactionPool">
      <Link to="/">Homepage></Link>
      <hr />
      <h3>TransactionPool</h3>
      <div>
        {
          transactions.map(t => {
            return <div key={t.id}>
              <hr />
              <Transaction transaction={t} />
            </div>
          })
        }
      </div>
      <Button
        variant="danger"
        onClick={fetchMineBlock}
      >
      Mine a block of these transactions
      </Button>
    </div>
  )

}

export default TransactionPool;