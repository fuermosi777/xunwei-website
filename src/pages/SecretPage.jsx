import React from 'react';
import AdminPostEditor from '../components/AdminPostEditor/AdminPostEditor.jsx';
import {History, State} from 'react-router';

export default React.createClass({
    mixins: [History, State],

    componentDidMount() {
    },

    render() {
        return (
            <div className="UserPage">
                <AdminPostEditor/>
            </div>
        );
    }
 });