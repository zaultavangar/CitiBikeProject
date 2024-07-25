import mapboxgl from 'mapbox-gl';
import * as React from 'react';
import Map, {FullscreenControl,  Layer,  MapProvider,  NavigationControl, Popup, ScaleControl, Source, useMap} from 'react-map-gl';
import { getAllStationInfo, getStationStatus } from '../api-gateway/gbfsFeedGateway';
import { useState } from 'react';
import { useEffect } from 'react';
import { useCallback } from 'react';


export const Mapbox = ({
  selectedStation,
  setSelectedStation,
  stations,
  colorCodeStrategy
}) => {

  let accessToken = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN;
  const mapRef = React.useRef(null);

  const [viewState, setViewState] = useState({
    longitude: -73.98131319608744,
    latitude: 40.754761812487516,
    zoom: 9.9
  });

  const handleStationClick = useCallback((event) => {
    if (event.features) {
      const feature = event.features[0];
      setSelectedStation({
        ...feature.properties,
        longitude: parseFloat(feature.geometry.coordinates[0]),
        latitude: parseFloat(feature.geometry.coordinates[1])
      });
    }
  }, []);

  useEffect(() => {
    if (!mapRef.current) {
      console.log('no map ref')
      return;
    }

    const map = mapRef.current.getMap();

    if (map) {
      console.log('hello')
      map.on('click', 'stations-layer', handleStationClick);

      return () => {
        map.off('click', 'stations-layer', handleStationClick);
      };
    }
  }, [handleStationClick]);


  const [stationDataGeojson, setStationDataGeojson] = useState({
    type: 'FeatureCollection',
    features: []
  })

  useEffect(() => {
    if (stations){
      const tmpData = {
        type: 'FeatureCollection',
        features: stations
          .filter(station => station.longitude !== null && station.latitude !== null)
          .map(station => ({
          type: 'Feature',
          properties: {
            id: station.id,
            name: station.name,
            num_bikes_available: station.num_bikes_available,
            num_ebikes_available: station.num_ebikes_available,
            num_docks_available: station.num_docks_available,
            capacity: station.capacity,
          },
          geometry: {
            type: 'Point',
            coordinates: [parseFloat(station.longitude), parseFloat(station.latitude)],
          },
        })),
      };
      setStationDataGeojson(tmpData);
    }


  }, [stations])

  const getCircleColorExpression = () => {
    if (colorCodeStrategy === 'bikes_available') {
      return [
        'interpolate',
        ['linear'],
        ['/', ['get', 'num_bikes_available'], ['get', 'capacity']],
        0, 'yellow',
        1, 'green',
      ];
    } else if (colorCodeStrategy === 'docks_available') {
      return [
        'interpolate',
        ['linear'],
        ['/', ['get', 'num_docks_available'], ['get', 'capacity']],
        0, 'yellow',
        1, 'green',
      ];
    }
    return ['match', ['get', 'id'], 'default', 'gray']; // Default color if strategy is not matched
  };

  return (
      <div id='map' style={{width: '400px', height: '300px'}}>
        <MapProvider>
          <Map
          ref={mapRef}
          mapboxAccessToken={accessToken}
          {...viewState}
          onMove={evt => {setViewState(evt.viewState)}}
          style={{width: 800, height: 500}}
          mapStyle="mapbox://styles/mapbox/streets-v9"
        >
          <FullscreenControl/>
          <NavigationControl/>
          <ScaleControl/>
          <Source id="stations" type="geojson" data={stationDataGeojson}>
          <Layer
              id="stations-layer"
              type="circle"
              // onClick={handleStationClick}
              paint={{
                'circle-color': getCircleColorExpression(),
                'circle-radius': [
                  'interpolate',
                  ['linear'],
                  ['get', 'capacity'],
                  1, 5,
                  50, 10,
                ],
                'circle-stroke-width': 2,
                'circle-stroke-color': '#ffffff',
              }}
            />
          </Source>

          {selectedStation && (
            <Popup
              longitude={selectedStation.longitude}
              latitude={selectedStation.latitude}
              onClose={() => setSelectedStation(null)}
              closeOnClick={false}
            >
              <div style={{color: 'black'}}>
                <h3>{selectedStation.name}</h3>
                <p>Bikes Available: {selectedStation.num_bikes_available}</p>
                <p>EBikes Available: {selectedStation.num_ebikes_available}</p>
                <p>Docks Available: {selectedStation.num_docks_available}</p>
                <p>Capacity: {selectedStation.capacity}</p>
              </div>
            </Popup>
          )}
        </Map>
        </MapProvider>
      </div>    
  )

}