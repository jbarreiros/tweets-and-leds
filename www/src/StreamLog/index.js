import React, { Component } from 'react';
import './stream-log.css';

function ListItem(props) {
  return <li className="ellipsis">{props.tweet}</li>
}

class Stream extends Component {
  render() {
    let tweets = (this.props && this.props.tweetList) || [];

    const listItems = tweets.map((tweet) => {
      return (
        <ListItem key={tweet.id} tweet={tweet.text} />
      );
    });

    return (
      <section>
        <h4>{this.props.keyword}</h4>
        <ul className="list-reset">
          {listItems}
        </ul>
      </section>
    );
  }
}

export default Stream;
