import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { Admin } from './pages/admin/Admin';

export const App = () => (
  <React.Fragment>
    <Router>
      <Switch>
        <Route exact path="/admin" component={Admin} />
      </Switch>
    </Router>
  </React.Fragment>
);
