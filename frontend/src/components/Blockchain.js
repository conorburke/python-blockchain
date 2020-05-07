import React, { useState, useEffect } from 'react';
import { Button } from 'react-bootstrap';
import {Link} from 'react-router-dom';

import Block from './Block';

import { API_BASE_URL } from '../config.js';

const PAGE_RANGE = 3;

function Blockchain() {
    const [blockchain, setBlockchain] = useState([]);
    const [blockchainLength, setBlockchainLength] = useState(0);

    const fetchBlockchainPage = ({ start, end }) => {
      fetch(`${API_BASE_URL}/blockchain/range?start=${start}&end=${end}`)
          .then(res => res.json())
          .then(json => setBlockchain(json));
    }

    useEffect(() => {
//        fetch(`${API_BASE_URL}/blockchain`)
//          .then(res => res.json())
//          .then(json => setBlockchain(json));

        fetchBlockchainPage({start: 0, end: PAGE_RANGE });


         fetch(`${API_BASE_URL}/blockchain/length`)
          .then(res => res.json())
          .then(json => setBlockchainLength(json));
    }, []);

    const buttonNumbers = [];
    for (let i=0; i<Math.ceil(blockchainLength/PAGE_RANGE); i++) {
      buttonNumbers.push(i)
    }

    return (
      <div className="Blockchain">
        <h3>Blockchain</h3>
        <Link to="/">Homepage</Link>
        <br />
        <Link to="/conduct-transaction">ConductTransaction</Link>
        <div>
          {blockchain.map(block => {
            return <Block key={block.hash} block={block} />
          })}
        </div>
        <div>
          {
            buttonNumbers.map(number => {
              const start = number * PAGE_RANGE;
              const end = (number+1) * PAGE_RANGE;

              return (
                <span key={number} onClick={() => fetchBlockchainPage({ start, end })}>
                  <Button size="sm" variant="danger">
                    {number+1}
                  </Button>{' '}
                </span>
              )
            })
          }
        </div>
      </div>
    )
}

export default Blockchain;