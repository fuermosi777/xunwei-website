export default {
    getLocation() {
        let location = localStorage.getItem('location');
        if (location) {
            return JSON.parse(location);
        } else {
            return null;
        }
    },
    setLocation(location) {
        localStorage.setItem('location', JSON.stringify(location));
    },
    removeLocation() {
        localStorage.removeItem('location');
    }
};