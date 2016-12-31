import React, { Component } from 'react';
import './app.css';
import ConfigForm from '../ConfigForm';
import StreamLog from '../StreamLog';
import Socket from '../lib/Socket';

class App extends Component {
  constructor(props) {
    super(props);

    this.ws = new Socket('ws://rasppiboyee.lan:9000/ws');
    this.ws.register(this.onSocketMessage);

    this.state = {
      keyword: '',
      threshold: null,
      tweetList: [],
    };
  }

  render() {
    return (
      <div className="app">
        <ConfigForm onSubmit={this.changeConfig} />
        <StreamLog
          keyword={this.state.keyword}
          threshold={this.state.threshold}
          tweetList={this.state.tweetList}
        />
      </div>
    );
  }

  changeConfig = (keyword, threshold) => {
    this.setState({keyword, threshold, tweetList: []});
    this.ws.sendMessage({keyword, threshold});
  }

  onSocketMessage = (data) => {
    if (typeof data === 'object') {
      let tweetList = [...this.state.tweetList, data];
      this.setState({tweetList});
    }
  }
}

export default App;
