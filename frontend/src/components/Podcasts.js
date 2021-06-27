import React from 'react';
import { useState, useEffect } from 'react';
import { Link, useParams } from "react-router-dom";
import { generatePath } from 'react-router';
import Card from 'react-bootstrap/Card'

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
        <div className="card shadow p-3" style={{ width: 10 + 'em' }} >
            <img src={props.podcast.img_url} alt={'Podcast cover art'} className="card-img-top" />
            <div className="card-body">
                <Link to={generatePath("/podcast/:id", { id: props.podcast.id })} className="stretched-link">{props.podcast.title}</Link>
            </div >
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
        <div className="container">
            <PodcastHeader podcast={podcast} />
            <SearchEpisodes query={query} setQuery={setQuery} />
            <EpisodeList episodes={episodes} query={query} />
        </div>
    );
}

function PodcastHeader(props)
{
    return (
        <div className="row">
            <h2>{props.podcast.title}</h2>
            <img src={props.podcast.img_url} alt={'Podcast cover art'} className="pod-art" />
        </div >
    )
}

function SearchEpisodes(props)
{
    function handleChange(e)
    {
        props.setQuery(e.target.value)
    }
    return (
        <div className="container">
            <label>
                Search episodes:
                <input type="text" value={props.query} onChange={handleChange} />
            </label>
        </div>
    );
}

function EpisodeList(props)
{
    return (
        <div className="row" key={props.query}>
            {props.episodes.map(
                ep => <EpisodeListItem key={ep.id} episode={ep} />
            )}
        </div >
    );
}

function EpisodeListItem(props)
{
    console.log(props.episode.published)
    return (
        <div>
            <h4>{props.episode.title}</h4>
            <p>{props.episode.published}</p>
            <p>{props.episode.description}</p>
        </div>
    );
}