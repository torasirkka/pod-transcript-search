function Podcast(props)
{
    return (
        <div className="podcast">
            <p>{props.title}</p>
        </div>
    );
}

function PodcastContainer()
{
    const [podcasts, updatePodcasts] = React.useState([]);

    React.useEffect(() =>
    {
        fetch('/api/all-podcasts.json')
            .then((response) => response.json())
            .then((data) => updatePodcasts(data))
    }, [])

    const podcasts_list = [];
    console.log({ podcasts })
    for (const currentPodcast of podcasts_list)
    {
        podcasts_list.push(
            <TradingCard
                key={currentPodcast.title}
                name={currentPodcast.title}
            />
        );
    }

    return (
        <div>{podcasts_list}</div>
    );

}

ReactDOM.render(
    <PodcastContainer />,
    document.getElementById('container')
);
