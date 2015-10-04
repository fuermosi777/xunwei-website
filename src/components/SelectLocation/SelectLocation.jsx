import React from 'react';
import Styles from './SelectLocation.less';

export default React.createClass({
    render() {
        let Locations = this.props.locations.map((item, i) => {
            return <li key={i} onClick={this.handleLocationClick.bind(this,item)}>{item.name}</li>;
        });
        return (
            <div className="SelectLocation">
                <div className="wrapper">
                    <p className="title">- 请选择您要寻味的地区 -</p>
                    <ul>
                        {Locations}
                    </ul>
                </div>
            </div> 
        );
    },

    handleLocationClick(l) {
        this.props.onLocationSelect(l);
    }
});