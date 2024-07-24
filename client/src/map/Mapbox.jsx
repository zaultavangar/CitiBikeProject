import mapboxgl from 'mapbox-gl';
import * as React from 'react';
import Map, {FullscreenControl,  MapProvider,  NavigationControl, ScaleControl, useMap} from 'react-map-gl';


export const Mapbox = () => {

  let accessToken = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN;

  const mapRef = React.useRef(null);

  const {current: map} = useMap();

  const [viewState, setViewState] = React.useState({
    longitude: -74.0060,
    latitude: 40.7128,
    zoom: 11
  });

  const onClick = () => {
    const map = mapRef.current.getMap();
    // map.flyTo({center: [-122.4, 37.8]});
  };

  return (
    <div id='map' style={{width: '400px', height: '300px'}}>
      <MapProvider>
        <Map
        ref={mapRef}
        mapboxAccessToken={accessToken}
        {...viewState}
        onMove={evt => setViewState(evt.viewState)}
        style={{width: 800, height: 500}}
        mapStyle="mapbox://styles/mapbox/streets-v9"
      >
        <FullscreenControl/>
        <NavigationControl/>
        <ScaleControl/>
      </Map>
      </MapProvider>
      
    <button onClick={onClick}></button>


    </div>
  )

}