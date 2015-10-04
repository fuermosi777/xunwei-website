import Urls from '../utils/Urls.js';
import {POST} from '../utils/Basic.js';

export default {
    checkUserExists(email) {
        return POST(Urls.checkUserExist(), {email: email});
    },
    login(email, password) {
        return POST(Urls.login(), {email: email, password: password});
    },
    signup(email, password, username) {
        return POST(Urls.signup(), {email: email, password: password, username: username});
    },
    checkStatus(token) {
        return POST(Urls.checkStatus(), {token: token});
    }
}