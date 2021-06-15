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
import { Podcasts, PodcastContainer } from './components/Podcasts';



export function App()
{
  return (
    <Router>
      <div>
        <p>
          <Link to="/podcasts">Podcasts</Link>
        </p>
        <hr />
        <Switch>
          <Route path="/podcasts">
            <Podcasts />
          </Route>
          <Route path="/podcast/:id">
            <PodcastContainer />
          </Route>
        </Switch>
      </div>
    </Router >
  );
}