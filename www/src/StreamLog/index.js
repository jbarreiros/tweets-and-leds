import React, { Component } from 'react';
import './stream-log.css';

class Stream extends Component {
  render() {
    let tweets = (this.props && this.props.tweets) || [];

    const listItems = tweets.map((tweet) => (
        <div key={tweet.id}>{tweet.title}</div>
      )
    );

    return (
      <section>
        <h4>{this.props.keyword}</h4>
        <div>
          {listItems}
        </div>
      </section>
    );
  }
}

export default Stream;