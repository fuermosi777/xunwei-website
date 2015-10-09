import React from 'react';  
import Router from 'react-router';  
import { DefaultRoute, Link, Route, RouteHandler } from 'react-router';
import createBrowserHistory from 'history/lib/createBrowserHistory';
import HomePage from './pages/HomePage.jsx';
import SecretPage from './pages/SecretPage.jsx';
import FramePage from './pages/FramePage.jsx';
import 'babel-runtime/core-js/promise';

React.render((
    <Router history={createBrowserHistory()}>
        <Route location="history" path="/" component={HomePage}>
            <Route name="post" path="/post/:pid" component={HomePage} />
            <Route name="business" path="/business/:bid" component={HomePage} />
            <Route name="search" path="/search/" component={HomePage} />
            <Route name="tag" path="/tag/:tag" component={HomePage} />
        </Route>
        <Route name="i" path="/i/:pid" component={FramePage} />
        <Route name="user" path="/secret/" component={SecretPage} />
    </Router>
), document.getElementById('container'));