import React from 'react';
import Style from './Nav.less';

export default React.createClass({
    render() {
        return (
            <div className="Nav">
                <img className="logo" src={require('./logo.svg')} alt="寻味Logo" onClick={this.handleLogoClick}/>
                <div className="xunwei" onClick={this.handleLogoClick}>
                    <span className="zh">寻味</span>
                    <span className="en"> xun-wei.com</span>
                </div>
                {this.props.location ? 
                <div className="right"> 
                    <span onClick={this.handlePublishClick}><i className="ion-android-create"/>写寻记</span>
                    {this.props.username ? <span onClick={this.handleLogoutClick}><i className="ion-android-exit"/>登出</span> : <span onClick={this.handleAuthClick}><i className="ion-android-happy"/>登录/注册</span>}
                    <span className="location" onClick={this.handleLocationClick}><i className="ion-android-navigate"/>{this.props.location.name}</span>
                </div> : ''}
            </div>
        );
    },

    handleLocationClick() {
        this.props.onLocationSelect();
    },

    handleAuthClick() {
        this.props.onAuthSelect();
    },

    handleLogoClick() {
        window.location = '/';
    },

    handleLogoutClick() {
        this.props.onLogout();
    },

    handlePublishClick() {
        if (this.props.username) {
            this.props.onPublishSelect();
        } else {
            this.props.onAuthSelect();
        }
    }
})