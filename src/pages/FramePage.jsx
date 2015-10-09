import React from 'react';
import Frame from '../components/Frame/Frame.jsx';
import {History, State} from 'react-router';
import ContentService from '../services/ContentService.js';

export default React.createClass({
    mixins: [History, State],

    getInitialState() {
        return {
            post: null
        };
    },

    componentDidMount() {
        let pid = this.props.params.pid || '';
        if (pid) {
            ContentService.getPost(pid).then((res) => {
                this.setState({post: res});
            });
        }
    },

    render() {
        return (
            <div className="FramePage" style={{height: '100%'}}>
                {this.state.post ? <Frame post={this.state.post} /> : ''}
            </div>
        );
    }
 });