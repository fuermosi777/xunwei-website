import React from 'react';
import Styles from './HomePage.less';
import Map from '../components/Map/Map.jsx';
import MainPostList from '../components/MainPostList/MainPostList.jsx';
import PostList from '../components/PostList/PostList.jsx';
import SelectLocation from '../components/SelectLocation/SelectLocation.jsx';
import Auth from '../components/Auth/Auth.jsx';
import Nav from '../components/Nav/Nav.jsx';
import Loading from '../components/Loading/Loading.jsx';
import PostEditor from '../components/PostEditor/PostEditor.jsx';
import Post from '../components/Post/Post.jsx';
import WechatIcon from '../components/WechatIcon/WechatIcon.jsx';
import Constant from '../utils/Constant.js';
import Tracker from '../utils/Tracker.js';

import {History, State} from 'react-router';

import ContentService from '../services/ContentService.js';

import LocationStore from '../stores/LocationStore.js';
import AuthStore from '../stores/AuthStore.js';

export default React.createClass({
    mixins: [History, State],

    getInitialState() {
        return {
            // if the user has logged in
            username: '',

            showAuth: false,
            showPostEditor: false,

            loading: false,
            location: null,
            center: null,
            mainPost: [],
            mainPostStart: 0,
            selectedBusiness: null,
            mouseOverBusiness: null,
            post: [],
            tag: [],
            selectedTag: null,
            selectedPost: null
        };
    },

    componentDidMount() {
        // get category from URL
        // and set to state
        Tracker.trackPageView();
        if (this.props.history.isActive('/post')) {
            let pid = this.props.params.pid || '';
            if (pid) {
                this.setState({loading: true});
                let post;
                ContentService.getPost(pid).then((res) => {
                    post = res;
                    let locationName = res.business.hot_area;
                    let location = Constant.LOCATIONS.filter((item) => {
                        return item.name === locationName;
                    })[0];
                    return this.handleLocationSelect(location);
                }).then(() => {
                    this.setState({loading: false});
                    this.handlePostSelect(post);
                });
            }
        } else if (this.props.history.isActive('/business')) {
            let bid = this.props.params.bid || '';
            if (bid) {
                this.setState({loading: true});
                let business;
                ContentService.getBusiness(bid).then((res) => {
                    business = res;
                    let locationName = res.hot_area;
                    let location = Constant.LOCATIONS.filter((item) => {
                        return item.name === locationName;
                    })[0];
                    return this.handleLocationSelect(location);
                }).then(() => {
                    this.setState({
                        loading: false
                    });
                    this.handleBusinessSelect(business);
                });
            }
        } else if (this.props.history.isActive('/tag')) {
            let tag = this.props.params.tag || '';
            let location = LocationStore.getLocation() || Constant.LOCATIONS[0];
            if (tag) {
                this.handleLocationSelect(location).then(() => {
                    this.handleTagSelect({name: tag});
                });
            }
        } else if (this.props.history.isActive('/search')) {
            let q = this.props.location.query.q || '';
            let location = LocationStore.getLocation() || Constant.LOCATIONS[0];
            if (q) {
                this.handleLocationSelect(location).then(() => {
                    this.handleSearch(q);
                });
            }
        } else {
            let location = LocationStore.getLocation();
            if (location) {
                this.handleLocationSelect(location);
            }
        }
        AuthStore.isLogin().then((username) => {
            this.setState({username: username});
        }).catch(() => {});
    },

    render() {
        return (
            <div className="HomePage">
                <Nav
                    location={this.state.location}
                    username={this.state.username}
                    onLocationSelect={this.handleLocationChange}
                    onLogout={this.handleLogout}
                    onAuthSelect={this.handleAuthStart}
                    onPublishSelect={this.handlePublishSelect} />
                {this.state.location ? '' :
                <SelectLocation
                    locations={Constant.LOCATIONS}
                    onLocationSelect={this.handleLocationSelect}/>}
                {!this.state.showAuth ? '' :
                <Auth 
                    onClose={this.handleAuthClose}
                    onSuccess={this.handleAuthSuccess}/>
                }
                <Map
                    center={this.state.center}
                    post={this.state.mainPost}
                    onMarkerSelect={this.handleMarkerSelect}
                    mouseOverBusiness={this.state.mouseOverBusiness}/>
                <MainPostList
                    post={this.state.mainPost}
                    tag={this.state.tag}
                    onBusinessSelect={this.handleBusinessSelect}
                    onPostSelect={this.handlePostSelect}
                    onTagSelect={this.handleTagSelect}
                    onPostMouseOver={this.handlePostMouseOver}
                    onPostMouseLeave={this.handlePostMouseLeave}
                    onLoadMoreClick={this.handleMoreMainPost}
                    onSearch={this.handleSearch} />
                {this.state.post && this.state.selectedBusiness ? 
                    <PostList 
                        post={this.state.post} 
                        business={this.state.selectedBusiness}
                        onPostSelect={this.handlePostSelect}
                        onCloseClick={this.handlePostListClose}/> : ''}
                {this.state.selectedPost ? 
                    <Post 
                        data={this.state.selectedPost} 
                        onCloseClick={this.handlePostClose} 
                        onStarFail={this.handleAuthStart}
                        onBusinessSelect={this.handleBusinessSelect}/> : ''}
                {this.state.loading ? 
                    <Loading/> : ''}
                {this.state.showPostEditor ? 
                    <PostEditor
                        onPublishSuccess={this.handlePublishSuccess}/> : ''}
                <WechatIcon/>
            </div>
        );
    },

    handleLocationSelect(l) {
        return new Promise((resolve, reject) => {
            LocationStore.setLocation(l);
            this.setState({
                location: l,
                center: l.center,
                loading: true,
                mouseOverBusiness: null,
                selectedPost: null,
                selectedBusiness: null
            });
            let getPostList = ContentService.getPostList(0, '', l.name, '').then((res) => {
                this.setState({
                    mainPost: res
                });
            });
            let getTagList = ContentService.getTagList().then((res) => {
                this.setState({tag: res});
            });
            Promise.all([getPostList, getTagList]).then((res) => {
                this.history.pushState(null, `/`);
                Tracker.trackPageView();
                document.title = `寻味`;
                this.setState({
                    loading: false
                });
                resolve();
            });
        });
        
    },

    handleMoreMainPost() {
        this.setState({
            loading: true
        });
        ContentService.getPostList(this.state.mainPostStart + 25, '', this.state.location.name, this.state.tag.name).then((res) => {
            this.setState({
                mainPost: this.state.mainPost.concat(res),
                loading: false,
                mainPostStart: this.state.mainPostStart + 25
            });
        });
    },

    handleTagSelect(tag) {
        this.setState({
            loading: true,
            selectedTag: tag
        });
        ContentService.getPostList(0, '', this.state.location.name, tag.name).then((res) => {
            this.history.pushState(null, `/tag/${tag.name}/`);
            Tracker.trackTagPageView(tag.name);
            document.title = `寻味 | ${tag.name}`;
            this.setState({
                mainPost: res,
                loading: false
            });
        });
    },

    handleSearch(key) {
        this.setState({loading: true});
        ContentService.getPostList(0, '', this.state.location.name, '', key).then((res) => {
            this.history.pushState(null, `/search/`, {q: key})
            document.title = `寻味 | 搜索结果: ${key}`;
            Tracker.trackSearchPageView(key);
            this.setState({
                mainPost: res,
                loading: false
            })
        });
    },

    handleLocationChange() {
        this.setState({location: null});
        LocationStore.removeLocation();
    },

    handleAuthStart() {
        this.setState({showAuth: true});
    },

    handleMarkerSelect(business) {
        this.setState({
            center: {
                lat: business.lat,
                lng: business.lng
            },
            selectedPost: null,
            mouseOverBusiness: business,
            loading: true
        });
        ContentService.getPostList(0, business.id).then((res) => {
            this.history.pushState(null, `/business/${business.id}/`);
            Tracker.trackBusinessPageView(business.name);
            document.title = `寻味 | ${business.name}`;
            this.setState({
                loading: false,
                post: res,
                selectedBusiness: business
            });
        });
    },

    handleBusinessSelect(business) {
        this.handleMarkerSelect(business);
    },

    handlePublishSelect() {
        this.setState({showPostEditor: !this.state.showPostEditor});
    },

    handlePublishSuccess() {
        this.setState({showPostEditor: false});
    },

    handleLogout() {
        AuthStore.logout();
        this.setState({
            username: null,
            showPostEditor: null
        });
    },

    handlePostSelect(post) {
        this.history.pushState(null, `/post/${post.id}/`);
        Tracker.trackPostPageView(post.title);
        document.title = `寻味 | ${post.title}`;
        this.setState({
            selectedPost: post,
            mouseOverBusiness: post.business
        });
    },

    handlePostMouseOver(post) {
        this.setState({mouseOverBusiness: post.business});
    },

    handlePostMouseLeave(post) {
        if (!this.props.history.isActive('/post') && !this.props.history.isActive('/business')) {
            this.setState({mouseOverBusiness: null});
        }
    },

    handlePostListClose() {
        this.goBackOrGoHome();
        this.setState({
            post: [],
            selectedBusiness: null,
            mouseOverBusiness: null
        });
    },

    handlePostClose() {
        this.goBackOrGoHome();
        this.setState({
            selectedPost: null,
            mouseOverBusiness: null
        });
    },

    handleAuthClose() {
        this.setState({showAuth: false});
    },

    handleAuthSuccess(username, token) {
        this.setState({
            showAuth: false,
            username: username
        });
        AuthStore.login(token);
    },

    goBackOrGoHome() {
        Tracker.trackPageView();
        document.title = `寻味`;
        if (this.history.length > 1) {
            this.history.goBack();
        } else {
            this.history.pushState(null, `/`);
        }
    }
 });