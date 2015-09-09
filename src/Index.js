import React from 'react';
import { Router, Route, Link } from 'react-router';
import App from './components/App';
import PoweredBy from './components/Powered-by';

window.React = React;

React.render(
  <Router>
    <Route path="/" component={App}>
        <Route path="poweredby" component={PoweredBy}/>
    </Route>
  </Router>
  , document.getElementById('content')
);
