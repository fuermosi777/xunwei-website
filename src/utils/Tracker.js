export default {
    
    // page view
    trackPageView() {
        if (typeof GA === 'undefined') return;
        GA('send', 'pageview');
    },
    trackPostPageView(title) {
        if (typeof GA === 'undefined') return;
        GA('send', 'pageview', '/post/' + title);
    },
    trackBusinessPageView(name) {
        if (typeof GA === 'undefined') return;
        GA('send', 'pageview', '/business/' + name);
    },
    trackTagPageView(tag) {
        if (typeof GA === 'undefined') return;
        GA('send', 'pageview', '/tag/' + tag);
    },
    trackSearchPageView(key) {
        if (typeof GA === 'undefined') return;
        GA('send', 'pageview', '/serach/?q=' + key);
    }
}