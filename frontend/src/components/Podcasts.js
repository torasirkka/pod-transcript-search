import React from 'react';
import { useState, useEffect } from 'react';
import { Link, useParams } from "react-router-dom";
import { generatePath } from 'react-router';
import Image from 'react-bootstrap/Image';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import ListGroup from 'react-bootstrap/ListGroup';
import Navbar from 'react-bootstrap/Navbar'

export function Podcasts()
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
    return (
        <div className="container">
            <PodcastList podcasts={podcasts} />
        </div>
    );
}

function PodcastList(props)
{
    return (
        <Row>
            <Col>
                {props.podcasts.map(podcast =>
                    <PodcastListItem podcast={podcast} key={podcast.id} />
                )}
            </Col>
        </Row>
    )
};

function PodcastListItem(props)
{
    return (
        <div className="card shadow" style={{ width: 10 + 'em' }} >
            <img src={props.podcast.img_url} alt={props.podcast.title} className="card-img-top rounded" />
            <Link to={generatePath("/podcast/:id", { id: props.podcast.id })} className="stretched-link"></Link>
        </div>
    )
}

export function PodcastContainer()
{
    const [podcast, setPodcast] = useState(null);
    const [query, setQuery] = useState('')
    const [episodes, setEpisodes] = useState([]);

    const params = useParams();
    useEffect(() =>
    {
        fetch('/api/podcasts/' + params.id).then(response =>
            response.json().then(data =>
            {
                setPodcast(data);
            })
        );
    }, [params.id]);

    useEffect(() =>
    {
        fetch('/api/podcasts/' + params.id + '/search?q=' + query).then(response =>
            response.json().then(data =>
            {
                setEpisodes(data);
            })
        );
    }, [query, params.id]);

    if (podcast === null)
    {
        return <p>'loading...'</p>
    }

    return (
        <Container className="pod-container">
            <NavbarHeader />
            <PodcastHeader podcast={podcast} />
            <SearchEpisodes query={query} setQuery={setQuery} />
            <EpisodeList episodes={episodes} query={query} />
        </Container >
    );
}

function NavbarHeader()
{
    return (
        <Row>
            <Col>
                <Navbar >
                    <Navbar.Brand href="/podcasts" className="text-muted fw-light lh-1">All podcasts</Navbar.Brand>
                </Navbar>
            </Col>
        </Row>
    );
}

function PodcastHeader(props)
{
    return (
        <Row >
            <Col>
                <div className="pod-header-width">
                    <div className="row no-gutters">
                        <div className="col xs:{5}">
                            <Image
                                src={props.podcast.img_url}
                                alt={'Podcast cover art'}
                                className="rounded pod-header" />
                        </div>
                        <div className="col-md-9">
                            <div className="card-body pad-0 mt-10">
                                <h2>{props.podcast.title}</h2>
                                <p>{props.podcast.description}</p>

                            </div>
                        </div>
                    </div>
                </div>
            </Col>
        </Row >
    )
}


function SearchEpisodes(props)
{
    function handleChange(e)
    {
        props.setQuery(e.target.value)
    }
    return (
        <Row >
            <Col>
                <div className="mt-10 mb-10" >
                    <InputGroup className="shadow">
                        <Form.Control type="search" placeholder="Search..." value={props.query} onChange={handleChange} />
                    </InputGroup>
                </div>
            </Col>
        </Row>
    );
}

function EpisodeList(props)
{
    return (
        <Row>
            <Col>
                <ListGroup className="bg-gradient-dark" variant="flush" key={props.query}>
                    {props.episodes.map(
                        ep => <EpisodeListItem key={ep.id} episode={ep} />
                    )}
                </ListGroup>
            </Col>
        </Row>
    );
}

function EpisodeListItem(props)
{
    return (
        <ListGroup.Item className="bg-transparent pl-0">
            <h5 className="">{props.episode.title}</h5>
            <p className="text-muted fw-light lh-1">{props.episode.published}</p>
            <p className="">{props.episode.description}</p>
        </ListGroup.Item>
    );
}