import React from 'react';
import Style from './MainPostList.less';

export default React.createClass({
    getInitialState() {
        return {
            keyword: ''
        };
    },

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
                    <div className="search-box">
                        {this.state.keyword ? '' : <label>开始搜索: 中餐、火锅、汉堡...</label>}
                        <input className="keyword-input" type="text" autocomplete="off" onChange={this.handleKeywordChange} onKeyDown={this.handleKeywordKeyDown}/>
                        <i className="ion-android-search search-button" onClick={this.handleSearch}/>
                    </div>
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

    handleKeywordChange(e) {
        this.setState({keyword: e.target.value});
    },

    handleKeywordKeyDown(e) {
        if (e.keyCode === 13) {
            this.handleSearch();
        }
    },

    handleSearch() {
        if (!this.state.keyword) return;
        this.props.onSearch(this.state.keyword);
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