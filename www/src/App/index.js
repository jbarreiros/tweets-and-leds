import React, { Component } from 'react';
import './app.css';
import ConfigForm from '../ConfigForm';
import StreamLog from '../StreamLog';

const ws = new WebSocket('ws://rasppiboyee.lan:9000');
ws.onopen = () => console.log('Websocket opened');
ws.onerror = (error) => console.log('Websocket error', error);
ws.onmessage = (e) => console.log('Websocket message received: ', e.data);

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      keyword: '',
      threshold: null,
    };
  }

  render() {
    return (
      <div className="app">
        <ConfigForm onSubmit={this.changeConfig} />
        <StreamLog keyword={this.state.keyword} threshold={this.state.threshold} />
      </div>
    );
  }

  changeConfig = (keyword, threshold) => {
    this.setState({keyword, threshold});
    console.log('Send message to websocket', {keyword, threshold});
    ws.send(JSON.stringify({keyword, threshold}));
  }
}

export default App;
