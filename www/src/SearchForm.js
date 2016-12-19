import React, { Component } from 'react';

class SearchForm extends Component {
  constructor(props) {
    super(props);

    this.state = {
      keyword: '',
      threshold: 5,
      min: 1,
      max: 60,
    };
  }

  render() {
    return (
      <form className="search" role="form" onSubmit={this.handleSubmit}>
        <div>
          <label htmlFor="keyword">Keyword</label>
          <input
            type="text" id="keyword" required
            placeholder="E.g. javascript"
            value={this.state.keyword}
            onChange={this.handleKeywordChange} />
        </div>
        <div>
          <label htmlFor="threshold">Threshold</label>
          <input
            type="range" id="threshold"
            min={this.state.min} max={this.state.max}
            value={this.state.threshold}
            onChange={this.handleThresholdChange} />
          <output htmlFor="threshold">{this.state.threshold}</output>
        </div>
        <div>
          <input type="submit" name="go" value="Go" />
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
  }
}

export default SearchForm;
