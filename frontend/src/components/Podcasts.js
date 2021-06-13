import React from 'react';
import { useState, useEffect } from 'react';
import { useParams } from "react-router-dom";

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
    console.log(podcasts);
    return (
        <div className='podcast'>
            <PodcastList podcasts={podcasts} />
        </div>
    );
}

export function PodcastList(props)
{
    return (
        <ul>
            {props.podcasts.map(podcast => <li key={podcast.title}>{podcast.title}</li>)}
        </ul >
    )
};


export function PodcastDetails()
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
    console.log(podcast);
    if (podcast === null)
    {
        return 'loading...'
    }

    return (
        <div>
            <h2>{podcast.title}</h2>
        </div>
    );
}
