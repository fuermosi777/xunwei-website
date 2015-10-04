import React from 'react';
import Styles from './Loading.less';

export default React.createClass({
    render() {
        return (
            <div className="Loading">
                <div className="wrapper">
                    <img src={require('./oval.svg')} className="spinner"/>
                    <p className="loading">寻味中...</p>
                </div>
            </div> 
        );
    }
});