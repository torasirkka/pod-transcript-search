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
    //console.log(podcasts);
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
    const params = useParams();
    const [podcast, setPodcast] = useState(null);

    useEffect(() =>
    {
        fetch('/api/podcasts/' + params.id).then(response =>
            response.json().then(data =>
            {
                setPodcast(data);
            })
        );
    }, [params.id]);

    const [episodes, setEpisodes] = useState([]);

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
            <img src={props.podcast.img_url} width={100}></img>
        </div>
    )
}

function EpisodeList(props)
{
    console.log(props.episodes)
    return (
        <div className='episodes-list'>
            {props.episodes.map(episode =>
                <div key={episode.id}>
                    <h2>{episode.title}</h2>
                    <p>{episode.description}</p>
                    <p>{episode.transcript}</p>
                </div>
            )}
        </div >
    );
}
