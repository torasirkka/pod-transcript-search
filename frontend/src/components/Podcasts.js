import React from 'react';
import { useState, useEffect } from 'react';
import { Link, useParams } from "react-router-dom";
import { generatePath } from 'react-router';
import Image from 'react-bootstrap/Image';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup'

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
        <div className="row">
            {props.podcasts.map(podcast =>
                <PodcastListItem podcast={podcast} key={podcast.id} />
            )}
        </div>
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
            <PodcastHeader podcast={podcast} />
            <SearchEpisodes query={query} setQuery={setQuery} />
            <EpisodeList episodes={episodes} query={query} />
        </Container >
    );
}

function PodcastHeader(props)
{
    return (
        <Row >
            <div style={{ width: '700px' }}>
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
            <div className="mt-10 mb-10" >
                <InputGroup className="shadow">
                    <Form.Control type="search" placeholder="Search..." value={props.query} onChange={handleChange} />
                </InputGroup>
            </div>
        </Row>
    );
}

function EpisodeList(props)
{
    return (
        <div key={props.query}>
            {props.episodes.map(
                ep => <EpisodeListItem key={ep.id} episode={ep} />
            )}
        </div >
    );
}

function EpisodeListItem(props)
{
    return (
        <div>
            <h4>{props.episode.title}</h4>
            <p>{props.episode.published}</p>
            <p>{props.episode.description}</p>
        </div>
    );
}