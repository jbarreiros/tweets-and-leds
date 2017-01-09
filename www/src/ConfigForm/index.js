import React, { Component } from 'react';
import './config-form.css';

class SearchForm extends Component {
  constructor(props) {
    super(props);
    this.state = this.getInitFormValues();
  }

  render() {
    return (
      <form role="form" className="inline-block" onSubmit={this.handleSubmit}>
        <div className="mb2">
          <label className="block" htmlFor="keyword">Keyword</label>
          <input
            type="text" id="keyword" required
            placeholder="E.g. javascript"
            value={this.state.keyword}
            onChange={this.handleKeywordChange} />
        </div>
        <div className="mb2">
          <label className="block" htmlFor="threshold">Threshold</label>
          <input
            type="range" id="threshold"
            className="ml0"
            min="1" max="60"
            value={this.state.threshold}
            onChange={this.handleThresholdChange} />
          <output htmlFor="threshold">{this.state.threshold}</output>
        </div>
        <div>
          <input type="submit" name="go" value="Go" className="block" />
        </div>
      </form>
    );
  }

  handleKeywordChange = (e) => {
    this.setState({
      keyword: e.target.value,
    });
  }

  handleThresholdChange = (e) => {
    this.setState({
      threshold: e.target.value,
    });
  }

  handleSubmit = (e) => {
    e.preventDefault();
    this.props.onSubmit(this.state.keyword, this.state.threshold);
    this.setState(this.getInitFormValues());
  }

  getInitFormValues() {
    return {
      keyword: '',
      threshold: 30
    };
  }
}

export default SearchForm;
