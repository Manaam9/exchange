import React from 'react';
import "../styles/AssetItem.css"
import {Link} from "react-router-dom";


const AssetPairItem = (props) => {
    const assetPairId = props.asset_pair.id + '/ '

    return (
        <Link to={assetPairId} className="cards">
            <div className="card card-1">
                <p className="card__apply">
                    <span className="card__link">
                        {props.asset_pair.base_asset.name}/{props.asset_pair.quote_asset.name}
                    </span>
                </p>
                <h2 className="card__title">
                    {props.asset_pair.base_asset.symbol}/{props.asset_pair.quote_asset.symbol}
                </h2>
            </div>
        </Link>
    );
};

export default AssetPairItem;