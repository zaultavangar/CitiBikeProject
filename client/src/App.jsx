import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import 'mapbox-gl/dist/mapbox-gl.css';
import { Mapbox } from './map/Mapbox'

function App() {

  const [count, setCount] = useState(0)

  return (
    <>
      <div>
       <Mapbox/>
      </div>
      
    </>
  )
}

export default App
