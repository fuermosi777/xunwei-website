import AuthService from '../services/AuthService.js';

export default {
    login(token) {
        localStorage.setItem('token', token);
    },
    logout() {
        localStorage.removeItem('token');
    },
    isLogin() {
        return new Promise((resolve, reject) => {
            let token = localStorage.getItem('token');
            if (!token) {
                reject();
                return;
            }
            AuthService.checkStatus(token).then((res) => {
                if (res.status) {
                    resolve(res.username);
                }
            }).catch(() => {
                reject();
            });
        });
    },
    getToken() {
        return localStorage.getItem('token');
    }
}