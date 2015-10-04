export default {
    
    // page view
    trackPageView() {
        if (typeof GA === 'undefined') return;
        GA('send', 'pageview');
    },
    trackAreaPageView(area) {
        if (typeof GA === 'undefined') return;
        GA('send', 'pageview', '/area/' + area);
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
}