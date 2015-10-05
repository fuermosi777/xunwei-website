import React from 'react';
import Styles from './PostEditor.less';
import $ from 'jquery';
import ContentService from '../../services/ContentService.js';
import AuthStore from '../../stores/AuthStore.js';

export default React.createClass({
    getInitialState() {
        return {
            loading: false,
            body: '',
            title: '',
            error: ''
        };
    },

    render() {
        return (
            <div className="PostEditor">
                {this.state.loading ? <div className="loading">LOADING</div> : 
                <div>
                    {this.state.error ? <p>{this.state.error}</p> : ''}
                    <input placeholder="输入文章标题" onChange={this.handleInputChange.bind(this, 'title')} className="title-input"/>
                    <input type="file" className="image-upload-input" ref="imageUploadInput" onChange={this.handleImageInputChange}/> 
                    <button onClick={this.handleAddImageClick}><i className="ion-android-image"/> 添加图片</button>
                    <div className="textarea" contentEditable="true" onPaste={this.handlePaste} onChanage={this.handleTextareaChange} ref="textarea"></div>
                    <button onClick={this.handleSubmitClick}>提交审核</button>
                </div>}
            </div>
        );
    },

    handleAddImageClick() {
        React.findDOMNode(this.refs.imageUploadInput).click();
    },

    handleTextareaChange() {
        
    },

    handleImageInputChange(e) {
        let exsitingHTML = React.findDOMNode(this.refs.textarea).innerHTML;
        if (!e.target.files[0]) return;
        var formData = new FormData();
        var file = e.target.files[0];
        var reader = new FileReader(); 

        reader.onload = (readerEvt) => {
            var binaryString = readerEvt.target.result;
            this.setState({loading: true});
            ContentService.uploadImage(btoa(binaryString)).then((res) => {
                this.setState({loading: false});
                
                React.findDOMNode(this.refs.textarea).innerHTML = exsitingHTML + `<img src="${res.link}"/>`;
            }).catch((err) => {
                this.setState({loading: false});
                console.log(err);
            });
        };

        reader.readAsBinaryString(file);
    },

    handleSubmitClick() {
        let token = AuthStore.getToken();
        let preview = React.findDOMNode(this.refs.textarea).textContent.substring(0, 80);
        this.setState({error: '', body: React.findDOMNode(this.refs.textarea).innerHTML}, () => {
            if (!this.state.title) {
                this.setState({error: '标题不能为空'});
                return;
            }
            if (!this.state.body) {
                this.setState({error: '内容不能为空'});
                return;
            }
            this.setState({loading: true});
            ContentService.addPost(this.state.title, preview, token, this.state.body).then((res) => {
                this.setState({loading: false});
                if (res.hasOwnProperty('msg') && res.msg === 'success') {
                    this.handlePublishSuccess();
                }
            }).catch((err) => {
                this.setState({loading: false, error: '发生未知错误，请稍后重试'})
            });
        });
    },

    handleInputChange(thing, e) {
        let st = {};
        st[thing] = e.target.value;
        this.setState(st);
    },

    handlePublishSuccess() {
        this.props.onPublishSuccess();
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
        document.execCommand('insertHTML', false, text);
    },

    storeImage(url) {
        return new Promise((resolve, reject) => {
            $.ajax({
                method: 'POST',
                url: 'http://localhost:8000/api/upload_image_url/',
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

    extractDomain(url) {
        var domain;
        var split = url.split('/');
        domain = split[0] + '//' + split[2];
        return domain;
    }
})