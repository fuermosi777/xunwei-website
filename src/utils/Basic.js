import $ from 'jquery';

export default {
    GET(url) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: url,
                dataType: 'json',
                success(res) {
                    resolve(res);
                },
                error(err) {
                    console.log(err);
                    reject(err);
                }
            });
        });
    },
    POST(url, data) {
        return new Promise((resolve, reject) => {
            let options = {
                url: url,
                type: 'POST',
                data: data,
                success(res) {
                    resolve(res);
                },
                error(err) {
                    console.log(err);
                    reject(err);
                }
            };
            $.ajax(options);
        });
    }
}