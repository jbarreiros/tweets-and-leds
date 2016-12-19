import React, { Component } from 'react';
import './app.css';
import SearchForm from './SearchForm';
import Stream from './Stream';

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
        <SearchForm onSubmit={this.changeStream} />
        <Stream keyword={this.state.keyword} threshold={this.state.threshold} />
      </div>
    );
  }

  changeStream = (keyword, threshold) => {
    this.setState({keyword, threshold});
  }
}

export default App;
