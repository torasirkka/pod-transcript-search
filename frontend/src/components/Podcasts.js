import React from 'react';

export const Podcasts = ({ podcasts }) =>
{
    return (
        <ul>
            {podcasts.map(podcast => <li key={podcast.title}>{podcast.title}</li>)}
        </ul >
    )
};