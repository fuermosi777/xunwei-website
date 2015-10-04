import React from 'react';  
import Router from 'react-router';  
import { DefaultRoute, Link, Route, RouteHandler } from 'react-router';
import createBrowserHistory from 'history/lib/createBrowserHistory';
import HomePage from './pages/HomePage.jsx';
import SecretPage from './pages/SecretPage.jsx';

React.render((
    <Router history={createBrowserHistory()}>
        <Route location="history" path="/" component={HomePage}>
            <Route name="area" path="/area/:category" component={HomePage} />
            <Route name="tag" path="/tag/:tag" component={HomePage} />
            <Route name="post" path="/post/:pid" component={HomePage} />
            <Route name="business" path="/business/:bid" component={HomePage} />
        </Route>
        <Route name="user" path="/secret/" component={SecretPage} />
    </Router>
), document.getElementById('container'));