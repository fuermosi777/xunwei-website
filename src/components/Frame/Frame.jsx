import React from 'react';
import Styles from './Frame.less';
import $ from 'jquery';

export default React.createClass({
    getInitialState() {
        return {
            showSource: true
        };
    },

    render() {
        return (
            <div className="Frame">
                {this.state.showSource && this.props.post.source ? 
                <div className="frame">
                    <iframe src={this.props.post.source} frameBorder="0" ref="iframe"/>
                    <div className="banner">
                        <button className="read" onClick={this.handleReadClick}>阅读模式</button>
                    </div>
                </div> 
                :
                <div className="post">
                    <p className="title">{this.props.post.title}</p>
                    <div className="body" dangerouslySetInnerHTML={{__html: this.props.post.body}}/>
                </div>
                }
            </div>
        );
    },

    handleReadClick() {
        this.setState({
            showSource: false
        });
    }
})