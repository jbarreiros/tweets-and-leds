import React, { Component } from 'react';
import './app.css';
import ConfigForm from '../ConfigForm';
import StreamLog from '../StreamLog';

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
  }
}

export default App;
