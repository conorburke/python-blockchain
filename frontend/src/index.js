import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Switch, Route } from 'react-router-dom';


import './index.css';
import history from './history';
import App from './components/App';
import Blockchain from './components/Blockchain';
import ConductTransaction from './components/ConductTransaction';
import TransactionPool from './components/TransactionPool';


import * as serviceWorker from './serviceWorker';


ReactDOM.render(
  <Router history={history}>
    <Switch>
      <Route exact path='/' component={App} />
      <Route path='/blockchain' component={Blockchain} />
      <Route path='/conduct-transaction' component={ConductTransaction} />
      <Route path='/transaction-pool' component={TransactionPool} />
    </Switch>
  </Router>,
//  <React.StrictMode>
//    <App />
//  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
