import React from "react";
import
{
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useParams
} from "react-router-dom";

import './App.css';
import { Podcasts, PodcastDetails } from './components/Podcasts';



export function App()
{
  return (
    <Router>
      <div>
        <ul>
          <li>
            <Link to="/podcasts">Podcasts</Link>
          </li>
          <li>
            <Link to="/podcast-details">Dashboard</Link>
          </li>
        </ul>

        <hr />

        {/*
          A <Switch> looks through all its children <Route>
          elements and renders the first one whose path
          matches the current URL. Use a <Switch> any time
          you have multiple routes, but you want only one
          of them to render at a time
        */}
        <Switch>
          <Route path="/podcasts">
            <Podcasts />
          </Route>
          <Route path="/podcast/:id">
            <PodcastDetails />
          </Route>
        </Switch>
      </div>
    </Router >
  );
}

// You can think of these components as "pages"
// in your app.


