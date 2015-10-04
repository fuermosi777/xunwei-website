import React from 'react';
import Styles from './Map.less';
import L from 'leaflet';
import ContentService from '../../services/ContentService.js';

const marker = L.divIcon({
    className: 'marker',
    iconSize: [8, 8]
});

const markerActive = L.divIcon({
    className: 'marker active',
    iconSize: [22, 22]
});

export default React.createClass({
    map: null,

    markers: {},

	getInitialState() {
		return {
            height: window.innerHeight - 50
		};
	},

    componentWillMount() {
        
    },

    componentWillUnmount() {
        window.removeEventListener('resize', this.handleWindowResize);
    },

    componentDidMount() {
        this.createMap();
        window.addEventListener('resize', this.handleWindowResize);
    },

    render() {
        return (
            <div className="Map" style={{height: this.state.height}}>
            </div> 
        );
    },

    componentWillReceiveProps(nextProps) {
        if (nextProps.center !== 'undefined') {
            if (nextProps.center !== this.props.center) {
                this.centerMap([nextProps.center.lat, nextProps.center.lng], 12);
            }
        }

        if (nextProps.post !== 'undefined') {
            if (nextProps.post !== this.props.post) {
                this.removeMarkers();
                this.createMarkers(nextProps.post);
            }
        }

        if (nextProps.mouseOverBusiness !== 'undefined') {
            this.unhoverMarkers();
            if (nextProps.mouseOverBusiness) {
                this.hoverMarker(nextProps.mouseOverBusiness.id);
            }
        }
    },

    createMap() {
        let map = this.map = L.map(this.getDOMNode(), {
            zoomControl: false,
            layers: [
                L.tileLayer('http://api.tiles.mapbox.com/v4/fuermosi777.8a0ed89c/{z}/{x}/{y}@2x.png?access_token=pk.eyJ1IjoiZnVlcm1vc2k3NzciLCJhIjoidXRyY2VfUSJ9.eAxVQWWk97vLH4wa4aa1ig')
            ]
        });
    },

    createMarkers(post) {
        post.map((item) => {
            let m = L.marker([item.business.lat, item.business.lng], {icon: marker})
                .bindPopup(`<div class="popup"><p class="name">${item.business.name}</p></div>`)
                .on('click', this.handleMarkerClick.bind(this, item.business))
                .on('mouseover', this.handleMarkerMouseOver.bind(this, item))
                .on('mouseout', this.handleMarkerMouseOut.bind(this, item));
            if (!this.markers.hasOwnProperty(item.business.id)) { // add if there isn't
                m.addTo(this.map);
                this.markers[item.business.id] = m;
            }
        });
    },

    removeMarkers() {
        for (let key in this.markers) {
            if (this.markers.hasOwnProperty(key)) {
                this.map.removeLayer(this.markers[key]);
            }
        }
        this.markers = {};
    },

    hoverMarker(id) {
        if (this.markers.hasOwnProperty(id)) { // do this only if markers have 
            let bounds = this.map.getBounds();
            if (!bounds.contains(this.markers[id].getLatLng())) {
                this.map.fitBounds([this.markers[id].getLatLng(), this.map.getCenter()]);
            }
            this.markers[id].setIcon(markerActive);
        }
    },

    unhoverMarkers() {
        for (let key in this.markers) {
            if (this.markers.hasOwnProperty(key)) {
                this.markers[key].setIcon(marker);
            }
        }
    },

    centerMap(center, zoom) {
        this.map.setView(center, zoom);
    },

    handleWindowResize() {
        this.setState({height: window.innerHeight - 50});
    },

    handleMarkerClick(item) {
        this.props.onMarkerSelect(item);
    },

    handleMarkerMouseOver(item, e) {
        e.target.openPopup();
        e.target.setIcon(markerActive);
    },

    handleMarkerMouseOut(item, e) {
        e.target.closePopup();
        e.target.setIcon(marker);
    }
});