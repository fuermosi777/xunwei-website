import Basic from '../utils/Basic.js';
import Url from '../utils/Urls.js';

export default {
    getBusinessList(start=0, hot_area='', tag='') {
        return Basic.GET(Url.businessList(start, hot_area, tag));
    },
    getPostList(start=0, business_id='', hot_area='', tag='') {
        return Basic.GET(Url.postList(start, business_id, hot_area, tag));
    },
    getPost(post_id) {
        return Basic.GET(Url.post(post_id));
    },
    getBusiness(business_id) {
        return Basic.GET(Url.business(business_id)); 
    },
    getTagList() {
        return Basic.GET(Url.tagList());
    },
    getPostStarNum(post_id) {
        return Basic.GET(Url.getPostStarNum(post_id));
    },
    starPost(post_id, token) {
        return Basic.POST(Url.starPost(), {post_id: post_id, token: token});
    },
    uploadImage(image_b64) {
        return Basic.POST(Url.uploadImage(), {image: image_b64});
    },
    addPost(title, preview, token, body) {
        return Basic.POST(Url.addPost(), {title: title, preview: preview, token: token, body: body});
    }
}