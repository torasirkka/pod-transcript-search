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
        fetch('/api/podcasts/' + params.id + '/search').then(response =>
            response.json().then(data =>
            {
                setEpisodes(data);
            })
        );
    }, []);
    //console.log(episodes);

    if (podcast === null)
    {
        return <p>'loading...'</p>
    }

    return (
        <div>
            <PodcastHeader podcast={podcast} />
            <SearchEpisodes query={setQuery} />
            <EpisodeList episodes={episodes} />
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

function SearchEpisodes()
{
    function handleSubmit(e)
    {
        e.preventDefault();
        console.log(e);
    }
    return (
        <form onSubmit={handleSubmit} >
            <label>
                Search episodes:
                <input type="text" />
            </label>
            <input type="submit" value="Submit" />
        </form >
    );
}

function EpisodeList(props)
{
    console.log(props.episodes[0])
    return (
        <div key={props.episodes} className='episodes-list'>
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