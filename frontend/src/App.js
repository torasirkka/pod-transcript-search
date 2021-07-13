import React from "react";
import
{
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import Navbar from "react-bootstrap/esm/Navbar";
import Container from "react-bootstrap/esm/Container";

import './App.css';
import { Podcasts, PodcastContainer } from './components/Podcasts';



export function App()
{
  return (
    <Router>
      <Navbar>
        <Navbar.Brand id="navbar-text" href="/podcasts">Podsearch.</Navbar.Brand>
      </Navbar>
      <Container className="pod-container">
        <Switch>
          <Route path="/podcasts">
            <Podcasts />
          </Route>
          <Route path="/podcast/:id">
            <PodcastContainer />
          </Route>
        </Switch>
      </Container>
    </Router >
  );
}