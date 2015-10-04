import React from 'react';
import Styles from './Auth.less';
import AuthService from '../../services/AuthService.js';

export default React.createClass({
    getInitialState() {
        return {
            email: '',
            emailValidate: null,
            username: '',
            usernameValidate: null,
            password: '',
            passwordValidate: null,
            showPassword: false,
            mode: null,
            error: ''
        };
    },

    render() {
        return (
            <div className="Auth">
                <div className="wrapper">
                    <p className="title">寻找海外中国人自己的味道</p>
                    <p className="subtitle">登录或注册寻味以便发布你的寻味经历，或者收藏别人的寻记</p>
                    <div className="form">
                        <div className="email">
                            {this.state.email ? '' : <label>Email</label>}
                            <input type="text" onChange={this.handleEmailInputChange}/>
                            {this.state.email && !this.state.showPassword ? <button className="goon" onClick={this.handleGoOnClick}>继续 <i className="ion-android-arrow-forward"/></button> : ''}
                            {this.state.emailValidate === false ? <span className="error"><i className="ion-android-close"/></span> : ''}
                            {this.state.emailValidate === true ? <span className="correct"><i className="ion-android-done"/></span> : ''}
                        </div>
                        {this.state.showPassword && this.state.mode === '注册' ? 
                        <div className="username">
                            {this.state.username ? '' : <label>显示的名字</label>}
                            <input type="text" onChange={this.handleUsernameInputChange} onBlur={this.handleUsernameInputBlur}/>
                            {this.state.usernameValidate === false ? <span className="error"><i className="ion-android-close"/></span> : ''}
                            {this.state.usernameValidate === true ? <span className="correct"><i className="ion-android-done"/></span> : ''}
                        </div> : ''}
                        {this.state.showPassword ? 
                        <div className="password">
                            {this.state.password ? '' : <label>密码</label>}
                            <input type="password" onChange={this.handlePasswordInputChange}/>
                            {this.state.password ? <button className="goon" onClick={this.handleSubmitClick}>{this.state.mode} <i className="ion-android-arrow-forward"/></button> : ''}
                            {this.state.passwordValidate === false ? <span className="error"><i className="ion-android-close"/></span> : ''}
                            {this.state.passwordValidate === true ? <span className="correct"><i className="ion-android-done"/></span> : ''}
                        </div> : ''}
                    </div>
                    <p className="error">{this.state.error}</p>
                </div>
                <i className="ion-android-close close" onClick={this.handleCloseClick}/>
            </div>
        );
    },

    handleLocationClick(l) {
        this.props.onLocationSelect(l);
    },

    handleEmailInputChange(e) {
        this.setState({
            email: e.target.value,
            emailValidate: null,
            username: '',
            usernameValidate: null,
            password: '',
            passwordValidate: null,
            showPassword: false
        });
    },

    handleUsernameInputChange(e) {
        this.setState({
            username: e.target.value,
            usernameValidate: null
        });
    },

    handleUsernameInputBlur() {
        this.validateUsername().catch((err) => {
        });
    },

    handlePasswordInputChange(e) {
        this.setState({
            password: e.target.value,
            passwordValidate: null
        });
    },

    handleGoOnClick() {
        this.validateEmail().then(() => {
            return AuthService.checkUserExists(this.state.email);
        }).then((res) => {
            let mode = res.status ? '登录' : '注册';
            this.setState({
                showPassword: true,
                mode: mode
            });
        }).catch((err) => {
        });
    },

    handleSubmitClick() {
        this.validatePassword().then(() => {
            return this.validateEmail();
        }).then(() => {
            return this.validateUsername();
        }).then(() => {
            if (this.state.mode === '登录') {
                return AuthService.login(this.state.email, this.state.password);
            } else if (this.state.mode === '注册') {
                return AuthService.signup(this.state.email, this.state.password, this.state.username);
            } else {
                return;
            }
        }).then((res) => {
            if (res.status) {
                this.props.onSuccess(res.username, res.token);
            } else {
                this.setState({error: '密码不正确'});
            }
        }).catch((err) => {
        });
    },

    validateEmail() {
        return new Promise((resolve, reject) => {
            let re = /\S+@\S+\.\S+/;
            if (re.test(this.state.email)) {
                this.setState({emailValidate: true}, () => {
                    resolve();
                });
            } else {
                this.setState({emailValidate: false}, () => {
                    reject();
                });
            }
        });
    },

    validatePassword() {
        return new Promise((resolve, reject) => {
            if (this.state.password.length >= 6) {
                this.setState({passwordValidate: true}, () => {
                    resolve();
                });
            } else {
                this.setState({passwordValidate: false}, () => {
                    reject();
                });
            }
        });
    },

    validateUsername() {
        return new Promise((resolve, reject) => {
            if (this.state.mode === '登录') {
                resolve();
            }
            if (this.state.username.length >= 2) {
                this.setState({usernameValidate: true}, () => {
                    resolve();
                });
            } else {
                this.setState({usernameValidate: false}, () => {
                    reject();
                });
            }
        });
    },

    handleCloseClick() {
        this.props.onClose();
    }
});