import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import 'mapbox-gl/dist/mapbox-gl.css';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import PropTypes from 'prop-types';
import { Mapbox } from './map/Mapbox'
import { LiveFeed } from './liveFeed/LiveFeed';

function App() {

  const [count, setCount] = useState(0)

  function TabPanel(props) {
    const {children, value, index, ...other} = props;

    return (
      <div
        role="tabpanel"
        hidden={value != index}
        id={`tabpanel-${index}`}
        aria-labelledby={`tab-${index}`}
        {...other}
      >
        {value === index && (
          <div>{children}</div>
        )}
      </div>
    );
  }

  TabPanel.propTypes = {
    children: PropTypes.node,
    index: PropTypes.number.isRequired,
    value: PropTypes.number.isRequired,
  }

  const [tabValue, setTabValue] = useState(0)

  const handleChange = (event, newValue) => {
    setTabValue(newValue)
  }

  return (
    <>
      <div>
        <Tabs value={tabValue} onChange={handleChange} aria-label="App tabs">
          <Tab label="Live Feed"/>
          <Tab label="Historical Analysis"/>
          <Tab label="Forecasting"/>
        </Tabs>
        <TabPanel value={tabValue} index={0}>
          <LiveFeed/>
        </TabPanel>
        <TabPanel value={tabValue} index={1}>
          Historical Analysis
        </TabPanel>
        <TabPanel value={tabValue} index={2}>
          Forecasting
        </TabPanel>
      
      </div>
      
    </>
  )
}

export default App
