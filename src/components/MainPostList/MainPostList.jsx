import React from 'react';
import Style from './MainPostList.less';

export default React.createClass({
    render() {
        let List = this.props.post.map((item, i) => {
            return (
                <li key={i} onMouseOver={this.handlePostMouseOver.bind(this, item)} onMouseLeave={this.handlePostMouseLeave.bind(this, item)}>
                    <div className="left" style={{backgroundImage: `url(${item.business.photo})`}} onClick={this.handlePostClick.bind(this, item)}>
                    </div>
                    <div className="right">
                        <p className="title" onClick={this.handlePostClick.bind(this, item)}>{item.title}</p>
                        <p className="preview" onClick={this.handlePostClick.bind(this, item)}>{item.preview}...</p>
                        <p className="tag">{item.business.tag.map((item2, i2) => {
                            return <span key={i2} className="tag-item" onClick={this.handleTagClick.bind(this, item2)}>{item2.name}</span>;
                        })}</p>
                        <p className="name" onClick={this.handleBusinessClick.bind(this, item.business)}><i className="ion-android-bar"/> {item.business.name}</p>
                        <p className="location"><i className="ion-android-pin"/> {item.business.street} {item.business.city}, {item.business.state} {item.business.postcode}</p>
                    </div>
                </li>
            );
        });
        let Tag = this.props.tag.map((item, i) => {
            return (
                <li key={i} onClick={this.handleTagClick.bind(this, item)}>{item.name}</li>
            );
        });
        return (
            <div className="MainPostList">
                <div className="wrapper">
                    <ul className="tag-list">
                        {Tag}
                    </ul>
                    <ul className="post-list">
                        {List}
                    </ul>
                    <div className="load-more" onClick={this.handleLoadMoreClick}>加载更多</div>
                </div>
            </div>
        );
    },

    handlePostClick(post) {
        this.props.onPostSelect(post);
    },

    handleBusinessClick(business) {
        this.props.onBusinessSelect(business);
    },

    handleTagClick(tag) {
        this.props.onTagSelect(tag);
    },

    handlePostMouseOver(post) {
        this.props.onPostMouseOver(post);
    },

    handlePostMouseLeave(post) {
        this.props.onPostMouseLeave(post);
    },

    handleLoadMoreClick() {
        this.props.onLoadMoreClick();
    }
})