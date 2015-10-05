let urlPrefix = XW_DEBUG ? 'http://localhost:8000' : 'http://xun-wei.com';

export default {
    businessList(start, hot_area, tag) {
        return `${urlPrefix}/api/business_list/?start=${start}&hot_area=${hot_area}&tag=${tag}`;
    },
    postList(start, business_id, hot_area, tag, q) {
        return `${urlPrefix}/api/post_list/?start=${start}&business_id=${business_id}&hot_area=${hot_area}&tag=${tag}&q=${q}`;
    },
    business(business_id) {
        return `${urlPrefix}/api/business/?business_id=${business_id}`;
    },
    post(post_id) {
        return `${urlPrefix}/api/post/?post_id=${post_id}`;
    },
    tagList() {
        return `${urlPrefix}/api/tag_list/`;  
    },

    checkUserExist() {
        return `${urlPrefix}/api/auth/check_user_exist/`;
    },
    login() {
        return `${urlPrefix}/api/auth/login/`;
    },
    signup() {
        return `${urlPrefix}/api/auth/signup/`;
    },
    checkStatus() {
        return `${urlPrefix}/api/auth/check_status/`;
    },
    getPostStarNum(post_id) {
        return `${urlPrefix}/api/post/star/?post_id=${post_id}`;
    },
    addPost() {
        return `${urlPrefix}/api/add_post/`;
    },
    starPost() {
        return `${urlPrefix}/api/star_post/`;
    },

    uploadImage() {
        return `${urlPrefix}/api/upload_image/`;
    }
};