import React, { Component } from 'react';
import './stream-log.css';

function ListItem(props) {
  return <li className="ellipsis">{props.tweet}</li>
}

function ListItems(props) {
  return (
      <ul className="list-reset">
        {props.tweets.map((tweet) => <ListItem key={tweet.id} tweet={tweet.text} />)}
      </ul>
  )
}

class Stream extends Component {
  render() {
    let tweets = this.props.tweetList || [];

    if (this.props.keyword === '') {
      return null;
    }

    return (
      <section className="mt3 border-top">
        <h4 className="mt3">Watching "{this.props.keyword}"</h4>
        <ListItems tweets={tweets} />
      </section>
    );
  }
}

export default Stream;
