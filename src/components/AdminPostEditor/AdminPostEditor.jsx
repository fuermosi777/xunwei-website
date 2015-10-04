import React from 'react';
import Styles from './AdminPostEditor.less';
import $ from 'jquery';

export default React.createClass({
    getInitialState() {
        return {
            loading: false,
            token: '',
            title: '',
            preview: '',
            source: '',
            business_id: null
        };
    },

    render() {
        return (
            <div className="AdminPostEditor">
                {this.state.loading ? <div className="loading">LOADING</div> : 
                <div>
                    <input placeholder="Publish Token" onChange={this.handleInputChange.bind(this, 'token')}/>
                    <input placeholder="Title" onChange={this.handleInputChange.bind(this, 'title')}/>
                    <input placeholder="Source" onChange={this.handleInputChange.bind(this, 'source')}/>
                    <textarea placeholder="Preview" onChange={this.handleInputChange.bind(this, 'preview')}/>
                    <input placeholder="Business ID" onChange={this.handleInputChange.bind(this, 'business_id')}/>
                    <div className="textarea" contentEditable="true" onPaste={this.handlePaste} ref="textarea"></div>
                    <p><button onClick={this.handleClick}>SUBMIT</button></p>
                </div>}
            </div>
        );
    },

    handleClick() {
        let data = {
            token: this.state.token,
            title: this.state.title,
            preview: this.state.preview,
            source: this.state.source,
            body: React.findDOMNode(this.refs.textarea).innerHTML,
            business_id: this.state.business_id
        };
        this.newPost(data).then((res) => {
            if (res.hasOwnProperty('msg') && res.msg === 'success') {
                alert('ssss');
                this.setState({
                    title: '',
                    preview: '',
                    source: '',
                    business_id: ''
                });
                React.findDOMNode(this.refs.textarea).innerHTML = '';
            }
        });
    },

    handleInputChange(thing, e) {
        let st = {};
        st[thing] = e.target.value;
        this.setState(st);
    },

    handlePaste(e) {
        e.preventDefault();
        var text = e.clipboardData.getData('text/html') || e.clipboardData.getData('text/plain');
        // rm meta tag
        text = text.replace(/<meta.*?>/gi, '');

        // rm style="xxx"
        text = text.replace(/[^>]style=".*?"/gi, '');
        text = text.replace(/[^>]class=".*?"/gi, '');
        text = text.replace(/[^>]id=".*?"/gi, '');
        text = text.replace(/[^>]width=".*?"/gi, '');
        text = text.replace(/[^>]height=".*?"/gi, '');

        var imgSrcRe = /<img.*?src=['|"](.*?)['|"]/g;
        var m;
        var urlsToReplace = [];
        var promises = [];
        do {
            m = imgSrcRe.exec(text);
            if (m) {
                let urlToReplace = m[1];
                let p = this.storeImage(urlToReplace);

                urlsToReplace.push(urlToReplace);
                promises.push(p);
            }
        } while (m);

        this.setState({loading: true});
        Promise.all(promises).then((res) => {
            this.setState({loading: false});
            for (let i = 0; i < res.length; i++) {
                text = text.replace(new RegExp(urlsToReplace[i], 'g'), res[i].link);
            }
            React.findDOMNode(this.refs.textarea).innerHTML = text;
        });
    },

    storeImage(url) {
        return new Promise((resolve, reject) => {
            $.ajax({
                method: 'POST',
                url: '/api/upload_image_url/',
                data: {
                    image_url: url,
                    source_domain: this.extractDomain(this.state.source)
                },
                success(res) {
                    resolve(res);
                },
                error(err) {
                    reject(err);
                }
            });
        });
    },

    newPost(data) {
        return new Promise((resolve, reject) => {
            $.ajax({
                method: 'POST',
                url: '/api/secret_add_post/',
                data: data,
                success(res) {
                    resolve(res);
                },
                error(err) {
                    reject(err);
                }
            });
        });
    },

    extractDomain(url) {
        var domain;
        var split = url.split('/');
        domain = split[0] + '//' + split[2];
        return domain;
    }
})