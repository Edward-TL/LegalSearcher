import plotly.graph_objects as go

def score_heatmap(test_names, user_queries, Scores_data, ArtCont_data, return_fig=False, show_fig=True):
    fig = go.Figure(
        data = 
        go.Heatmap(
            x = test_names,
            y = user_queries,
            z = Scores_data,
            text = ArtCont_data,
            colorscale = 'Inferno',
            hovertemplate =
            '<b>Word/Phrase Searched</b>: %{y}<b>'+
            '<br><b>Query Type</b>: %{x}</br>'+
            '<b>Score</b>: %{z}'+
            '<br>%{text}</br>'
        )
    )
    fig.update_layout(
        title = "Max Score",
        xaxis_title = "Tests",
        yaxis_title = "Word searched"
        )

    if show_fig: fig.show()
    if return_fig: return fig

def serie_boxplot(serie_list, serie_title, plot_title, return_fig=False, show_fig=True):
    simple_t = [array[0] for array in serie_list]
    fuzzy_t = [array[1] for array in serie_list]
    match_t = [array[2] for array in serie_list]
    embedds_t = [array[3] for array in serie_list]
    

    fig = go.Figure()
    fig.add_trace(go.Box(y=simple_t, name="Simple"))
    fig.add_trace(go.Box(y=fuzzy_t, name="Fuzzy"))
    fig.add_trace(go.Box(y=match_t, name="Math Phrase"))
    fig.add_trace(go.Box(y=embedds_t, name="Embedds"))
    fig.update_traces(boxpoints='all', jitter=0.25)

    fig.update_layout(
        title = plot_title,
        xaxis_title = "Tests",
        yaxis_title = serie_title
        )

    if show_fig: fig.show()
    if return_fig: return fig