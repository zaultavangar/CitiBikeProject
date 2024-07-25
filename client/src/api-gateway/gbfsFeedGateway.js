
const STATION_STATUS_URL = 'http://localhost:8000/gbfs_feed/station-status/'
const STATION_INFO_URL = 'http://localhost:8000/gbfs_feed/station-info/'

const CONCURRENCY_LIMIT = 5;

export async function getStationStatus(){
  const stationStatusResponse = await fetch(STATION_STATUS_URL);
  if (stationStatusResponse.ok){
    const json = await stationStatusResponse.json();
    return json.data;
  } else {
    console.log(stationStatusResponse.status)
    return [];
  }
}

export async function fetchStationInfo(station) {
  try {
    const response = await fetch(`${STATION_INFO_URL}?station_id=${station.id}`);
    if (response.ok) {
      const {station_id, ...stationInfo} = await response.json();
      return { ...station, ...stationInfo };
    } else {
      console.error(`Failed to fetch info for station ${station.id}: ${response.status}`);
      return null; 
    }
  } catch (error) {
    console.error(`Error fetching info for station ${station.id}:`, error);
    return null; 
  }
}

export async function getAllStationInfo(stationStatusArr, progressCallback){
  const filteredStations = stationStatusArr.filter(station => station.is_renting || station.is_returning);

  const results = [];

  const processBatch = async (batch) => {
    const promises = batch.map(station => fetchStationInfo(station));
    const batchResults = await Promise.all(promises)
    results.push(...batchResults.filter(result => result !== null));
  };

  for (let i = 0; i < filteredStations.length; i += CONCURRENCY_LIMIT) {
    const batch = filteredStations.slice(i, i + CONCURRENCY_LIMIT);
    await processBatch(batch);

    if (progressCallback) {
      progressCallback((i + CONCURRENCY_LIMIT)/ filteredStations.length);
    }
  }

  return results;

}




