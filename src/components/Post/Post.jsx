import React from 'react';
import Style from './Post.less';
import ContentService from '../../services/ContentService.js';
import AuthStore from '../../stores/AuthStore.js';

export default React.createClass({
    getInitialState() {
        return {
            starNum: 0
        };
    },

    componentDidMount() {
        ContentService.getPostStarNum(this.props.data.id).then((res) => {
            this.setState({starNum: res.star_num});
        });
    },
    render() {
        return (
            <div className="Post">
                <div className="wrapper">
                    <p className="title">{this.props.data.title}</p>
                    <div className="meta">
                        <p className="name"><img src={this.props.data.business.photo}/>{` ${this.props.data.business.name} ${this.props.data.business.name2}`}</p>
                        <p className="tags">
                        {this.props.data.business.tag.map((item, i) => {
                            return <span className="tag" key={i}>{item.name}</span>
                        })}
                        </p>
                        {this.props.data.source ? <p className="read-source"><a href={this.props.data.source} target="_blank">本文来自 {this.props.data.source.substring(0, 30)} ...</a></p> : ''}
                    </div>
                    <div className="body" dangerouslySetInnerHTML={{__html: this.props.data.body}}/>
                    <div className="star" onClick={this.handleStarClick}>
                        <i className="ion-android-star"/>
                        <span> 喜欢 | {this.state.starNum}</span>
                    </div>
                    {this.props.data.source ? <a className="source" href={this.props.data.source} target="_blank">阅读原文</a> : ''}
                    {this.props.data.source ? <p className="copy">本文为机器自动抓取于网络，根据<a href="http://creativecommons.org/">CC2.5</a>分发，若您认为本文侵犯了您的版权，请联系我们</p> : ''}
                </div>
                <span className="close" onClick={this.handleCloseClick}><i className="ion-android-close"></i></span>
            </div>
        );
    },

    handleCloseClick() {
        this.props.onCloseClick();
    },

    handleStarClick() {
        let token = AuthStore.getToken();
        if (!token) {
            this.props.onStarFail();
        } else {
            ContentService.starPost(this.props.data.id, token).then((res) => {
                this.setState({starNum: res.star_num});
            });
        }
    }
})