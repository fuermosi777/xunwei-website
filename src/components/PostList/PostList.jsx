import React from 'react';
import Style from './PostList.less';

export default React.createClass({
    render() {
        let List = this.props.post.map((item, i) => {
            return (
                <li key={i} onClick={this.handlePostClick.bind(this, item)}>
                    <p className="title">{item.title}</p>
                    <div className="preview">{item.preview}...</div>
                </li>
            );
        })
        return (
            <div className="PostList">
                <div className="wrapper">
                    <div className="info">
                        <div className="photo" style={{backgroundImage: `url(${this.props.business.photo})`}}>
                            <div className="tags">{this.props.business.tag.map((item, i) => {
                                return <span className="tag" key={i}>{item.name}</span>;
                            })}</div>
                        </div>
                        <p className="name">{this.props.business.name} {this.props.business.name2 || ''}</p>
                        <p className="location"><i className="ion-android-pin"/> {this.props.business.street} {this.props.business.city}, {this.props.business.state} {this.props.business.postcode}</p>
                    </div>
                    <ul className="post-list">
                        {List}
                    </ul>
                </div>
                <span className="close" onClick={this.handleCloseClick}><i className="ion-android-close"></i></span>
            </div>
        );
    },

    handlePostClick(post) {
        this.props.onPostSelect(post);
    },

    handleCloseClick() {
        this.props.onCloseClick();
    }
})