import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';
import { Podcasts } from './components/Podcasts';
import ReactDOM from 'react-dom'
import
  {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
  } from "react-router-dom";


function App()
{
  const [podcasts, setPodcasts] = useState([]);

  useEffect(() =>
  {
    fetch('/api/podcasts').then(response =>
      response.json().then(data =>
      {
        setPodcasts(data);
      })
    );
  }, []);
  console.log(podcasts);
  return (
    <div className='App'>
      <Podcasts podcasts={podcasts} />
    </div>
  );
}

export default App;
