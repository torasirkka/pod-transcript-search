import React from 'react';
import { useState, useEffect } from 'react';
import { Link, useParams } from "react-router-dom";
import { generatePath } from 'react-router';

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
        <div className='podcasts'>
            <PodcastList podcasts={podcasts} />
        </div>
    );
}

function PodcastList(props)
{
    return (
        <ul>
            {props.podcasts.map(podcast =>
                <li key={podcast.title}>
                    <Link to={generatePath("/podcast/:id", { id: podcast.id })}>{podcast.title}</Link>
                </li>
            )}
        </ul>
    )
};

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
        <div>
            <PodcastHeader podcast={podcast} />
            <SearchEpisodes query={query} setQuery={setQuery} />
            <EpisodeList episodes={episodes} query={query} />
        </div>
    );
}

function PodcastHeader(props)
{
    return (
        <div className='podcast-details'>
            <h2>{props.podcast.title}</h2>
            <p>{props.podcast.description}</p>
            <img src={props.podcast.img_url} alt={'Podcast cover art'} width={100} />
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
        <label>
            Search episodes:
            <input type="text" value={props.query} onChange={handleChange} />
        </label>
    );
}

function EpisodeList(props)
{
    return (
        <div key={props.query} className='episodes-list'>
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
            <h3>{props.episode.title}</h3>
            <p>{props.episode.description}</p>
            <p>{props.episode.transcript}</p>
        </div>
    );
}