import React, { Component } from 'react';
import './app.css';
import ConfigForm from '../ConfigForm';
import StreamLog from '../StreamLog';
import Socket from '../lib/Socket';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      keyword: '',
      threshold: null,
      tweetList: [],
    };
  }

  componentDidMount() {
    this.ws = new Socket('ws://rasppiboyee.lan:9000/ws');
    this.ws.register('new_tweet', this.onNewTweet);
    this.ws.register('current_config', this.onConfigChanged);
  }

  componentWillUnmount() {
    this.ws.close();
  }

  render() {
    return (
      <div className="app">
        <ConfigForm onSubmit={this.saveConfig} />
        <StreamLog
          keyword={this.state.keyword}
          tweetList={this.state.tweetList}
        />
      </div>
    );
  }

  saveConfig = (keyword, threshold) => {
    this.setState({keyword, threshold, tweetList: []});
    this.ws.sendMessage('set_keyword', {keyword, threshold});
  }

  onNewTweet = (data) => {
    let tweetList = [data, ...this.state.tweetList];

    if (tweetList.length > 10) {
      tweetList.pop();
    }

    this.setState({tweetList});
  }

  onConfigChanged = (data) => {
    data.tweetList = [];
    this.setState(data);
  }
}

export default App;
