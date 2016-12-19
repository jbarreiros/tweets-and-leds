import React, { Component } from 'react';

class Stream extends Component {
  render() {
    let tweets = (this.props && this.props.tweets) || [];

    const listItems = tweets.map((tweet) => (
        <div key={tweet.id}>{tweet.title}</div>
      )
    );

    return (
      <section className="stream-wrap">
        <h4>{this.props.keyword}</h4>
        <div className="stream">
          {listItems}
        </div>
      </section>
    );
  }
}

export default Stream;
