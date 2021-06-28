import React from "react";
import
{
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";

import './App.css';
import { Podcasts, PodcastContainer } from './components/Podcasts';



export function App()
{
  return (
    <Router>
      <Switch>
        <Route path="/podcasts">
          <Podcasts />
        </Route>
        <Route path="/podcast/:id">
          <PodcastContainer />
        </Route>
      </Switch>
    </Router >
  );
}