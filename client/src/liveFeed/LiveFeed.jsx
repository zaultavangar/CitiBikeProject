import * as React from 'react';
import './LiveFeed.css'
import { Mapbox } from '../map/Mapbox';
import { useState } from 'react';
import { useEffect } from 'react';
import { getAllStationInfo, getStationStatus } from '../api-gateway/gbfsFeedGateway';

export const LiveFeed = () => {
  const [fetchStationInfoProgress, setFetchStationInfoProgress] = useState(0);
  const [lastUpdated, setLastUpdated] = useState(null)
  const [selectedStation, setSelectedStation] = useState(null);
  const [stations, setStations] = useState([]);
  const [colorCodeStrategy, setColorCodeStrategy] = useState('bikes_available');

  const load = async () => {
    const stationStatusArr = await getStationStatus();
    const allStationInfo = await getAllStationInfo(stationStatusArr, (progress) => {
      setFetchStationInfoProgress(progress);
    });

    setLastUpdated(new Date())
    setStations(allStationInfo)

    console.log('Expanded Station Info: ', allStationInfo)
  }

  const onRefresh = async () => {
    setFetchStationInfoProgress(0)
    setSelectedStation(null)
    await load()
  };

  useEffect(() => {
    console.log('useEffect running on mount');
    load()
  }, [])



  return (
    <div className='live-feed-container'>
      <h1>Live Feed</h1>
      <div className='live-feed-options-container'>
        {fetchStationInfoProgress < 1 && 
          <div>Loading Station Info: {Math.round(fetchStationInfoProgress * 100)}%</div>
        }
        {lastUpdated &&
          <div>
            Last Updated: {lastUpdated.toLocaleTimeString()}
          </div>
        }
        {fetchStationInfoProgress === 100 &&
          <button onClick={onRefresh}>Refresh</button>
        }
        <button 
          onClick={() => setColorCodeStrategy('bikes_available')}
          style={{ backgroundColor: colorCodeStrategy === 'bikes_available' ? '#9932CC' : '#696969' , padding: '10px 12px'}}
          >
          Color by Bikes Available
        </button>
        <button 
          onClick={() => setColorCodeStrategy('docks_available')}
          style={{ backgroundColor: colorCodeStrategy === 'docks_available' ? '#9932CC' : '#696969' , padding: '10px 12px'}}
          >
          Color by Docks Available
        </button>
      </div>
      <Mapbox
        selectedStation={selectedStation}
        setSelectedStation={setSelectedStation}
        stations={stations}
        colorCodeStrategy={colorCodeStrategy}
      />
    </div>
  )
}

/**
 * 
 *   const [fetchStationInfoProgress, setFetchStationInfoProgress] = useState(0);
  const [lastUpdated, setLastUpdated] = useState(null)
  const [selectedStation, setSelectedStation] = useState(null);
  const [stations, setStations] = useState([]);
  const [colorCodeStrategy, setColorCodeStrategy] = useState('bikes_available');



 */